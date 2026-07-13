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
import math
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
            elif key.strip() == "hidden":
                cur["hidden"] = val.strip().lower() == "true" 
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


# Public review platforms — a source URL on one of these domains is a page where
# families can read the actual reviews, so we surface it as a labeled link.
REVIEW_PLATFORMS = [
    ("aplaceformom.com", "A Place for Mom"),
    ("caring.com", "Caring.com"),
    ("senioradvisor.com", "SeniorAdvisor"),
    ("senioradvice.com", "SeniorAdvice"),
    ("seniorcareauthority.com", "Senior Care Authority"),
    ("assistedlivingcenter.com", "AssistedLivingCenter"),
    ("carelistings.com", "CareListings"),
    ("seniorly.com", "Seniorly"),
    ("mycaringplan.com", "My Caring Plan"),
    ("olera.care", "Olera"),
    ("birdeye.com", "Birdeye"),
    ("yelp.com", "Yelp"),
    ("health.usnews.com", "U.S. News"),
    ("g.page", "Google"),
    ("google.com/maps", "Google"),
]


def review_links_from_sources(sources):
    """Map source URLs to labeled links for the review platforms among them."""
    links, seen = [], set()
    for url in sources or []:
        low = url.lower()
        for domain, name in REVIEW_PLATFORMS:
            if domain in low and name not in seen:
                links.append({"name": name, "url": url})
                seen.add(name)
                break
    return links


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


def load_geo():
    path = ROOT / "data" / "geo.json"
    return json.loads(path.read_text()) if path.exists() else {"outlines": {}, "cities": {}}


REGION_PAGE_THRESHOLD = 25  # states with this many facilities get region navigation


def load_regions():
    path = ROOT / "data" / "regions.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data.pop("_comment", None)
    return data


def assign_region(f, state_regions):
    for slug, r in state_regions.items():
        if f["county"] in r["counties"]:
            return slug
    return "other-areas"


def build_map(state, facs, geo, city_region=None, region_colors=None):
    """Inline-SVG state map: simplified outline + one clickable dot per city.

    Equirectangular projection with cos(mid-latitude) x-scaling — fine at state scale.
    Returns front-matter data the state layout renders; no external map service needed.
    """
    outline = geo["outlines"].get(state)
    city_coords = geo["cities"].get(state, {})
    if not outline:
        return None
    lons = [p[0] for p in outline]
    lats = [p[1] for p in outline]
    kx = math.cos(math.radians((min(lats) + max(lats)) / 2))
    width = 340.0
    scale = (width - 24) / ((max(lons) - min(lons)) * kx)
    height = round((max(lats) - min(lats)) * scale + 24, 1)

    def pt(lon, lat):
        return (round(12 + (lon - min(lons)) * kx * scale, 1),
                round(12 + (max(lats) - lat) * scale, 1))

    path = "M" + " L".join(f"{x},{y}" for x, y in (pt(lon, lat) for lon, lat in outline)) + " Z"

    per_city = {}
    for f in facs:
        per_city.setdefault(f["city"], {"name": f["city_name"], "count": 0})
        per_city[f["city"]]["count"] += 1
    dots, missing = [], []
    for slug, info in sorted(per_city.items()):
        if slug not in city_coords:
            missing.append(info["name"])
            continue
        lat, lon = city_coords[slug]
        x, y = pt(lon, lat)
        dot = {"slug": slug, "x": x, "y": y,
               "r": min(6, 3.5 + 0.7 * (info["count"] - 1)),
               "label": f"{info['name']} ({info['count']})"}
        if city_region and slug in city_region:
            dot["region"] = city_region[slug]
            if region_colors:
                dot["color"] = region_colors.get(city_region[slug], 0)
        dots.append(dot)
    if missing:
        print(f"  !! no map coordinates for: {', '.join(missing)} (add to data/geo.json)")
    return {"width": width, "height": height, "outline": path, "dots": dots}


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
        # County/city pages exist (stable URLs for future density) but are
        # intentionally not linked — breadcrumbs jump state → facility.
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": f["state_name"], "url": f"/directory/{f['state']}/"},
            {"name": f["name"], "url": facility_url(f)},
        ],
        "nearby": nearby,
    }
    passthrough = ("state", "state_name", "state_abbrev", "county", "county_name", "city",
                   "city_name", "address", "zip", "phone", "website", "care_levels",
                   "facility_size", "capacity", "organization", "organization_name",
                   "cms_ccn", "cms_rating_overall", "sources", "verified_date",
                   # lifestyle & services — optional, shown when verified
                   "pets", "couples", "min_age", "transportation",
                   "medical_services", "support_services",
                   # media — photos: [{src, alt, caption}], logo: path
                   "photos", "logo",
                   # public review reputation (from search, dated)
                   "google_rating", "google_review_count", "rating_as_of", "review_note",
                   # small-home differentiated quality signals (see SPEC small-home model)
                   "license_id", "licensed_since", "specialties", "quality_basis")
    for k in passthrough:
        if f.get(k) not in (None, "", []):
            front[k] = f[k]
    front["description_full"] = f.get("description")
    rlinks = f.get("review_links") or review_links_from_sources(f.get("sources"))
    if rlinks:
        front["review_links"] = rlinks
    if not f.get("cms_ccn") and licensing:
        front["licensing"] = {"agency": licensing.get("agency"), "lookup_url": licensing.get("lookup_url")}
    write(DIRECTORY / f["state"] / county_slug(f) / f["city"] / f["slug"] / "index.md", fm(front))


