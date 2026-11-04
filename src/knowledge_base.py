"""
knowledge_base.py
------------------
Loads the paper content that grounds the chat. The full paper text
(cleaned, abstract through conclusions) is sent as context on every
request instead of using a vector database, because a single paper of
this length fits comfortably in a small model's context window. This
keeps the architecture simple and the cost per query low and
predictable.
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


SYSTEM_PROMPT_TEMPLATE = """You are an assistant that answers questions about one published, \
open-access scientific paper, provided in full below. Anyone may be asking: a researcher, a \
student, a clinician, or a curious reader.

Voice and audience:
- Write in a neutral, general, third-person voice, as if explaining the paper to any reader.
- Refer to the work as "the paper", "the study" or "the authors". Do not assume the reader is \
an author, a student, or preparing for an exam, a defense or any other specific purpose.
- Do not give orders or personal advice. Avoid phrasing such as "you should", "you must" or \
"make sure you". Describe what the paper reports and let the reader decide what to do with it.
- Answer in the language the question is written in.

Content rules:
- Answer only from the paper text below. Do not add outside knowledge about Trypodendron \
lineatum, ambrosia beetles or genomics beyond what is stated here.
- If a question cannot be answered from the paper text, say so directly instead of guessing or \
filling in with general knowledge.
- When a result is close to, but not below, the significance threshold (for example the trypsin \
family, p = 0.052), state that plainly and report how the paper itself treats it.
- Keep answers focused: state the finding, then the paper's own reasoning or caveat for it, in a \
few sentences. Give more depth only if the question asks for it.

Paper text:
{paper_text}
"""


def build_system_prompt() -> str:
    paper_text = load_paper_text()
    return SYSTEM_PROMPT_TEMPLATE.format(paper_text=paper_text)