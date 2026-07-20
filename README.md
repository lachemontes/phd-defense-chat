# PhD Defense Study Chat

By Zaide Montes

A scoped study assistant grounded in one paper: Montes-Ortiz et al. 2026, "Comparative genomics reveal signatures of ecological specialization in the striped ambrosia beetle Trypodendron lineatum," BMC Genomics (open access, DOI: 10.1186/s12864-026-13049-3). Built to help prepare for a PhD defense by answering questions strictly from that paper's text, not from general knowledge about the topic.

## Why this costs nothing to run

This uses the Google Gemini API, specifically Gemini 2.5 Flash-Lite, which has a genuine, permanent free tier as of mid-2026: no credit card, no expiration, rate limits generous enough for a personal portfolio project (roughly 15 to 30 requests per minute and over 1,000 requests per day). This is different from the Anthropic Claude API, which has no free tier at all, so this app is built on Gemini specifically for that reason.

The tradeoff: on the free tier, prompts and responses may be used by Google to improve their models. That is an acceptable tradeoff here because the content is a published, open-access paper, not private material. If this app is ever repurposed with different, more sensitive content, that tradeoff should be reconsidered, and a paid tier without data sharing would be the safer choice at that point.

This app also caps responses at 600 tokens and each browser session at 20 exchanges, mainly to stay comfortably under the daily free-tier request quota if the page gets shared around, not because of any billing risk.

## Setup

### 1. Get a free Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com) and sign in with a Google account, no credit card needed.
2. Click "Get API key," then "Create API key."
3. Copy the key somewhere safe.

### 2. Running locally

```bash
git clone <your-repo>
cd phd-defense-chat
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a file at `.streamlit/secrets.toml` (this file is gitignored, it will not be committed) with:

```toml
GEMINI_API_KEY = "your-key-here"
```

Then run:

```bash
streamlit run app.py
```

### 3. Deploying to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub.
3. Click "Create app," point it at this repo, branch `main`, main file `app.py`.
4. Before or right after deploying, go to the app's Settings, then Secrets, and add:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Deploy.

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
