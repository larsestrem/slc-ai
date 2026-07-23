# Pre-launch password protection (internal - docs/ is excluded from the site)

The site can be put behind a single shared password so only people you invite can
see it, which is ideal for sharing an in-progress build with outside reviewers.
It is enforced at Cloudflare's edge by `functions/_middleware.js`, so pages are
not served at all without the password (this is real protection, not a JavaScript
gate that leaves the content in the page source).

The gate is controlled entirely by environment variables in the Cloudflare Pages
project - no code change is needed to turn it on or off.

## Turn protection ON (share with reviewers)

1. In Cloudflare: **Workers & Pages > (this project) > Settings > Variables and
   secrets**.
2. Add a variable named **`SITE_PASSWORD`** and set a password (make it a secret).
   Optionally add **`SITE_USERNAME`** (defaults to `review` if you skip it).
3. Set them for the environments you want protected (Production and/or Preview).
4. Redeploy (or trigger a new deployment) so the setting takes effect.
5. Share with reviewers: the site URL, the username (`review` unless you changed
   it), and the password. Their browser will prompt once and remember it for the
   session.

To change the password later, edit `SITE_PASSWORD` and redeploy. To revoke access
for everyone, change it.

## Turn protection OFF (go live)

Delete the **`SITE_PASSWORD`** variable (or set it to empty) in the same settings
screen, then redeploy. With no password configured, the gate passes every request
through and the site is public. Nothing in the repo needs to change.

This is a separate switch from the search-indexing block (`noindex_site` in
`_config.yml`). At go-live you will typically do both: remove `SITE_PASSWORD`
here, and set `noindex_site: false` per `docs/LAUNCH-CHECKLIST.md`.

## Notes

- Because the password lives in Cloudflare (not the repo), it is never committed
  and never appears in the source. The repo only contains the gate logic.
- The gate is dormant until `SITE_PASSWORD` is set. After this code is deployed,
  the site stays public until you set that variable, so set it before sharing any
  link you want kept private.
- This protects the Cloudflare-served site (`*.pages.dev` and the live domain).
  It does not protect the GitHub repository, which has its own access controls.
