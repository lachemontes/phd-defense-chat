"""
app.py
------
A study assistant for PhD defense preparation, grounded in one paper.
Uses the Google Gemini API, which has a free tier (no credit card),
unlike the Anthropic API, which has no free tier at all.

Run with: python -m streamlit run app.py

Bring your own key, by design:
Each visitor enters their own free Gemini API key rather than the app
using a single shared key. The owner of this portfolio never pays for or
is rate-limited by anyone else's usage, and there is no shared secret to
leak. The key is kept only in that browser's session state for the
current visit, never written to disk, and sent only to Google's API.

Cost and reliability, by design:
- Uses Gemini 3.1 Flash-Lite, which is available on the free tier.
- Caps response length (max_output_tokens).
- Caps the number of exchanges per browser session.
- Retries a few times when Google returns a temporary 503 (overloaded).

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

MODEL = "gemini-3.1-flash-lite"
MAX_OUTPUT_TOKENS = 600
MAX_MESSAGES_PER_SESSION = 20
MAX_ATTEMPTS = 3

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
# Bring your own API key
# --------------------------------------------------------------------------

if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

with st.expander(
    "Enter your free Gemini API key to use this tool",
    expanded=not st.session_state.user_api_key,
):
    st.markdown(
        "This tool needs your own free Google Gemini API key, not the "
        "portfolio owner's. Get one at "
        "[aistudio.google.com](https://aistudio.google.com), sign in with "
        "a Google account, click \"Get API key,\" then \"Create API key.\" "
        "No credit card is required."
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
        st.session_state.pop("chat_session", None)
        st.session_state.display_messages = []
    st.caption(
        "Your key is used only in this browser session to call Google's "
        "API directly. It is never saved to disk and never sent anywhere "
        "other than Google."
    )

if not st.session_state.user_api_key:
    st.warning("Enter your Gemini API key above to start chatting.")
    st.stop()

if "gemini_client" not in st.session_state:
    try:
        st.session_state.gemini_client = genai.Client(
            api_key=st.session_state.user_api_key
        )
    except Exception as e:
        st.error(f"Could not set up the Gemini client with that key: {e}")
        st.stop()

if "system_prompt" not in st.session_state:
    try:
        st.session_state.system_prompt = build_system_prompt()
    except FileNotFoundError as e:
        st.error(str(e))
        st.stop()

if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.gemini_client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=st.session_state.system_prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )

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
            reply = None
            for attempt in range(MAX_ATTEMPTS):
                try:
                    response = st.session_state.chat_session.send_message(user_input)
                    reply = response.text
                    break
                except Exception as e:
                    error_text = str(e)
                    is_busy = "503" in error_text or "UNAVAILABLE" in error_text
                    if is_busy and attempt < MAX_ATTEMPTS - 1:
                        time.sleep(2 * (attempt + 1))
                        continue
                    if is_busy:
                        reply = (
                            "Google's model is overloaded right now. This is "
                            "temporary and not caused by your key. Please try "
                            "again in a minute."
                        )
                    else:
                        reply = (
                            f"Something went wrong calling the API: {e}\n\n"
                            "If this mentions an invalid key, check that you "
                            "pasted your Gemini API key correctly above."
                        )
                    break
        st.markdown(reply)

    st.session_state.display_messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.divider()
st.caption("By Zaide Montes")