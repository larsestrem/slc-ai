#!/usr/bin/env python3
"""
senior.living.community page generator.

The folder structure IS the directory: this script turns per-state facility JSON
(data/facilities/<state>.json) into Jekyll pages under directory/<state>/<county>-county/
<city>/<facility>/ plus organization pages and _data/stats.yml. All data is baked into
front matter, so Jekyll templates never scan collections — builds stay fast at scale.

Rebuild scoping (the whole point):
  python3 scripts/generate.py --all                      # every state
  python3 scripts/generate.py --state oregon             # one state's tree
  python3 scripts/generate.py --city oregon/portland     # one city (+ its county/state indexes)

A state or city regen rewrites only files under its own subtree (plus the shared
organization pages and stats file, which aggregate across states).

Data refresh: scripts/fetch_cms.py merges current CMS Care Compare records into the
state JSON files; re-run this script afterward for the affected states.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "facilities"
DIRECTORY = ROOT / "directory"
ORGS = ROOT / "organizations"

try:
    import yaml  # optional, only used to read _data/states.yml
except ImportError:
    yaml = None


def read_states_meta():
    """Licensing metadata per state from _data/states.yml (tiny hand-rolled parse if no PyYAML)."""
    path = ROOT / "_data" / "states.yml"
    if yaml:
        return {s["slug"]: s for s in yaml.safe_load(path.read_text())}
    states, cur = {}, None
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("- slug:"):
            cur = {"slug": stripped.split(":", 1)[1].strip()}
            states[cur["slug"]] = cur
        elif cur is not None and ":" in stripped and not stripped.startswith("#"):
            key, val = stripped.split(":", 1)
            val = val.strip().strip('"')
            if key.strip() == "licensing":
                cur["licensing"] = {}
            elif "licensing" in cur and key.strip() in ("agency", "lookup_url", "small_home", "note"):
                cur["licensing"][key.strip()] = val
            elif key.strip() in ("name", "abbrev"):
                cur[key.strip()] = val
    return states


def fm(data: dict, body: str = "") -> str:
    """Render front matter + body. Values are JSON-encoded (JSON is valid YAML)."""
    lines = ["---"]
    for k, v in data.items():
        if v is None:
            continue
        lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + ("\n" + body + "\n" if body else "\n")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def county_slug(f):
    return f["county"] if f["county"].endswith("-county") else f["county"] + "-county"


def facility_url(f):
    return f"/directory/{f['state']}/{county_slug(f)}/{f['city']}/{f['slug']}/"


def card(f):
    """The subset of fields a facility card include needs."""
    c = {
        "name": f["name"], "url": facility_url(f),
        "city_name": f["city_name"], "state_abbrev": f["state_abbrev"],
        "care_levels": f.get("care_levels", []),
    }
    for k in ("facility_size", "cms_rating_overall", "description"):
        if f.get(k):
            c[k] = f[k]
    return c


def load_state(slug):
    path = DATA / f"{slug}.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    return payload.get("facilities", []), payload.get("organizations", [])


def gen_facility_page(f, siblings, licensing):
    nearby = [card(s) for s in siblings if s["slug"] != f["slug"]][:6]
    front = {
        "layout": "facility",
        "title": f["name"],
        "seo_title": f"{f['name']} — Senior Living in {f['city_name']}, {f['state_abbrev']}",
        "description": (f.get("description") or
                        f"{f['name']} in {f['city_name']}, {f['state_name']}: care levels, contact details, and official inspection records.")[:158],
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": f["state_name"], "url": f"/directory/{f['state']}/"},
            {"name": f["county_name"] + " County", "url": f"/directory/{f['state']}/{county_slug(f)}/"},
            {"name": f["city_name"], "url": f"/directory/{f['state']}/{county_slug(f)}/{f['city']}/"},
            {"name": f["name"], "url": facility_url(f)},
        ],
        "nearby": nearby,
    }
    passthrough = ("state", "state_name", "state_abbrev", "county", "county_name", "city",
                   "city_name", "address", "zip", "phone", "website", "care_levels",
                   "facility_size", "capacity", "organization", "organization_name",
                   "cms_ccn", "cms_rating_overall", "sources", "verified_date")
    for k in passthrough:
        if f.get(k) not in (None, "", []):
            front[k] = f[k]
    front["description_full"] = f.get("description")
    if not f.get("cms_ccn") and licensing:
        front["licensing"] = {"agency": licensing.get("agency"), "lookup_url": licensing.get("lookup_url")}
    write(DIRECTORY / f["state"] / county_slug(f) / f["city"] / f["slug"] / "index.md", fm(front))


def gen_city_page(state, cslug, city_facs):
    f0 = city_facs[0]
    front = {
        "layout": "city",
        "title": f"Senior Living in {f0['city_name']}, {f0['state_abbrev']}",
        "seo_title": f"Senior Living in {f0['city_name']}, {f0['state_abbrev']} — Assisted Living, Memory Care & More",
        "description": f"Compare {len(city_facs)} senior living communities in {f0['city_name']}, {f0['state_name']}: care levels, sizes, and official inspection records for each.",
        "city_name": f0["city_name"], "county_name": f0["county_name"],
        "state_name": f0["state_name"], "state_abbrev": f0["state_abbrev"],
        "facility_count": len(city_facs),
        "facilities": [card(f) for f in sorted(city_facs, key=lambda x: x["name"])],
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": f0["state_name"], "url": f"/directory/{state}/"},
            {"name": f0["county_name"] + " County", "url": f"/directory/{state}/{cslug}/"},
            {"name": f0["city_name"], "url": f"/directory/{state}/{cslug}/{f0['city']}/"},
        ],
    }
    write(DIRECTORY / state / cslug / f0["city"] / "index.md", fm(front))


def gen_county_page(state, cslug, county_facs):
    f0 = county_facs[0]
    cities = {}
    for f in county_facs:
        cities.setdefault(f["city"], []).append(f)
    city_blocks = [
        {"slug": cs, "name": fl[0]["city_name"],
         "url": f"/directory/{state}/{cslug}/{cs}/",
         "facilities": [card(f) for f in sorted(fl, key=lambda x: x["name"])]}
        for cs, fl in sorted(cities.items())
    ]
    front = {
        "layout": "county",
        "title": f"{f0['county_name']} County, {f0['state_abbrev']} Senior Living",
        "seo_title": f"Senior Living in {f0['county_name']} County, {f0['state_abbrev']} — {len(county_facs)} Communities",
        "description": f"Senior living in {f0['county_name']} County, {f0['state_name']}: {len(county_facs)} communities across {len(cities)} cities, with care levels and inspection links.",
        "county_name": f0["county_name"], "state_name": f0["state_name"],
        "state_abbrev": f0["state_abbrev"], "facility_count": len(county_facs),
        "cities": city_blocks,
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": f0["state_name"], "url": f"/directory/{state}/"},
            {"name": f0["county_name"] + " County", "url": f"/directory/{state}/{cslug}/"},
        ],
    }
    write(DIRECTORY / state / cslug / "index.md", fm(front))


def gen_state_page(state, facs, meta):
    counties = {}
    for f in facs:
        counties.setdefault(county_slug(f), []).append(f)
    county_rows = []
    for cslug, fl in sorted(counties.items()):
        city_names = sorted({f["city_name"] for f in fl})
        county_rows.append({
            "slug": cslug, "name": fl[0]["county_name"],
            "url": f"/directory/{state}/{cslug}/",
            "facility_count": len(fl), "city_names": city_names,
        })
    front = {
        "layout": "state",
        "title": f"{meta['name']} Senior Living",
        "seo_title": f"Senior Living in {meta['name']} — Assisted Living, Memory Care & Nursing Homes",
        "description": f"Find senior living in {meta['name']}: {len(facs)} communities by county and city, with care levels, sizes, and links to official state inspection records.",
        "state_name": meta["name"], "state_abbrev": meta["abbrev"],
        "facility_count": len(facs),
        "counties": county_rows,
        "licensing": meta.get("licensing"),
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": meta["name"], "url": f"/directory/{state}/"},
        ],
    }
    write(DIRECTORY / state / "index.md", fm(front))


def gen_state(state, states_meta, stats):
    loaded = load_state(state)
    if loaded is None:
        print(f"  !! no data file for {state} (data/facilities/{state}.json) — skipped")
        return None
    facs, orgs = loaded
    meta = states_meta.get(state) or {"name": state.title(), "abbrev": state[:2].upper()}
    licensing = meta.get("licensing")

    # Clean the state's subtree so removed facilities don't leave stale pages.
    state_dir = DIRECTORY / state
    if state_dir.exists():
        shutil.rmtree(state_dir)

    counties = {}
    for f in facs:
        counties.setdefault(county_slug(f), {}).setdefault(f["city"], []).append(f)

    for cslug, cities in counties.items():
        county_facs = [f for fl in cities.values() for f in fl]
        gen_county_page(state, cslug, county_facs)
        for _, city_facs in cities.items():
            gen_city_page(state, cslug, city_facs)
            for f in city_facs:
                gen_facility_page(f, city_facs, licensing)

    gen_state_page(state, facs, meta)
    stats["states"][state] = {
        "facilities": len(facs),
        "cities": len({(f["county"], f["city"]) for f in facs}),
        "counties": len(counties),
    }
    print(f"  {state}: {len(facs)} facilities, {stats['states'][state]['cities']} cities, {len(counties)} counties")
    return orgs


def gen_organizations(all_orgs, facilities_by_org, org_names):
    merged = {}
    for o in all_orgs:
        cur = merged.setdefault(o["slug"], {})
        for k, v in o.items():
            if k not in cur or (k == "description" and len(str(v)) > len(str(cur.get(k, "")))):
                cur[k] = v
    # Stub pages for operators referenced by facilities but not described in any
    # state file — the facility link must never 404.
    for slug, name in org_names.items():
        merged.setdefault(slug, {"slug": slug, "name": name})
    if ORGS.exists():
        for child in ORGS.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
    index_cards = []
    for slug, o in sorted(merged.items()):
        facs = sorted(facilities_by_org.get(slug, []), key=lambda c: c["name"])
        front = {
            "layout": "organization",
            "title": o["name"],
            "seo_title": f"{o['name']} — Senior Living Communities & Locations",
            "description": (o.get("description") or f"{o['name']} senior living communities: locations in our directory, company facts, and how to evaluate each community.")[:158],
            "org_description": o.get("description"),
            "headquarters": o.get("headquarters"),
            "website": o.get("website"),
            "facility_count_approx": o.get("facility_count_approx"),
            "org_states": o.get("states"),
            "facilities": facs,
            "crumbs": [
                {"name": "Organizations", "url": "/organizations/"},
                {"name": o["name"], "url": f"/organizations/{slug}/"},
            ],
        }
        write(ORGS / slug / "index.md", fm(front))
        index_cards.append({"name": o["name"], "url": f"/organizations/{slug}/",
                            "count_here": len(facs), "headquarters": o.get("headquarters")})
    front = {
        "layout": "default",
        "title": "Senior Living Organizations & Operators",
        "description": "Multi-community senior living operators: who runs which communities, at what scale, and how to judge an operator when choosing a community.",
        "orgs": index_cards,
        "crumbs": [{"name": "Organizations", "url": "/organizations/"}],
    }
    body = """<h1>Senior Living Organizations</h1>
