#!/usr/bin/env python3
"""
Extract the 100 testable conservation questions from:
Sutherland et al. (2022) "Creating testable questions in practical conservation:
a process and 100 questions", Conservation Evidence Journal 19, 1-7.

Source PDF: https://conservationevidencejournal.com/reference/pdf/11619

Output: a CSV with one row per question:
    index, question, theme

Usage:
    python extract_questions.py [--pdf path/to/local.pdf] [--out questions.csv]

If --pdf is omitted, the script downloads the PDF from the journal URL.
"""

import argparse
import csv
import io
import os
import re
import sys

PDF_URL = "https://conservationevidencejournal.com/reference/pdf/11619"

# The five overarching themes used in the paper, with the question-number range
# each one covers (per the article's own grouping).
THEMES = [
    ("Invasive and problem species", 1, 18),
    ("Habitat creation", 19, 52),
    ("Habitat management", 53, 74),
    ("Infrastructure such as nest boxes", 75, 90),
    ("Working with others", 91, 100),
]


def theme_for(num: int) -> str:
    for name, lo, hi in THEMES:
        if lo <= num <= hi:
            return name
    return ""


def get_pdf_bytes(local_path: str | None) -> bytes:
    if local_path:
        with open(local_path, "rb") as f:
            return f.read()
    import requests
    headers = {"User-Agent": "Mozilla/5.0 (question-extractor)"}
    resp = requests.get(PDF_URL, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.content


def extract_text(pdf_bytes: bytes) -> str:
    """
    The paper is laid out in TWO COLUMNS. A naive extract_text() reads across
    both columns and interleaves them, corrupting every question. So for each
    page we crop the left half and the right half separately, extract each in
    reading order, then concatenate left-then-right per page.
    """
    import pdfplumber
    parts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            w, h = page.width, page.height
            mid = w / 2.0
            # Small overlap margin so glyphs straddling the centre aren't lost.
            left = page.crop((0, 0, mid + 5, h))
            right = page.crop((mid - 5, 0, w, h))
            ltext = left.extract_text(x_tolerance=1.5) or ""
            rtext = right.extract_text(x_tolerance=1.5) or ""
            parts.append(ltext)
            parts.append(rtext)
    return "\n".join(parts)


def parse_questions(text: str) -> list[tuple[int, str]]:
    """
    Questions are numbered 1..100. Each begins with a number at a line start
    (e.g. "1. Are chemical treatments...") and runs until the next number.
    We join the whole document and split on the "<n>." markers in order.
    """
    # Normalise whitespace but keep it as a single stream.
    flat = re.sub(r"[ \t]+", " ", text)
    flat = re.sub(r"\n+", "\n", flat)

    # Find every "<number>." that starts a question. The expected sequence is
    # 1..100. We walk the numbers in order so stray numbers (years, references)
    # don't derail us.
    results: list[tuple[int, str]] = []
    expected = 1
    # Pattern: a question number is a 1-3 digit number followed by '.' and a space,
    # appearing at a line start OR after a newline.
    # We locate the start offset of each expected number specifically.
    search_from = 0
    while expected <= 100:
        # Look for the expected number followed by '.' near a line boundary.
        pat = re.compile(r"(?:^|\n)\s*%d[\.\)]\s+" % expected)
        m = pat.search(flat, search_from)
        if not m:
            # Some PDFs collapse "100." onto the previous line; try anywhere.
            pat2 = re.compile(r"(?<!\d)%d[\.\)]\s+" % expected)
            m = pat2.search(flat, search_from)
            if not m:
                break
        start = m.end()
        # End = start of the next expected number.
        if expected < 100:
            nxt = re.compile(r"(?:^|\n)\s*%d[\.\)]\s+" % (expected + 1))
            mn = nxt.search(flat, start)
            if not mn:
                nxt2 = re.compile(r"(?<!\d)%d[\.\)]\s+" % (expected + 1))
                mn = nxt2.search(flat, start)
            end = mn.start() if mn else len(flat)
        else:
            # Last question: cut at the DISCUSSION section if present.
            disc = re.search(r"\nDISCUSSION", flat[start:])
            end = start + disc.start() if disc else len(flat)

        q = flat[start:end].strip()
        q = re.sub(r"\s+", " ", q)
        # Strip trailing theme headers that may bleed in.
        for name, _, _ in THEMES:
            q = q.replace(name, "").strip()
        # Strip footer noise: page numbers, ISSN line, running header.
        q = re.sub(r"\s+ISSN\s*1758-?2067.*$", "", q)
        q = re.sub(r"\s+W\.J\. Sutherland.*$", "", q)
        # Running header bleed (possibly truncated by the column crop), e.g.
        # "... 4 tion Evidence Journal (2022) 19, 1-7".
        q = re.sub(r"\s+\d{0,2}\s*[A-Za-z]*\s*Evidence Journal.*$", "", q)
        q = re.sub(r"\s+et al\..*Conservation.*$", "", q)
        q = re.sub(r"\s+\d{1,2}\s*$", "", q)  # trailing bare page number
        # Normalize smart punctuation to plain ASCII (prevents â€™-style mojibake
        # when the CSV is opened in cp1252 readers like Excel).
        q = (q.replace("\u2019", "'").replace("\u2018", "'")
               .replace("\u201c", '"').replace("\u201d", '"')
               .replace("\u2013", "-").replace("\u2014", "-")
               .replace("\u00a0", " "))
        q = q.strip()
        results.append((expected, q))
        search_from = end
        expected += 1

    return results


def write_csv(rows: list[tuple[int, str]], out_path: str) -> None:
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["", "Your research question.", "Theme"])
        for num, q in rows:
            w.writerow([num, q, theme_for(num)])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", help="local PDF path (skips download)")
    ap.add_argument("--out", default="sutherland_100_questions.csv",
                    help="output CSV filename (or full path)")
    ap.add_argument("--output", "--output-dir", dest="output_dir", default=None,
                    help="output folder; --out is written inside it. "
                         "Created if it does not exist.")
    args = ap.parse_args()

    # Resolve the final output path. If --output is given, join it with --out
    # (using only the basename of --out so a folder + filename combine cleanly).
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        out_path = os.path.join(args.output_dir, os.path.basename(args.out))
    else:
        out_path = args.out
        parent = os.path.dirname(out_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    pdf_bytes = get_pdf_bytes(args.pdf)
    text = extract_text(pdf_bytes)
    rows = parse_questions(text)

    if len(rows) != 100:
        print(f"WARNING: extracted {len(rows)} questions, expected 100",
              file=sys.stderr)

    write_csv(rows, out_path)
    print(f"Wrote {len(rows)} questions to {out_path}")
    return 0 if len(rows) == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
