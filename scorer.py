import re

def _normalize(text: str) -> str:
    """Lowercase and remove punctuation and whitespace for comparison."""
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", "", text)
    return text


def _contains_phrase(text: str, phrase: str) -> bool:
    """Check if normalized text contains the normalized phrase."""
    return _normalize(phrase) in _normalize(text)


def judge(question: str, expects: str, answer: str, results) -> bool:
    """Judge if the answer contains the expected phrase after normalization."""
    return _contains_phrase(answer, expects)