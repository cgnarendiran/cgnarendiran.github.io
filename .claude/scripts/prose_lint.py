#!/usr/bin/env python3
"""Mechanical checks for the sentence shapes Naren rejects as "nobody writes like this".

Usage:
  prose_lint.py <post.md>              blog post thresholds
  prose_lint.py --linkedin <file>      LinkedIn post thresholds (outbox file or plain text)

Scans prose only: skips front matter, headings, code fences, display math, tables,
blockquotes, list items, image lines and italic caption lines. Prints one line per finding
and a summary. Exit 1 on any ERROR, 0 otherwise (warnings do not fail).

Errors
  negation triplet      "no X, no Y, no Z"
  fragment run          a second paragraph with 3+ consecutive sentences of 6 words or fewer
                        (one such triplet per post is a deliberate move; two is a habit)
  aphorism run          a second run of 3+ paragraphs ending on a sentence of 8 words or fewer
  fragment sentences    3+ sentences like "Not a long thin one." / "Could be a hinge." / "Just a gauge."
  colon labels          (LinkedIn) "My read:", "The dragons:", "Bottom line:" opening a sentence
Warnings
  colon labels          (blog) the same, as a warning
  landing-line ratio    more than 25% of multi-sentence paragraphs end on a short sentence
                        (the style guide's target is about one in six); the lines are listed
  too few asides        fewer than 3 parenthetical asides of 20+ characters (LinkedIn: 1)
  too few questions     fewer than 3 question marks in prose (LinkedIn: 1)
  arch commentary       "which is the healthiest possible sign", "for reasons that took", and similar
  banned vocabulary     the blog guide's section 13 list
"""
import re
import sys

BANNED = r"\b(additionally|delve|realm|tapestry|landscape|harness|unlock|leverage|utilize|facilitate|crucial|pivotal|testament|underscores?|showcas\w*|groundbreaking|revolutionary|seamless|cutting-edge|game-chang\w*|vibrant)\b"
ARCH = [r"healthiest possible sign", r"for reasons that took", r"dressed in overalls", r"a polite way of saying",
        r"is not a result .* prepared", r"moved house", r"the entire theoretical content", r"which is to say nothing of"]
LABEL = re.compile(r"^(My read|My take|The dragons|The stance|The bet|The catch|Bottom line|The takeaway|The kicker|The upshot|Translation|The lesson):", re.I)
FRAG = re.compile(r"^(Not|Just|Could be|Same|No) [^.!?]{0,45}[.!?]$")
NEG3 = re.compile(r"\b[Nn]o [^,.;:]{1,30}, no [^,.;:]{1,30},? (and )?no \b")
SENT_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z"\'(*$\[])')


def prose_paragraphs(text):
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        try:
            end = lines.index("---", 1)
            lines = lines[end + 1:]
        except ValueError:
            pass
    paras, cur, in_code, in_math = [], [], False, False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if s == "$$":
            in_math = not in_math
            continue
        if in_code or in_math:
            continue
        skip = (not s or s.startswith("#") or s.startswith("|") or s.startswith(">") or s.startswith("![")
                or s.startswith("*Figure") or s.startswith("*On the cover") or s.startswith("- ")
                or re.match(r"^\d+\. ", s) or s.startswith("http") or s.startswith("@["))
        if skip:
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(s)
    if cur:
        paras.append(" ".join(cur))
    return paras


def sentences(p):
    p = re.sub(r"\$[^$]*\$", "X", p)               # inline math counts as one word
    p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)  # links to their text
    return [s.strip() for s in SENT_SPLIT.split(p) if s.strip()]


def words(s):
    return len(re.findall(r"[A-Za-z0-9'%$.-]+", s))


def main():
    args = sys.argv[1:]
    linkedin = "--linkedin" in args
    args = [a for a in args if a != "--linkedin"]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    text = open(args[0], encoding="utf-8").read()
    paras = prose_paragraphs(text)
    errors, warns = [], []

    for m in NEG3.finditer(" ".join(paras)):
        errors.append(f"negation triplet: '{m.group(0).strip()}'")

    frag_sents, frag_runs, labels = [], [], []
    for p in paras:
        ss = sentences(p)
        run = 0
        for i, s in enumerate(ss):
            if LABEL.match(s):
                labels.append(s[:50])
            if FRAG.match(s):
                frag_sents.append(s)
            if words(s) <= 6:
                run += 1
                if run == 3:
                    frag_runs.append(" ".join(ss[i - 2:i + 1]))
            else:
                run = 0
    for l in labels:
        (errors if linkedin else warns).append(f"colon label: '{l}'")
    for i, r in enumerate(frag_runs):
        (warns if i == 0 else errors).append(f"fragment run{' (the one allowed)' if i == 0 else ''}: '{r}'")
    if len(frag_sents) >= 3:
        errors.append("fragment sentences: " + " | ".join(frag_sents[:6]))
    elif frag_sents:
        warns.append("fragment sentence: " + " | ".join(frag_sents))

    multi = [p for p in paras if len(sentences(p)) >= 2]
    closes = [words(sentences(p)[-1]) <= 8 for p in multi]
    run, aph_runs = 0, []
    for p, c in zip(multi, closes):
        run = run + 1 if c else 0
        if run == 3:
            aph_runs.append(sentences(p)[-1])
    for i, r in enumerate(aph_runs):
        (warns if i == 0 else errors).append(f"aphorism run{' (the one allowed)' if i == 0 else ''}: three paragraphs in a row end on a short sentence, ending '{r}'")
    if multi and sum(closes) / len(multi) > 0.25:
        landing = [sentences(p)[-1] for p, c in zip(multi, closes) if c]
        warns.append(f"landing-line ratio: {sum(closes)}/{len(multi)} multi-sentence paragraphs end on a sentence of 8 words or fewer; aim for 1 in 6. Each must be a joke or a fact: " + " | ".join(landing[:8]))

    prose = " ".join(paras)
    asides = re.findall(r"\(([^()]{20,})\)", prose)
    min_asides = 1 if linkedin else 3
    if len(asides) < min_asides:
        warns.append(f"too few asides: {len(asides)} parenthetical asides of 20+ characters, want {min_asides}+")
    qs = prose.count("?")
    min_q = 1 if linkedin else 3
    if qs < min_q:
        warns.append(f"too few questions: {qs} question marks in prose, want {min_q}+")
    for pat in ARCH:
        for m in re.finditer(pat, prose, re.I):
            warns.append(f"arch commentary: '{m.group(0)}'")
    for m in re.finditer(BANNED, prose, re.I):
        warns.append(f"banned vocabulary: '{m.group(0)}'")

    for e in errors:
        print("ERROR  " + e)
    for w in warns:
        print("WARN   " + w)
    print(f"summary: {len(paras)} paragraphs, {len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
