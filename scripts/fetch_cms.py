#!/usr/bin/env python3
"""
Pull current CMS Care Compare nursing-home data and merge it into the per-state
facility JSON files (data/facilities/<state>.json).

CMS publishes the "Provider Information" dataset (id 4pq5-n9py) — every
Medicare/Medicaid-certified nursing home in the country, refreshed monthly:
name, address, county, phone, certified beds, ownership, and the Five-Star
ratings (overall, health inspection, staffing, quality measures).
Docs: https://data.cms.gov/provider-data/dataset/4pq5-n9py

NOTE: requires normal internet access (data.cms.gov is blocked in some sandboxed
CI environments). Run from a regular machine:

  python3 scripts/fetch_cms.py --states OR CA WA NV ID
  python3 scripts/generate.py --all

Merge behavior:
- Facilities are matched by CMS CCN (cms_ccn). Existing hand-verified records
  gain/refresh rating fields; new CMS facilities are added as new records.
- CMS covers ONLY skilled nursing facilities. Assisted living, memory care, and
  small care homes come from state licensing exports (see README) or manual
  verification — this script never touches non-CMS records.
"""
import argparse
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "facilities"
DATASET = "4pq5-n9py"
META_URL = f"https://data.cms.gov/provider-data/api/1/metastore/schemas/dataset/items/{DATASET}?show-reference-ids"

STATE_NAMES = {"OR": ("oregon", "Oregon"), "CA": ("california", "California"),
               "WA": ("washington", "Washington"), "NV": ("nevada", "Nevada"),
               "ID": ("idaho", "Idaho")}


def slugify(s):
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


def fetch_csv_url():
    with urllib.request.urlopen(META_URL, timeout=60) as r:
        meta = json.load(r)
    for dist in meta.get("distribution", []):
        url = (dist.get("data") or {}).get("downloadURL")
        if url and url.endswith(".csv"):
            return url
    raise SystemExit("No CSV distribution found in dataset metadata")


def pick(row, *names):
    for n in names:
        for key in row:
            if key.lower().replace("_", " ").strip() == n:
                return row[key].strip()
    return ""


def row_to_facility(row, state_slug, state_name):
    name = pick(row, "provider name")
    city = pick(row, "city/town", "provider city", "city")
    county = pick(row, "county/parish", "provider county name", "county")
    fac = {
        "name": name.title() if name.isupper() else name,
        "slug": slugify(name),
        "state": state_slug, "state_name": state_name,
        "state_abbrev": pick(row, "state", "provider state"),
        "county": slugify(county), "county_name": county.title() if county.isupper() else county,
        "city": slugify(city), "city_name": city.title() if city.isupper() else city,
        "address": pick(row, "provider address", "address"),
        "zip": pick(row, "zip code", "provider zip code"),
        "phone": pick(row, "telephone number", "provider phone number"),
        "care_levels": ["skilled-nursing"],
        "cms_ccn": pick(row, "cms certification number (ccn)", "federal provider number"),
        "sources": [f"https://www.medicare.gov/care-compare/details/nursing-home/{pick(row, 'cms certification number (ccn)', 'federal provider number')}"],
    }
    beds = pick(row, "number of certified beds")
    if beds.isdigit():
        fac["capacity"] = int(beds)
        fac["facility_size"] = "small" if int(beds) <= 10 else ("medium" if int(beds) <= 60 else "large")
    rating = pick(row, "overall rating")
    if rating.isdigit():
        fac["cms_rating_overall"] = int(rating)
    return fac


def merge(state_slug, state_name, cms_facilities, apply_changes):
    path = DATA / f"{state_slug}.json"
    payload = {"facilities": [], "organizations": []}
    if path.exists():
        payload = json.loads(path.read_text())
    by_ccn = {f["cms_ccn"]: f for f in payload["facilities"] if f.get("cms_ccn")}
    updated = added = 0
    for cf in cms_facilities:
        existing = by_ccn.get(cf["cms_ccn"])
        if existing:
            for k in ("cms_rating_overall", "capacity", "phone", "address", "zip"):
                if cf.get(k):
                    existing[k] = cf[k]
            updated += 1
        else:
            payload["facilities"].append(cf)
            added += 1
    print(f"{state_slug}: {updated} updated, {added} added ({len(payload['facilities'])} total)")
    if apply_changes:
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--states", nargs="+", required=True, help="state abbreviations, e.g. OR CA WA NV ID")
    ap.add_argument("--dry-run", action="store_true", help="report changes without writing")
    args = ap.parse_args()

    csv_url = fetch_csv_url()
    print(f"Downloading {csv_url} ...")
    with urllib.request.urlopen(csv_url, timeout=300) as r:
        text = r.read().decode("utf-8-sig", errors="replace")

    wanted = {s.upper() for s in args.states}
    by_state = {}
    for row in csv.DictReader(io.StringIO(text)):
        st = pick(row, "state", "provider state").upper()
        if st in wanted and st in STATE_NAMES:
            slug, name = STATE_NAMES[st]
            by_state.setdefault(st, []).append(row_to_facility(row, slug, name))

    for st in sorted(wanted):
        slug, name = STATE_NAMES[st]
        merge(slug, name, by_state.get(st, []), apply_changes=not args.dry_run)
    print("Now run: python3 scripts/generate.py --state " + " --state ".join(STATE_NAMES[s][0] for s in sorted(wanted)))


if __name__ == "__main__":
    sys.exit(main())