def gen_city_page(state, cslug, city_facs):
    f0 = city_facs[0]
    front = {
        "layout": "city",
        "noindex": True,  # thin at seed density; flip when city coverage is real
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
        "noindex": True,  # thin at seed density; flip when county coverage is real
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


def city_blocks_for(facs):
    cities = {}
    for f in facs:
        c = cities.setdefault(f["city"], {"slug": f["city"], "name": f["city_name"],
                                          "counties": set(), "facilities": []})
        c["counties"].add(f["county_name"] + " County")
        c["facilities"].append(f)
    return [
        {"slug": c["slug"], "name": c["name"],
         "county_label": " / ".join(sorted(c["counties"])),
         "facilities": [card(f) for f in sorted(c["facilities"], key=lambda x: x["name"])]}
        for c in sorted(cities.values(), key=lambda c: c["name"])
    ]


def gen_region_page(state, rslug, rname, facs, meta, geo):
    front = {
        "layout": "region",
        "title": f"{rname} Senior Living",
        "seo_title": f"Senior Living in {rname}, {meta['abbrev']} — {len(facs)} Communities",
        "description": f"Compare {len(facs)} senior living communities in {rname}, {meta['name']} — care levels, review evidence, and official inspection links for each.",
        "region_name": rname, "state": state,
        "state_name": meta["name"], "state_abbrev": meta["abbrev"],
        "facility_count": len(facs),
        "cities": city_blocks_for(facs),
        "map": build_map(state, facs, geo),
        "licensing": meta.get("licensing"),
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": meta["name"], "url": f"/directory/{state}/"},
            {"name": rname, "url": f"/directory/{state}/{rslug}/"},
        ],
    }
    write(DIRECTORY / state / rslug / "index.md", fm(front))


