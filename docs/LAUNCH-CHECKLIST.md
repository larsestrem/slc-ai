# Launch checklist (internal - docs/ is excluded from the built site)

The site is intentionally blocked from search indexing until the owner says go. Do not
remove the block as a cleanup - it comes off only as a deliberate launch step.

## The indexing block, and how it comes off

While `noindex_site: true` in `_config.yml`:

- every page renders `<meta name="robots" content="noindex, nofollow">` (see `_includes/head.html`)
- `robots.txt` serves `Disallow: /` for all user-agents (see `robots.txt`)

**To go live (owner's explicit instruction only):**

1. Set `noindex_site: false` in `_config.yml` (or delete the line).
2. Rebuild and confirm:
   - page source no longer contains `noindex`
   - `/robots.txt` now shows `Allow: /` and the `Sitemap:` line
3. Point the `senior.living.community` domain at the Cloudflare Pages project.
4. Verify `url:` in `_config.yml` is `https://senior.living.community` (already set).
5. Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
6. Spot-check that canonical URLs and Open Graph URLs resolve on the live domain.

## Reminder rule for any assistant working on this repo

As soon as the owner shares live `senior.living.community` links or treats the site as
live, remind them the noindex/nofollow block is still in place and ask if they want it
removed. Keep reminding until they confirm the site is ready to be indexed.
