# sources.py
import re

__all__ = [
    "find_sources_section",
    "normalize_url",
    "extract_source_count",
]

def find_sources_section(content: str) -> str:
    """
    Return the markdown substring that belongs to the *last* Sources/References
    section. If no such header is found, return an empty string.

    We match headers like (case-insensitive, any heading level):
        ## Sources
        ## References
        ## Bibliography
        ## Works cited
    """
    header_re = re.compile(r'(?im)^\s*#{1,6}\s*(sources|references|bibliography|works\s+cited)\s*$')
    matches = list(header_re.finditer(content))
    if not matches:
        return ""

    start = matches[-1].end()

    # Next header marks the end; if none, use EOF
    next_header_re = re.compile(r'(?im)^\s*#{1,6}\s+\S+.*$')
    m2 = next_header_re.search(content, pos=start)
    end = m2.start() if m2 else len(content)
    return content[start:end]


def normalize_url(u: str) -> str:
    """
    Normalize URLs/DOIs for robust deduplication:
      - strip trailing punctuation
      - DOI variants -> https://doi.org/<doi>
      - normalize http(s) and www to https://
      - drop obvious tracking params (utm_*, ref=) conservatively
    """
    u = u.strip().rstrip(').,;:]')

    # DOI variants
    if re.match(r'(?i)^doi:\s*10\.\d{4,9}/\S+$', u):
        u = re.sub(r'(?i)^doi:\s*', 'https://doi.org/', u)
    elif re.match(r'^10\.\d{4,9}/\S+$', u):
        u = 'https://doi.org/' + u

    # http(s) normalization
    u = re.sub(r'^https?://(www\.)?', 'https://', u)

    # conservative removal of common tracking params
    u = re.sub(r'(\?|&)utm_[^=&]+=[^&]+', '', u)
    u = re.sub(r'(\?|&)ref=[^&]+', '', u)

    return u


def extract_source_count(content: str) -> int:
    """
    Count *unique* sources **only** from the terminal Sources/References section.
    This deliberately ignores inline links in the main body.

    Supports:
      - Markdown links: [text](https://...)
      - Bare URLs:      https://...
      - DOIs:           10.XXXX/...  or "doi: 10.XXXX/..."

    Returns
    -------
    int
        Number of unique, normalized URLs.
    """
    section = find_sources_section(content)
    if not section:
        return 0

    urls = set()

    # 1) Markdown link targets
    for u in re.findall(r'\((https?://[^\s)]+)\)', section):
        urls.add(normalize_url(u))

    # 2) Bare URLs
    for u in re.findall(r'https?://[^\s)]+', section):
        urls.add(normalize_url(u))

    # 3) DOIs (with/without prefix)
    for doi in re.findall(r'(?i)\b(?:doi:\s*)?10\.\d{4,9}/\S+\b', section):
        urls.add(normalize_url(doi))

    return len(urls)