def gen_state_page_regions(state, facs, meta, geo, state_regions):
    region_names = {s: r["name"] for s, r in state_regions.items()}
    region_names["other-areas"] = "Other Areas"
    order = list(state_regions.keys()) + ["other-areas"]
    colors = {s: i % 8 for i, s in enumerate(order)}
    by_region, city_region = {}, {}
    for f in facs:
        r = f["_region"]
        by_region.setdefault(r, []).append(f)
        city_region[f["city"]] = r
    region_cards = []
    for rslug in order:
        rl = by_region.get(rslug)
        if not rl:
            continue
        cities = sorted({f["city_name"] for f in rl})
        region_cards.append({
            "slug": rslug, "name": region_names[rslug],
            "url": f"/directory/{state}/{rslug}/",
            "facility_count": len(rl), "color": colors[rslug],
            "city_names": cities[:8] + (["…"] if len(cities) > 8 else []),
        })
        gen_region_page(state, rslug, region_names[rslug], rl, meta, geo)
    level_counts = {}
    for f in facs:
        for lv in f.get("care_levels", []):
            level_counts[lv] = level_counts.get(lv, 0) + 1
    front = {
        "layout": "state",
        "care_level_counts": [{"slug": k, "count": v}
                              for k, v in sorted(level_counts.items(), key=lambda kv: -kv[1])],
        "title": f"{meta['name']} Senior Living",
        "seo_title": f"Senior Living in {meta['name']} — Assisted Living, Memory Care & Nursing Homes",
        "description": f"Find senior living in {meta['name']}: {len(facs)} communities across {len({f['city'] for f in facs})} cities, organized by region with care levels and inspection links.",
        "state_name": meta["name"], "state_abbrev": meta["abbrev"],
        "facility_count": len(facs),
        "regions": region_cards,
        "map": build_map(state, facs, geo, city_region, colors),
        "licensing": meta.get("licensing"),
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": meta["name"], "url": f"/directory/{state}/"},
        ],
    }
    write(DIRECTORY / state / "index.md", fm(front))


def gen_state_page(state, facs, meta, geo):
    # Group directly by city (merged across county lines — Salem spans two counties)
    # so the state page links straight to facilities, no county/city hop.
    cities = {}
    for f in facs:
        c = cities.setdefault(f["city"], {"slug": f["city"], "name": f["city_name"],
                                          "counties": set(), "facilities": []})
        c["counties"].add(f["county_name"] + " County")
        c["facilities"].append(f)
    city_blocks = [
        {"slug": c["slug"], "name": c["name"],
         "county_label": " / ".join(sorted(c["counties"])),
         "facilities": [card(f) for f in sorted(c["facilities"], key=lambda x: x["name"])]}
        for c in sorted(cities.values(), key=lambda c: c["name"])
    ]
    level_counts = {}
    for f in facs:
        for lv in f.get("care_levels", []):
            level_counts[lv] = level_counts.get(lv, 0) + 1
    front = {
        "layout": "state",
        "care_level_counts": [{"slug": k, "count": v}
                              for k, v in sorted(level_counts.items(), key=lambda kv: -kv[1])],
        "title": f"{meta['name']} Senior Living",
        "seo_title": f"Senior Living in {meta['name']} — Assisted Living, Memory Care & Nursing Homes",
        "description": f"Find senior living in {meta['name']}: {len(facs)} communities across {len(cities)} cities, with care levels, sizes, and links to official state inspection records.",
        "state_name": meta["name"], "state_abbrev": meta["abbrev"],
        "facility_count": len(facs),
        "cities": city_blocks,
        "map": build_map(state, facs, geo),
        "licensing": meta.get("licensing"),
        "crumbs": [
            {"name": "Directory", "url": "/directory/"},
            {"name": meta["name"], "url": f"/directory/{state}/"},
        ],
    }
    write(DIRECTORY / state / "index.md", fm(front))


def gen_state(state, states_meta, stats, geo, regions):
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

    state_regions = regions.get(state, {})
    if state_regions and len(facs) >= REGION_PAGE_THRESHOLD:
        for f in facs:
            f["_region"] = assign_region(f, state_regions)
        gen_state_page_regions(state, facs, meta, geo, state_regions)
    else:
        gen_state_page(state, facs, meta, geo)
    if meta.get("hidden"):
        for page in (DIRECTORY / state).rglob("index.md"):
            txt = page.read_text()
            if "\nnoindex:" not in txt:
                page.write_text(txt.replace("---\n", "---\nnoindex: true\n", 1))
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
    geo = load_geo()
    regions = load_regions()
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
            orgs = gen_state(state, states_meta, stats, geo, regions)
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
