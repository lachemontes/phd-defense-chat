"""
app.py
------
A study assistant for PhD defense preparation, grounded in one paper.
Uses the Google Gemini API, which has a free tier (no credit card),
unlike the Anthropic API, which has no free tier at all.

Run with: python -m streamlit run app.py

How the API key works:
- By default the app uses the owner's free-tier key stored in Streamlit
  secrets (GEMINI_API_KEY), so visitors can try it without setting up
  anything. The key is never shown in the page or the code.
- The owner's key has no billing attached, so heavy use can at worst use
  up the free daily quota, never create a charge.
- If that shared quota runs out, or a visitor prefers it, they can paste
  their own free key. It lives only in that browser session.

Reliability, by design:
- Free-tier models can return a temporary 503 (overloaded) or a 429
  (quota). Free quotas are tracked per model, so the app tries a list of
  models in order and uses the first one that answers.
- Models that do not exist or are not on the free tier for this key simply
  fail and the app moves to the next one.
- No guarantee of uptime exists on a free tier. This reduces failures, it
  cannot remove them.

Other cost controls:
- Caps response length (max_output_tokens).
- Caps the number of exchanges per browser session.

Privacy note: on Google's free tier, prompts and responses may be used to
improve Google's products. That is acceptable here because the grounding
content is a published, open-access paper. If you ever swap in different
content, revisit this tradeoff first.
"""

import time

import streamlit as st
from google import genai
from google.genai import types

from src.knowledge_base import build_system_prompt

# Tried in order. Edit this list if Google retires or adds models.
MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
]
ATTEMPTS_PER_MODEL = 2
RETRY_WAIT_SECONDS = 3
MAX_OUTPUT_TOKENS = 600
MAX_MESSAGES_PER_SESSION = 20


def get_owner_key() -> str:
    """Return the owner's key from Streamlit secrets, or an empty string."""
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


def build_contents(messages):
    """Turn the visible chat into Gemini contents.

    Error replies are skipped, and consecutive turns from the same role are
    merged, so the model always sees a clean user/model alternation.
    """
    turns = []
    for m in messages:
        if m.get("error"):
            continue
        role = "user" if m["role"] == "user" else "model"
        if turns and turns[-1][0] == role:
            turns[-1] = (role, turns[-1][1] + "\n\n" + m["content"])
        else:
            turns.append((role, m["content"]))
    return [
        types.Content(role=role, parts=[types.Part(text=text)])
        for role, text in turns
    ]


def ask_gemini(client, contents, system_prompt):
    """Try each model in order. Returns (reply_text, last_error_text)."""
    last_error = None
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=MAX_OUTPUT_TOKENS,
    )
    for model in MODELS:
        for attempt in range(ATTEMPTS_PER_MODEL):
            try:
                response = client.models.generate_content(
                    model=model, contents=contents, config=config
                )
                if response.text:
                    return response.text, None
                last_error = "The model returned an empty response."
                break
            except Exception as e:
                last_error = str(e)
                if "API_KEY_INVALID" in last_error or "API key not valid" in last_error:
                    return None, last_error
                is_busy = "503" in last_error or "UNAVAILABLE" in last_error
                if is_busy and attempt < ATTEMPTS_PER_MODEL - 1:
                    time.sleep(RETRY_WAIT_SECONDS)
                    continue
                break
    return None, last_error


st.set_page_config(
    page_title="Chat with my paper III",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Chat with my paper III")
st.caption(
    "Grounded in one paper: Montes-Ortiz et al. 2026, "
    "\"Comparative genomics reveal signatures of ecological specialization "
    "in the striped ambrosia beetle Trypodendron lineatum,\" BMC Genomics. "
    "Open access."
)

st.info(
    f"This is a scoped chatbot, not a general one. It only answers "
    f"from the paper's text, and this session is capped at "
    f"{MAX_MESSAGES_PER_SESSION} exchanges."
)

# --------------------------------------------------------------------------
# API key: owner's key by default, visitor's own key as optional fallback
# --------------------------------------------------------------------------

owner_key = get_owner_key()

if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

expander_label = (
    "Optional: use your own free Gemini API key"
    if owner_key
    else "Enter your free Gemini API key to use this tool"
)

with st.expander(
    expander_label,
    expanded=not owner_key and not st.session_state.user_api_key,
):
    st.markdown(
        "A free Google Gemini API key lets you use your own quota. Get one "
        "at [aistudio.google.com](https://aistudio.google.com), sign in "
        "with a Google account, click \"Get API key,\" then \"Create API "
        "key.\" No credit card is required."
    )
    entered_key = st.text_input(
        "Your Gemini API key",
        type="password",
        value=st.session_state.user_api_key,
        placeholder="Paste your key here",
    )
    if entered_key != st.session_state.user_api_key:
        st.session_state.user_api_key = entered_key
        st.session_state.pop("gemini_client", None)
        st.session_state.display_messages = []
    st.caption(
        "Your key is used only in this browser session to call Google's "
        "API directly. It is never saved to disk and never sent anywhere "
        "other than Google."
    )

active_key = st.session_state.user_api_key or owner_key
using_owner_key = bool(owner_key) and not st.session_state.user_api_key

if not active_key:
    st.warning("Enter your Gemini API key above to start chatting.")
    st.stop()

if "gemini_client" not in st.session_state:
    try:
        st.session_state.gemini_client = genai.Client(api_key=active_key)
    except Exception as e:
        st.error(f"Could not set up the Gemini client with that key: {e}")
        st.stop()

if "system_prompt" not in st.session_state:
    try:
        st.session_state.system_prompt = build_system_prompt()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

for message in st.session_state.display_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

remaining = MAX_MESSAGES_PER_SESSION - len(st.session_state.display_messages) // 2
st.caption(f"{max(remaining, 0)} exchanges left in this session.")

if remaining <= 0:
    st.warning(
        "This session has reached its message cap. Refresh the page to "
        "start a new session."
    )
    st.stop()

user_input = st.chat_input("Ask about the paper")

if user_input:
    st.session_state.display_messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            contents = build_contents(st.session_state.display_messages)
            reply, error_text = ask_gemini(
                st.session_state.gemini_client,
                contents,
                st.session_state.system_prompt,
            )

        is_error = reply is None
        if is_error:
            error_text = error_text or ""
            is_busy = "503" in error_text or "UNAVAILABLE" in error_text
            is_quota = "429" in error_text or "RESOURCE_EXHAUSTED" in error_text
            if is_quota and using_owner_key:
                reply = (
                    "The shared free quota for this demo has run out for "
                    "now. You can keep going right away by pasting your own "
                    "free Gemini API key in the section above, or try again "
                    "later."
                )
            elif is_busy or is_quota:
                reply = (
                    "Google's models are overloaded right now. This is "
                    "temporary and not caused by your key. Please try again "
                    "in a minute."
                )
            else:
                reply = (
                    f"Something went wrong calling the API: {error_text}\n\n"
                    "If this mentions an invalid key, check that you pasted "
                    "your Gemini API key correctly."
                )
        st.markdown(reply)

    st.session_state.display_messages.append(
        {"role": "assistant", "content": reply, "error": is_error}
    )
    st.rerun()

st.divider()
st.caption("By Zaide Montes")