<p class="lead">Many communities belong to multi-state operators. Company policy shapes pricing,
staffing, and care assessments — but quality still varies building to building.</p>
<ul class="grid">
{% for o in page.orgs %}<li class="card"><h3><a href="{{ o.url }}">{{ o.name }}</a></h3>
<p class="meta">{% if o.headquarters %}{{ o.headquarters }} · {% endif %}{{ o.count_here }} in our directory</p></li>
{% endfor %}</ul>
<p class="notice">Judge each community on its own <a href="/guides/reading-inspection-reports-and-ratings/">inspection record</a> — an operator's brand is a starting point, not an answer.</p>"""
    write(ORGS / "index.html", fm(front, body))
    print(f"  organizations: {len(merged)} pages")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="regenerate every state with a data file")
    ap.add_argument("--state", action="append", default=[], help="state slug to regenerate (repeatable)")
    ap.add_argument("--city", action="append", default=[], help="state/city-slug to regenerate one city subtree")
    args = ap.parse_args()

    states_meta = read_states_meta()
    if args.all:
        targets = sorted(p.stem for p in DATA.glob("*.json"))
    else:
        targets = list(args.state)
        for spec in args.city:
            targets.append(spec.split("/")[0])  # city regen = state regen (cheap, always consistent)
    targets = sorted(set(targets))
    if not targets:
        ap.error("nothing to do — pass --all, --state <slug>, or --city <state>/<city>")

    stats_path = ROOT / "_data" / "stats.yml"
    stats = {"states": {}}
    if stats_path.exists():
        if yaml:
            stats = yaml.safe_load(stats_path.read_text()) or {"states": {}}
        else:  # crude reload: regen all known states to keep stats truthful
            targets = sorted(set(targets) | {p.stem for p in DATA.glob("*.json")})

    print("Generating:", ", ".join(targets))
    all_orgs, facilities_by_org, org_names = [], {}, {}
    for state in sorted(set(p.stem for p in DATA.glob("*.json"))):
        if state in targets:
            orgs = gen_state(state, states_meta, stats)
            if orgs is None:
                continue
        else:
            loaded = load_state(state)
            if loaded is None:
                continue
            orgs = loaded[1]
        facs, _ = load_state(state)
        for f in facs:
            if f.get("organization"):
                facilities_by_org.setdefault(f["organization"], []).append(card(f))
                org_names.setdefault(f["organization"], f.get("organization_name") or f["organization"].replace("-", " ").title())
        all_orgs.extend(orgs or [])

    gen_organizations(all_orgs, facilities_by_org, org_names)

    total = {"facilities": sum(s["facilities"] for s in stats["states"].values()),
             "cities": sum(s["cities"] for s in stats["states"].values()),
             "counties": sum(s["counties"] for s in stats["states"].values())}
    out = ["# Generated by scripts/generate.py — do not edit by hand", "total:"]
    out += [f"  {k}: {v}" for k, v in total.items()]
    out.append("states:")
    for slug, s in sorted(stats["states"].items()):
        out.append(f"  {slug}:")
        out += [f"    {k}: {v}" for k, v in s.items()]
    write(stats_path, "\n".join(out) + "\n")
    print(f"Done. Totals: {total['facilities']} facilities / {total['cities']} cities / {total['counties']} counties.")


if __name__ == "__main__":
    sys.exit(main())
