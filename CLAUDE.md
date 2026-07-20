# senior.living.community

Jekyll static site (Cloudflare Pages). Build with `jekyll build`; layouts in
`_layouts/`, shared partials and inlined CSS in `_includes/`, facility profiles
in `directory/<state>/<county>/<city>/<facility>/index.md`.

## PRE-LAUNCH: the site is blocked from search indexing (do not remove)

The whole site is deliberately kept out of search results while it's being built.
`noindex_site: true` in `_config.yml` makes every page emit
`<meta name="robots" content="noindex, nofollow">` and makes `robots.txt` disallow all
crawlers. This is intentional and MUST stay until the owner explicitly says the site is
ready to go live.

- **Never** set `noindex_site` to false, or strip the meta/robots block, as a "cleanup" or
  because it looks like a bug. Removing it is a **launch step**, done only on the owner's
  explicit go-live instruction. See `docs/LAUNCH-CHECKLIST.md`.
- Staging lives at `slc-ai.pages.dev`; the live domain will be `senior.living.community`.
- **Reminder rule:** as soon as the owner starts sharing live `senior.living.community`
  links, or otherwise treats the site as live, remind them the noindex/nofollow block is
  still in place and ask whether they're ready to remove it. Keep reminding on each such
  occasion until the owner confirms the site is ready to be indexed. Only then remove the block.

## Content rules (apply to ALL content: pages, front matter, layouts, comments)

- **No long dashes, ever.** Never use em dashes or en dashes in any
  content, code comment, or front matter. Use a plain hyphen, a comma, a colon,
  or split the sentence. Long dashes make content look AI-generated. Number
  ranges use a plain hyphen (5-10 minutes).
- **Voice**: plain-language, warm, and direct. Write like a knowledgeable friend
  helping a family through a stressful decision, not like marketing copy and not
  like AI-ese. No hype words, no hedging filler.
- **We never publish ratings, scores, or characterizations of any facility's
  record.** Profiles link families to primary sources (state licensing records,
  Medicare Care Compare, review platforms). The `records_note` flag only nudges
  readers to check the record; it never says what the record contains.
- **Facility-descriptive content comes only from the facility itself** through
  the verified claiming flow, and edits beyond the basic structured fields
  (record links, review links, licensing data) need the site owner's review
  before publishing.
- Review links must point at reputable pages with genuine review content
  (Google, Yelp, Caring.com, A Place for Mom, SeniorAdvisor, Birdeye, Seniorly).
  No scraper/SEO directories, and no bare listing pages with no reviews.
