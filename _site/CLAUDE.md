# senior.living.community

Jekyll static site (Cloudflare Pages). Build with `jekyll build`; layouts in
`_layouts/`, shared partials and inlined CSS in `_includes/`, facility profiles
in `directory/<state>/<county>/<city>/<facility>/index.md`.

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
