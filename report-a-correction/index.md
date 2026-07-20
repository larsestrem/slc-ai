---
layout: page
title: "Report Inaccurate Information"
description: "See something wrong on a community listing? Tell us what's inaccurate and we'll verify and fix it. Community staff can claim and manage the listing instead."
crumbs:
  - name: Report a correction
    url: /report-a-correction/
---

Facility details change constantly - phone numbers, ownership, services, availability - and
we'd rather hear about an error twice than miss it once. Tell us what's wrong and we'll check
it against current sources and correct the listing. Corrections are verified before anything
changes; we never edit a listing on an unverified report alone.

<p class="notice"><strong>Work at this community?</strong> Don't just fix one field - <a href="/for-communities/">claim and manage the listing</a>. It's free, your updates are
published under your name and title, and your profile gets photos, team bios, and your own
answers to what families ask most.</p>

<form class="q-form" method="POST" action="{{ site.forms.endpoint }}" accept-charset="UTF-8">
  <input type="hidden" name="_subject" value="Correction report - listing inaccuracy">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="{{ site.url }}/report-a-correction/thanks/">
  <div class="honey" aria-hidden="true"><label>Leave this field empty<input type="text" name="_honey" tabindex="-1" autocomplete="off"></label></div>

  <fieldset>
    <legend>What's inaccurate?</legend>
    <label for="r-community">Community name &amp; city <span class="opt">(required)</span></label>
    <input type="text" id="r-community" name="Community" required>
    <label for="r-wrong">What's wrong on the listing? <span class="opt">(required)</span></label>
    <p class="hint">The more specific the better - "the phone number rings a different business," "they no longer offer memory care," "the address is the old campus."</p>
    <textarea id="r-wrong" name="What is inaccurate" required></textarea>
    <label for="r-correct">What's the correct information, if you know it?</label>
    <textarea id="r-correct" name="Correct information"></textarea>
    <label for="r-source">Where can we verify it? <span class="opt">(a link, phone number, or how you know)</span></label>
    <input type="text" id="r-source" name="How to verify">
    <label for="r-relation">Your connection to the community <span class="opt">(optional)</span></label>
    <input type="text" id="r-relation" name="Relationship" placeholder="family member, staff, neighbor, just noticed it…">
    <label for="r-email">Your email <span class="opt">(optional - only if you'd like to hear back)</span></label>
    <input type="email" id="r-email" name="Reporter email">
  </fieldset>

  <p><button class="btn" type="submit">Send correction report</button></p>
  <p class="form-foot">Reports go privately to our editors and are verified against current
  sources before any listing changes. See our <a href="/privacy/">Privacy Policy</a>.
  Prefer email? Write <strong>listings@senior.living.community</strong>.</p>
</form>

<script>
/* Prefill the community field from ?community= so profile links land ready to send. */
(function () {
  var v = new URLSearchParams(location.search).get("community");
  var f = document.getElementById("r-community");
  if (v && f && !f.value) f.value = v;
})();
</script>
