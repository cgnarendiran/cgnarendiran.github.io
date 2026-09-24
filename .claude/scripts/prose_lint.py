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
  jargon                (LinkedIn) 3+ distinct ML terms a non-technical reader would not know
                        (token, encoder, gradient, KV cache, kernel, ...); the post is for
                        people with no ML background (LinkedIn guide §0). Hashtag lines are skipped
  pipe in inline math   an unescaped | inside $...$ on the first line of a paragraph ("$1/|o_i|$");
                        kramdown turns the paragraph into a table before MathJax sees it. Write \vert
  stray $$ in prose     an odd number of $$ on a prose line ("$1/|o_i|$$"); it opens a display
                        block that swallows the rest of the paragraph
Warnings
  colon labels          (blog) the same, as a warning
  landing-line ratio    more than 25% of multi-sentence paragraphs end on a short sentence
                        (the style guide's target is about one in six); the lines are listed
  too few asides        fewer than 3 parenthetical asides of 20+ characters (LinkedIn: 1)
  too few questions     fewer than 3 question marks in prose (LinkedIn: 1)
  arch commentary       "which is the healthiest possible sign", "for reasons that took", "the whole way
                        through", "than anybody admits", and similar (style guide §20)
  chained sentence      one sentence carrying two or more ", and" / ", so" / ", which" / ", but" joins;
                        split it into simple statements (§20.1)
  long sentence         more than 35 words in one sentence (§20.1)
  stopped/became        "X stopped being A and became B", the chiasmus form of negate-then-reveal (§18.4)
  negate-then-reveal    a short "... is not X." followed by "It is / They are / It just ..." (§18.4)
  banned vocabulary     the blog guide's section 13 list
  jargon                (LinkedIn) 1-2 ML terms: each must be explained in everyday words or cut
  long sentence         (LinkedIn) more than 25 words in one sentence
"""
import re
import sys

BANNED = r"\b(additionally|delve|realm|tapestry|landscape|harness|unlock|leverage|utilize|facilitate|crucial|pivotal|testament|underscores?|showcas\w*|groundbreaking|revolutionary|seamless|cutting-edge|game-chang\w*|vibrant)\b"
ARCH = [r"healthiest possible sign", r"for reasons that took", r"dressed in overalls", r"a polite way of saying",
        r"is not a result .* prepared", r"moved house", r"the entire theoretical content", r"which is to say nothing of",
        r"the whole way through", r"than (anybody|anyone) (admits|realises|realizes)", r"\bnobody likes (this|that|it)\b",
        r"which is a lovely thing to find", r"is the interesting part", r"the thing that actually works", r"in a footnote, wearing",
        r"owes you nothing", r"it breaks it completely", r"a batching story",
        r"\b(and )?(nobody|no one) has (even )?\w+[^.!?]{0,60}\byet\b", r"and (we|you) (have not|haven't) even\b"]
JOIN = re.compile(r", (and|so|which|but) ")
STOPPED = re.compile(r"\bstopped being\b[^.!?]{1,90}\bbec(ame|omes)\b", re.I)
NEG_SENT = re.compile(r"\b(is|are|was|were|isn't|aren't|wasn't) not\b|\b(isn't|aren't|wasn't)\b", re.I)
REVEAL = re.compile(r"^(It|They|It's|That) (is|are|was|just|were)\b")
LABEL = re.compile(r"^(My read|My take|The dragons|The stance|The bet|The catch|Bottom line|The takeaway|The kicker|The upshot|Translation|The lesson):", re.I)
FRAG = re.compile(r"^(Not|Just|Could be|Same|No) [^.!?]{0,45}[.!?]$")
NEG3 = re.compile(r"\b[Nn]o [^,.;:]{1,30}, no [^,.;:]{1,30},? (and )?no \b")
# Terms a reader with no ML background would stop at. Model and product names (Mamba, ChatGPT)
# are not jargon; "AI" and "model" are not either.
JARGON = [r"tokens?", r"tokeni[sz]\w*", r"encoders?", r"decoders?", r"embeddings?", r"gradients?", r"logits?",
          r"softmax", r"kv cache", r"cache", r"kernels?", r"convolution\w*", r"cnns?", r"rnns?", r"lstms?",
          r"transformers?", r"self-attention", r"attention (layer|head)s?", r"parameters?", r"fine-tun\w*",
          r"backprop\w*", r"inference", r"latents?", r"vectors?", r"matri(x|ces)", r"tensors?", r"quanti[sz]\w*",
          r"perplexity", r"benchmarks?", r"ablations?", r"regulari[sz]\w*", r"loss function", r"the loss",
          r"optimi[sz]ers?", r"epochs?", r"autoregressive", r"pre-?train\w*", r"rlhf", r"reward model",
          r"state space", r"ssms?", r"recurren\w*", r"discreti[sz]\w*", r"distillation", r"llms?",
          r"architectures?", r"weights", r"activations?", r"hyperparameters?", r"on-policy", r"off-policy",
          r"diffusion", r"eigen\w*", r"fft", r"gpus?", r"vram", r"h100s?", r"flops?", r"throughput", r"latency"]
JARGON_RE = re.compile(r"\b(" + "|".join(JARGON) + r")\b", re.I)
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


def math_lint(text):
    """Errors for markdown/MathJax interactions that silently break a paragraph's rendering.

    Kramdown's table parser runs before MathJax. An unescaped | on the FIRST line of a paragraph
    turns the paragraph into a table (a | on a continuation line, or an escaped \|, does not).
    A single $$...$$ pair on one line is kramdown inline math and is fine; an odd number of $$ on
    a line is a stray delimiter that swallows the rest of the paragraph.
    """
    errs = []
    lines = text.split("\n")
    offset = 0
    if lines and lines[0].strip() == "---":
        try:
            offset = lines.index("---", 1) + 1
            lines = lines[offset:]
        except ValueError:
            pass
    in_code = in_math = False
    block_start = True
    for n, line in enumerate(lines, offset + 1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if s == "$$":
            in_math = not in_math
            block_start = False
            continue
        if in_math:
            continue
        if not s:
            block_start = True
            continue
        if s.count("$$") % 2 == 1:
            errs.append(f"stray $$ in prose (line {n}): '{s[:70]}'")
        if block_start and not s.startswith("|"):
            for m in re.finditer(r"(?<!\$)\$(?!\$)[^$\n]+(?<!\$)\$(?!\$)", s):
                if re.search(r"(?<!\\)\|", m.group(0)):
                    errs.append(f"pipe in inline math (line {n}): '{m.group(0)}' turns the paragraph into a kramdown table; use \\vert")
        block_start = False
    return errs


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
    if not linkedin:
        errors.extend(math_lint(text))

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

    chained, longs, negrev = [], [], []
    for p in paras:
        ss = sentences(p)
        for i, s_ in enumerate(ss):
            if s_.startswith(("where ", "This is the story of")):  # symbol lists and the §3 thesis line
                pass
            elif len(JOIN.findall(s_)) >= 2:
                chained.append(s_)
            elif words(s_) > 35:
                longs.append(s_)
            if i + 1 < len(ss) and words(s_) <= 14 and NEG_SENT.search(s_) and REVEAL.match(ss[i + 1]):
                negrev.append(s_ + " " + ss[i + 1])
    if not linkedin:
        if chained:
            warns.append(f"chained sentences: {len(chained)} sentences carry two or more ', and/so/which/but' joins; split each into simple statements: " + " | ".join(c[:90] + "..." for c in chained[:8]))
        if longs:
            warns.append(f"long sentences: {len(longs)} over 35 words: " + " | ".join(l[:90] + "..." for l in longs[:8]))
    for n_ in negrev:
        warns.append(f"negate-then-reveal: '{n_[:140]}'")

    prose = " ".join(paras)
    for m in STOPPED.finditer(prose):
        warns.append(f"stopped/became: '{m.group(0)}'")
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

    if linkedin:
        found = {}
        for m in JARGON_RE.finditer(prose):
            found.setdefault(m.group(0).lower(), m.group(0))
        if len(found) >= 3:
            errors.append(f"jargon: {len(found)} ML terms a non-technical reader would not know: " + ", ".join(found.values()) + ". Keep at most two, each explained in everyday words (LinkedIn guide §0)")
        elif found:
            warns.append("jargon: " + ", ".join(found.values()) + ". Explain each in everyday words or cut it (LinkedIn guide §0)")
        longs_li = [s_ for p in paras for s_ in sentences(p) if words(s_) > 25]
        for l in longs_li:
            warns.append(f"long sentence: {words(l)} words: '{l[:90]}...'")

    for e in errors:
        print("ERROR  " + e)
    for w in warns:
        print("WARN   " + w)
    print(f"summary: {len(paras)} paragraphs, {len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
