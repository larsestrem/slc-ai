/**
 * Pre-launch access gate (Cloudflare Pages Function).
 *
 * While the SITE_PASSWORD environment variable is set in the Cloudflare Pages
 * project, the ENTIRE site is behind HTTP Basic Auth, so only people who have
 * the shared username and password can see it. That makes it safe to share an
 * in-progress build with outside reviewers: send them the URL plus the one
 * shared login.
 *
 * This runs at Cloudflare's edge, so it is real protection - the pages are not
 * served at all without the password (unlike a JavaScript gate, where the
 * content is still in the source).
 *
 * TO OPEN THE SITE AT GO-LIVE: delete the SITE_PASSWORD variable (or set it to
 * empty) in the Cloudflare Pages project. No code change or content redeploy is
 * needed - with no password configured, this gate passes every request through.
 *
 * Environment variables (Cloudflare Pages > Settings > Variables and secrets):
 *   SITE_PASSWORD  Shared password. Unset or empty = site is public (go-live).
 *   SITE_USERNAME  Optional shared username. Defaults to "review".
 *
 * See docs/pre-launch-access.md for step-by-step instructions.
 */
export async function onRequest(context) {
  const { request, env, next } = context;
  const password = (env.SITE_PASSWORD || "").trim();

  // No password configured => the site is open. This is the go-live state.
  if (!password) return next();

  const username = (env.SITE_USERNAME || "review").trim();
  const expected = "Basic " + btoa(username + ":" + password);
  const provided = request.headers.get("Authorization") || "";

  if (provided.length === expected.length && provided === expected) {
    return next();
  }

  return new Response(
    "senior.living.community is not open to the public yet. If you were given a preview password, enter it to continue.",
    {
      status: 401,
      headers: {
        "WWW-Authenticate":
          'Basic realm="senior.living.community - pre-launch preview", charset="UTF-8"',
        "Cache-Control": "no-store",
        "Content-Type": "text/plain; charset=utf-8",
      },
    }
  );
}
