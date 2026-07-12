import re, pathlib, sys

# (regex, target) — longest/most specific first
TERMS = [
    (r"in-home care", "/guides/in-home-care-explained/"),
    (r"home care", "/guides/in-home-care-explained/"),
    (r"independent living", "/guides/independent-living/"),
    (r"assisted living", "/guides/assisted-living/"),
    (r"memory care", "/guides/memory-care/"),
    (r"skilled nursing", "/guides/skilled-nursing/"),
    (r"nursing homes?", "/guides/skilled-nursing/"),
    (r"respite care", "/guides/respite-care/"),
    (r"respite stays?", "/guides/respite-care/"),
    (r"continuing care retirement communit(?:y|ies)", "/guides/ccrc-life-plan-communities/"),
    (r"CCRCs?", "/guides/ccrc-life-plan-communities/"),
    (r"adult family homes?", "/guides/adult-family-homes/"),
    (r"adult foster homes?", "/guides/adult-family-homes/"),
    (r"residential care homes?", "/guides/adult-family-homes/"),
    (r"hospice", "/guides/hospice-and-palliative-care/"),
    (r"palliative care", "/guides/hospice-and-palliative-care/"),
    (r"estate recovery", "/guides/medicaid-estate-recovery/"),
    (r"Medicaid", "/guides/medicaid-vs-medicare/"),
    (r"Medicare", "/guides/medicaid-vs-medicare/"),
]
LINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")

def process(path):
    text = path.read_text()
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    if not m:
        return 0
    fm, body = m.group(0), text[m.end():]
    permalink = re.search(r"permalink:\s*(\S+)", fm)
    self_url = permalink.group(1).strip('"') if permalink else None
    changes = 0
    for pat, target in TERMS:
        if target == self_url:
            continue
        if target in body:  # already linked somewhere on this page
            continue
        rx = re.compile(r"(?<![\w/\[-])(" + pat + r")(?![\w/-])", re.I if not pat[0].isupper() else 0)
        lines = body.split("\n")
        done = False
        for i, line in enumerate(lines):
            if done or line.startswith("#") or line.startswith("|--"):
                continue
            # protect existing links: replace only in non-link segments
            parts, last, segs = [], 0, []
            for lm in LINK_RE.finditer(line):
                segs.append((last, lm.start(), True)); segs.append((lm.start(), lm.end(), False)); last = lm.end()
            segs.append((last, len(line), True))
            out = []
            for a, b, editable in segs:
                seg = line[a:b]
                if editable and not done:
                    nm = rx.search(seg)
                    if nm:
                        seg = seg[:nm.start()] + "[" + nm.group(1) + "](" + target + ")" + seg[nm.end():]
                        done = True
                out.append(seg)
            lines[i] = "".join(out)
        if done:
            body = "\n".join(lines)
            changes += 1
    if changes:
        path.write_text(fm + body)
    return changes

total = 0
for pattern in ["guides/*.md", "_posts/*.md", "placement-professionals/*.md", "about/index.md", "for-communities/*.md"]:
    for p in sorted(pathlib.Path(".").glob(pattern)):
        n = process(p)
        if n:
            print(f"{p}: {n} terms linked")
            total += n
print("TOTAL new links:", total)
