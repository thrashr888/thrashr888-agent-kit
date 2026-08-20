#!/usr/bin/env python3
"""Mechanical tell check for user-facing copy (copy-review skill, Stage 4).

Scans HTML/Markdown/text for the machine-writing tells that survive good
intentions: encoding damage, banned words, em-dash density, repeated-head
triples, and leaked internal vocabulary.

Usage:
    tell-check.py <file-or-dir> [--banned banned.txt] [--vocab vocab.txt]
                  [--allow allow.txt]

banned.txt / vocab.txt / allow.txt: one term per line, '#' comments
allowed. Terms in allow.txt suppress any finding whose flagged text
contains them — the place to encode WRITING.md's named, grandfathered
exceptions (a deliberate hero tricolon, a product name that trips the
banned list). Exit code is the number of findings, so it works as a
commit gate.
"""

import argparse
import pathlib
import re
import sys

DEFAULT_BANNED = [
    "vibes", "seamless", "supercharge", "game-changing", "delve",
    "honestly", "revolutionize", "unleash", "elevate your",
]

EXTS = {".html", ".htm", ".md", ".txt"}


def load_terms(path):
    if not path:
        return []
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.startswith("#")]


def visible_text(raw, is_html):
    if not is_html:
        return raw
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S)
    s = re.sub(r"<[^>]+>", "\n", s)
    for ent, ch in [("&mdash;", "—"), ("&ndash;", "–"),
                    ("&rsquo;", "’"), ("&nbsp;", " "), ("&amp;", "&")]:
        s = s.replace(ent, ch)
    return s


def check_file(path, banned, vocab):
    findings = []
    data = path.read_bytes()

    # 1. Encoding: UTF-8 double-encoding leaves C3 A2 / C3 83 pairs that
    # render as mojibake. Byte-level so it works before any decode.
    double = data.count(b"\xc3\xa2") + data.count(b"\xc3\x83")
    if double:
        findings.append(f"{path}: {double} double-encoded UTF-8 sequence(s) — "
                        "fix the file encoding, not the strings")

    text = visible_text(data.decode("utf-8", errors="replace"),
                        path.suffix in {".html", ".htm"})
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # 2. Banned words and leaked vocabulary.
    for term in banned + vocab:
        for l in lines:
            if term.lower() in l.lower():
                kind = "banned" if term in banned else "internal vocab"
                findings.append(f"{path}: {kind} '{term}': {l[:90]}")
                break

    # 3. Em-dash density: more than one per prose block.
    for l in lines:
        if len(l) > 80 and l.count("—") > 1:
            findings.append(f"{path}: multiple em dashes in one paragraph: {l[:90]}")

    # 4. Repeated-head triples ("real X, real Y, real Z"), case-insensitive.
    for m in re.finditer(
            r"\b(\w+) ([\w-]+), \1 ([\w-]+), (?:and )?\1 ([\w-]+)",
            text, re.IGNORECASE):
        findings.append(f"{path}: repeated-head triple: {m.group(0)}")

    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--banned", help="extra banned terms, one per line")
    ap.add_argument("--vocab", help="internal vocabulary terms, one per line")
    ap.add_argument("--allow", help="grandfathered phrases to suppress")
    args = ap.parse_args()

    banned = DEFAULT_BANNED + load_terms(args.banned)
    vocab = load_terms(args.vocab)
    allow = load_terms(args.allow)

    target = pathlib.Path(args.target)
    files = ([target] if target.is_file()
             else sorted(p for p in target.rglob("*") if p.suffix in EXTS))

    findings = []
    for f in files:
        findings.extend(check_file(f, banned, vocab))
    findings = [f for f in findings
                if not any(a.lower() in f.lower() for a in allow)]

    for f in findings:
        print(f)
    print(f"\n{len(findings)} finding(s) across {len(files)} file(s)")
    sys.exit(min(len(findings), 100))


if __name__ == "__main__":
    main()
