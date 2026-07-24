---
layout: page
title: "Add a Community"
description: "Know a senior living community that's not in our directory? Tell us and we'll add it. Anyone can suggest one; if you work there, you can fill in the full profile too."
crumbs:
  - name: Add a Community
    url: /add-a-facility/
---

Know a senior living community that isn't listed here? Tell us about it and we'll add it. You
don't need to work there, and it only takes a minute. If you'd like, we'll let you know once the
listing is live.

**Work at or manage this community?** Even better - you're the best possible source. Check the box
in the form and we'll help you fill in the details families most want to see: care levels and bed
counts, services, staffing, photos, and how you handle concerns.

<form class="q-form" method="POST" action="{{ site.forms.endpoint }}" accept-charset="UTF-8">
  <input type="hidden" name="_subject" value="Add a community - suggestion">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="{{ site.url }}/for-communities/thank-you/">
  <div class="honey" aria-hidden="true"><label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>

  <fieldset>
    <legend>The community</legend>
    <label for="f-name">Community name <span class="opt">(required)</span></label>
    <input type="text" id="f-name" name="Community name" required autocomplete="organization">
    <label for="f-loc">City &amp; state <span class="opt">(required)</span></label>
    <input type="text" id="f-loc" name="Community city and state" required>
    <label for="f-addr">Street address <span class="opt">(if you have it)</span></label>
    <input type="text" id="f-addr" name="Street address">
    <label for="f-phone">Phone</label>
    <input type="tel" id="f-phone" name="Phone" autocomplete="tel">
    <label for="f-web">Website</label>
    <input type="url" id="f-web" name="Website" placeholder="https://">
    <label>Care levels offered <span class="opt">(check any you know of)</span></label>
    <div class="checks">
      <label><input type="checkbox" name="Care levels" value="Independent living"> Independent living</label>
      <label><input type="checkbox" name="Care levels" value="Assisted living"> Assisted living</label>
      <label><input type="checkbox" name="Care levels" value="Memory care"> Memory care</label>
      <label><input type="checkbox" name="Care levels" value="Skilled nursing"> Skilled nursing</label>
      <label><input type="checkbox" name="Care levels" value="Respite / short stays"> Respite / short stays</label>
      <label><input type="checkbox" name="Care levels" value="Small care home / adult family home"> Small care home / adult family home</label>
    </div>
  </fieldset>

  <fieldset>
    <legend>You</legend>
    <label for="f-you">Your name <span class="opt">(required)</span></label>
    <input type="text" id="f-you" name="Your name" required autocomplete="name">
    <label for="f-email">Your email <span class="opt">(required, so we can follow up)</span></label>
    <input type="email" id="f-email" name="Your email" required autocomplete="email">

    <div class="reveal-item">
      <input type="checkbox" id="f-works" class="reveal" name="I work at this community" value="Yes">
      <label for="f-works" class="reveal-label">I work at or help manage this community</label>
      <div class="reveal-target">
        <p class="hint">Great - as verified staff you can tell families what public sources can't.
        Add your role and a work email below and we'll start the quick verification, then send you
        the short listing questionnaires so you can fill in care levels and bed counts, services,
        staffing, photos, and how you handle concerns.</p>
        <label for="f-role">Your title / role</label>
        <input type="text" id="f-role" name="Your title" autocomplete="organization-title">
        <label for="f-workemail">Work email <span class="opt">(at the community's domain, so we can verify you)</span></label>
        <input type="email" id="f-workemail" name="Work email at community domain">
        <p class="hint">Want to get a head start now? See <a href="/for-communities/">how claiming
        works</a> and the <a href="/for-communities/questionnaire-basics/">listing questionnaires</a>.</p>
      </div>
    </div>
  </fieldset>

  <p><button class="btn" type="submit">Send this to our editors</button></p>
  <p class="form-foot">Your suggestion goes privately to our editors by email. We verify a
  community and its basic facts before it's published, and nothing you mark as staff-provided
  appears until we've verified you. Prefer email? Send the details to
  <strong>listings@senior.living.community</strong> instead. See our <a href="/privacy/">Privacy
  Policy</a>.</p>
</form>
