"""
knowledge_base.py
------------------
Loads the paper content that grounds the chat. The full paper text
(cleaned, abstract through conclusions) is sent as context on every
request instead of using a vector database, because a single paper of
this length fits comfortably in a small model's context window. This
keeps the architecture simple and the cost per query low and
predictable, appropriate for a personal study tool with a tight budget.
"""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PAPER_PATH = DATA_DIR / "paper_trypodendron_lineatum.md"


def load_paper_text() -> str:
    if not PAPER_PATH.exists():
        raise FileNotFoundError(
            f"Paper knowledge base not found at {PAPER_PATH}. "
            "Add the paper content file before running the app."
        )
    return PAPER_PATH.read_text(encoding="utf-8")


SYSTEM_PROMPT_TEMPLATE = """You are a focused study assistant helping Zaide Montes-Ortiz prepare \
for her PhD defense. You answer questions strictly grounded in the paper text provided below, \
which she is the first author of. This is her own published, open-access work.

Rules:
- Answer only using information in the paper text below. Do not use outside knowledge about \
Trypodendron lineatum, ambrosia beetles, or genomics beyond what is stated here, since defense \
answers need to match what is actually written and defensible from this specific study.
- If a question cannot be answered from the paper text, say so directly rather than guessing or \
filling in with general knowledge.
- When useful for defense prep, note where a finding is a p-value close to but not below 0.05 \
(like the trypsin family), since a committee member may probe the distinction between \
significant and near-significant results.
- Keep answers focused and exam-ready: state the fact, then the paper's own reasoning or \
caveat for it, in a few sentences, not a full essay, unless asked for more depth.
- If asked to role-play as a hostile or skeptical committee member, do that directly and \
pointedly, since that is a legitimate and useful part of defense preparation.

Paper text:
{paper_text}
"""


def build_system_prompt() -> str:
    paper_text = load_paper_text()
    return SYSTEM_PROMPT_TEMPLATE.format(paper_text=paper_text)
