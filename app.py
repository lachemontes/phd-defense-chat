"""
app.py
------
A study assistant for PhD defense preparation, grounded in one paper.
Uses the Google Gemini API, which has a genuine, permanent free tier
(no credit card, no expiration), unlike the Anthropic API used elsewhere
in this portfolio, which has no free tier at all.

Run with: streamlit run app.py

Cost control, by design:
- Uses Gemini 2.5 Flash-Lite, the model with the most generous free tier
  rate limits (as of mid-2026: roughly 15 to 30 requests per minute and
  1,000+ requests per day, no card required).
- Caps response length (max_output_tokens).
- Caps the number of exchanges per browser session, mainly to stay well
  under the daily free-tier request quota if the page gets shared, not
  because of any billing risk.

Privacy note, stated plainly for whoever deploys this: on Google's free
tier, prompts and responses may be used to improve Google's products.
That is an acceptable tradeoff here because the grounding content is a
published, open-access paper, not private or sensitive material. If you
ever swap in different content, revisit this tradeoff first.
"""

import streamlit as st
from google import genai
from google.genai import types

from src.knowledge_base import build_system_prompt

MODEL = "gemini-3.1-flash-lite"
MAX_OUTPUT_TOKENS = 600
MAX_MESSAGES_PER_SESSION = 20

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
    f"This is a general chatbot. It only answers "
    f"from the paper's text, and this session is capped at "
    f"{MAX_MESSAGES_PER_SESSION} exchanges."
)

if "api_key_missing" not in st.session_state:
    st.session_state.api_key_missing = "GEMINI_API_KEY" not in st.secrets

if st.session_state.api_key_missing:
    st.error(
        "No API key found. Add GEMINI_API_KEY to Streamlit secrets "
        "before this app can answer questions. See the README for how, "
        "it is free to get one."
    )
    st.stop()

if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

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
            try:
                response = st.session_state.chat_session.send_message(user_input)
                reply = response.text
            except Exception as e:
                reply = f"Something went wrong calling the API: {e}"
        st.markdown(reply)

    st.session_state.display_messages.append({"role": "assistant", "content": reply})
    st.rerun()

st.divider()
st.caption("By Zaide Montes")
