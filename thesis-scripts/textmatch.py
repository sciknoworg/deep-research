# textmatch.py
import re
from typing import List

__all__ = [
    "normalize_separators",
    "unique_phrase_hits",
    "unique_token_presence",
]

def normalize_separators(s: str) -> str:
    """
    Normalize separators and whitespace, and lower-case the string.

    Why? Authors may write "fine-tuning", "fine_tuning", "fine / tuning".
    This normalizer makes them all comparable and robust for regex matching.
    """
    s = re.sub(r'[-–—_/]+', ' ', s)
    return re.sub(r'\s+', ' ', s.strip().lower())


def unique_phrase_hits(text: str, vocab_terms: List[str]) -> int:
    """
    Count *unique* presence (0/1 per vocab term/phrase) with tolerant matching.

    Matching rules:
      - Case-insensitive.
      - Hyphen/underscore/slash tolerant (via normalize_separators).
      - Flexible whitespace between tokens (multi-word phrases).
      - Simple plural tolerance on the LAST token (s|es), e.g., "service(s)".
    """
    if not vocab_terms:
        return 0

    t_norm = normalize_separators(text)
    hits, seen = 0, set()

    for raw in vocab_terms:
        term = normalize_separators(str(raw))
        if not term or term in seen:
            continue
        seen.add(term)

        tokens = [re.escape(tok) for tok in term.split()]
        if not tokens:
            continue

        # Allow flexible whitespace between tokens; plural allowed on the final token only.
        core = tokens[0] if len(tokens) == 1 else r'\s+'.join(tokens[:-1]) + r'\s+' + tokens[-1]
        # Lookarounds prevent partial matches inside larger alphanumeric strings.
        pattern = rf'(?<![A-Za-z0-9]){core}(?:s|es)?(?![A-Za-z0-9])'

        if re.search(pattern, t_norm, flags=re.IGNORECASE):
            hits += 1

    return hits


def unique_token_presence(text_lower: str, terms: List[str]) -> int:
    """
    Count unique presence for a small list of plain tokens (fast substring check).

    Intended for short lists like ["uncertain", "unclear", "unknown"] where full
    regexes are unnecessary and substring behavior is acceptable.
    """
    if not terms:
        return 0
    tl = text_lower.lower()
    uniq = {t.strip().lower() for t in terms if t and t.strip()}
    return sum(1 for tok in uniq if tok in tl)
