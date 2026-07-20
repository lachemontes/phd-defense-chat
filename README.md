# PhD Study Chat

By Zaide Montes

**[Live demo](https://phd-defense-chat-mfxc7x5vswsc69bghpvbqq.streamlit.app/)**

A scoped study assistant grounded in one paper: Montes-Ortiz et al. 2026, "Comparative genomics reveal signatures of ecological specialization in the striped ambrosia beetle Trypodendron lineatum," BMC Genomics (open access, DOI: 10.1186/s12864-026-13049-3). Built to help prepare for a PhD defense by answering questions strictly from that paper's text, not from general knowledge about the topic.

## Bring your own key

This app does not use a shared API key. Each visitor pastes in their own free Google Gemini API key directly in the app. That key is used only for that browser session, to call Google's API directly, and is never saved to disk or sent anywhere else. This means the app costs its owner nothing, ever, no matter how much traffic it gets, and there is no shared secret that could ever leak.

## Why this costs nothing to run

This uses the Google Gemini API, specifically Gemini 3.1 Flash-Lite, which has a genuine, permanent free tier: no credit card, no expiration, rate limits generous enough for personal use (roughly 15 to 30 requests per minute and over 1,000 requests per day per key). This is different from the Anthropic Claude API, which has no free tier at all, so this app is built on Gemini specifically for that reason.

The tradeoff: on Google's free tier, prompts and responses may be used to improve their models. That is an acceptable tradeoff here because the content is a published, open-access paper, not private material.

This app also caps responses at 600 tokens and each browser session at 20 exchanges, mainly to keep any one session comfortably under the daily free-tier request quota, not because of any billing risk to the app's owner.

## Getting a free Gemini API key (for visitors using the app)

1. Go to [aistudio.google.com](https://aistudio.google.com) and sign in with a Google account, no credit card needed.
2. Click "Get API key," then "Create API key."
3. Copy the key and paste it into the app when prompted.

## Running it locally (for development)

```bash
git clone <your-repo>
cd phd-defense-chat
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

No secrets file is needed. When the app opens in your browser, paste your own Gemini API key into the field at the top of the page.

Note: use `python -m streamlit run app.py` rather than `streamlit run app.py` if your system has more than one Python environment active (for example, both conda and a venv), since the plain `streamlit` command can sometimes resolve to the wrong Python and fail to find installed packages.

## Deploying to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click "Create app," point it at this repo, branch `main`, main file `app.py`.
4. Deploy. No secrets configuration is needed, since there is no shared key.

## Using it for defense prep

Ask it to explain a specific result, quiz you on a method, or role-play as a skeptical committee member pushing on a weak point, for example the trypsin family's near-significant p-value of 0.052. It will decline to answer anything outside the paper's content rather than filling in with outside knowledge, which matters for defense prep specifically: you want answers that match what you can actually defend from your own study.

## Project structure

```
phd-defense-chat/
    app.py
    src/
        knowledge_base.py
    data/
        paper_trypodendron_lineatum.md
    requirements.txt
    README.md
```

## Data license

The paper content in `data/paper_trypodendron_lineatum.md` is drawn from Montes-Ortiz et al. 2026, BMC Genomics, published open access under a Creative Commons license by the paper's own authors.
