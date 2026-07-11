#!/usr/bin/env python3
"""
Merge a research batch file into the per-state facility JSON files.

Batch format: {"facilities": [...], "organizations": [...]} — same schema as
data/facilities/<state>.json, but may span multiple states. Facilities are
deduped by slug (and by CMS CCN when present); organizations by slug.

  python3 scripts/merge_batch.py path/to/batch.json [--dry-run]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "facilities"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)
    batch = json.loads(Path(args[0]).read_text())

    by_state = {}
    for f in batch.get("facilities", []):
        by_state.setdefault(f["state"], []).append(f)

    for state, incoming in sorted(by_state.items()):
        path = DATA / f"{state}.json"
        payload = json.loads(path.read_text()) if path.exists() else {"facilities": [], "organizations": []}
        slugs = {f["slug"] for f in payload["facilities"]}
        ccns = {f["cms_ccn"] for f in payload["facilities"] if f.get("cms_ccn")}
        added = skipped = 0
        for f in incoming:
            if f["slug"] in slugs or (f.get("cms_ccn") and f["cms_ccn"] in ccns):
                skipped += 1
                continue
            payload["facilities"].append(f)
            slugs.add(f["slug"])
            if f.get("cms_ccn"):
                ccns.add(f["cms_ccn"])
            added += 1
        org_slugs = {o["slug"] for o in payload["organizations"]}
        org_added = 0
        for o in batch.get("organizations", []):
            states_field = o.get("states") or []
            if o["slug"] in org_slugs:
                continue
            # attach org to the state file of any facility that references it
            if any(f.get("organization") == o["slug"] for f in payload["facilities"]) or state.upper()[:2] in states_field:
                payload["organizations"].append(o)
                org_slugs.add(o["slug"])
                org_added += 1
        print(f"{state}: +{added} facilities ({skipped} duplicates skipped), +{org_added} orgs → {len(payload['facilities'])} total")
        if not dry:
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
