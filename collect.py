#!/usr/bin/env python3
"""
Build an unlabelled labels.csv from collected r/csmajors comments.

    python collect.py --sample 240 RAW1.json [RAW2.json ...]

Each RAW file is a list of {"text", "author", "link", "source"} dicts, from
either the PullPush archive or Reddit's public RSS feeds. This merges them,
drops what isn't a take anyone wrote, de-duplicates, and writes:

    labels.csv            text,label,note   (label and note left blank to fill in)
    notes/sources.csv     the same rows with author-free provenance: link, source
    notes/pool.csv        every kept comment that wasn't sampled, for topping up
                          a thin label later

--sample takes the same number from each thread, round-robin, so no single
thread decides what the dataset sounds like. Seeded, so it's repeatable.

Nothing here labels anything.
"""

import argparse
import csv
import json
import random
import re

MIN_CHARS = 40       # shorter than this is "lol", "same", "congrats"
MAX_CHARS = 1500     # the notebook truncates at 128 tokens anyway; walls of text
                     # would mostly be cut off

BOT = re.compile(r"I am a bot|LLM-powered bot|AutoModerator|was identified as something likely to violate",
                 re.IGNORECASE)
COMMENT_LINK = re.compile(r"/comments/\w+/[^/]*/\w+/?$")


def clean(text: str) -> str:
    text = text.replace("\r", "")
    text = re.sub(r"https?://preview\.redd\.it\S+", "", text)   # pasted image links
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def mostly_english(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and sum(c.isascii() for c in letters) / len(letters) > 0.9


def keep(row: dict) -> str | None:
    """Why a row is dropped, or None to keep it."""
    text = row["text"]
    if text in ("[removed]", "[deleted]"):
        return "removed"
    if "automoderator" in row.get("author", "").lower() or BOT.search(text):
        return "bot"
    if row.get("link") and "reddit.com" in row["link"] and not COMMENT_LINK.search(row["link"]):
        return "the thread's own post, not a comment"
    if not mostly_english(text):
        return "not English"
    if len(text) < MIN_CHARS:
        return f"under {MIN_CHARS} chars"
    if len(text) > MAX_CHARS:
        return f"over {MAX_CHARS} chars"
    if not re.sub(r"https?://\S+", "", text).strip():
        return "only a link"
    return None


def sample_evenly(rows: list[dict], n: int, seed: int = 0) -> tuple[list[dict], list[dict]]:
    """Round-robin across sources, shuffled within each, until n are picked."""
    rng = random.Random(seed)
    groups = {}
    for row in rows:
        groups.setdefault(row.get("source", ""), []).append(row)
    for group in groups.values():
        rng.shuffle(group)
    picked = []
    while len(picked) < n and any(groups.values()):
        for source in sorted(groups):
            if groups[source] and len(picked) < n:
                picked.append(groups[source].pop())
    rest = [row for group in groups.values() for row in group]
    rng.shuffle(picked)
    return picked, rest


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main(paths, n):
    raw = []
    for path in paths:
        raw += json.load(open(path, encoding="utf-8"))

    kept, seen, dropped = [], set(), {}
    for row in raw:
        row = {**row, "text": clean(row["text"])}
        why = keep(row)
        key = re.sub(r"\W+", " ", row["text"].lower()).strip()
        if why is None and key in seen:
            why = "duplicate"
        if why:
            dropped[why] = dropped.get(why, 0) + 1
            continue
        seen.add(key)
        kept.append(row)

    picked, rest = sample_evenly(kept, n) if n else (kept, [])

    write("labels.csv", ["text", "label", "note"], [[r["text"], "", ""] for r in picked])
    write("notes/sources.csv", ["row", "link", "source"],
          [[i, r.get("link", ""), r.get("source", "")] for i, r in enumerate(picked, 1)])
    write("notes/pool.csv", ["text", "link", "source"],
          [[r["text"], r.get("link", ""), r.get("source", "")] for r in rest])

    print(f"{len(raw)} collected, {len(kept)} kept, {len(picked)} sampled into labels.csv, "
          f"{len(rest)} left in notes/pool.csv")
    for why, n in sorted(dropped.items(), key=lambda kv: -kv[1]):
        print(f"  dropped {n:3}  {why}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", nargs="+")
    parser.add_argument("--sample", type=int, default=0, help="rows for labels.csv (0 = all)")
    args = parser.parse_args()
    main(args.raw, args.sample)
