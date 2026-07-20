---
layout: page
title: "Listing Questionnaire: The Basics"
description: "Short online questionnaire for senior living communities: building, beds, rooms, and staffing basics. About 5-10 minutes - answers are sent privately to our editors."
crumbs:
  - name: For Communities
    url: /for-communities/
  - name: "Questionnaire: The Basics"
    url: /for-communities/questionnaire-basics/
---

About 5-10 minutes. Fill in what you can and skip anything that doesn't apply or that you'd
rather not publish - partial answers are welcome, and you can come back to any section later.
Your answers are **sent privately to our editors**; nothing is published until we've verified
you with your community.

{% include q-form-start.html subject="Listing questionnaire - The Basics" %}

  <fieldset>
    <legend>The community</legend>
    <label for="b1">Official licensed name <span class="opt">(and the name families know you by, if different)</span></label>
    <input type="text" id="b1" name="Q1 Official licensed name">
    <label for="b2">Year opened, and year of the most recent major renovation</label>
    <input type="text" id="b2" name="Q2 Year opened and renovated">
    <label for="b3">Ownership</label>
    <p class="hint">Independent, family-owned, non-profit, or part of an organization - and which one?</p>
    <input type="text" id="b3" name="Q3 Ownership">
    <label for="b3b">When did the current management team take over?</label>
    <p class="hint">Month/year your current Executive Director or management group began.
    Families weigh this - a community can change a lot under new leadership, for better or worse.</p>
    <input type="text" id="b3b" name="Q3b Current management since">
    <label for="b4">State license number(s) and license type(s)</label>
    <input type="text" id="b4" name="Q4 License numbers and types">
  </fieldset>

  <fieldset>
    <legend>Capacity &amp; rooms</legend>
    <label for="b5">Licensed capacity <span class="opt">(beds/residents)</span></label>
    <input type="text" id="b5" name="Q5 Licensed capacity">
    <label for="b6">Current approximate resident count</label>
    <input type="text" id="b6" name="Q6 Current resident count">
    <label>Room types offered</label>
    <div class="checks">
      <label><input type="checkbox" name="Q7 Room types" value="Private rooms"> Private rooms</label>
      <label><input type="checkbox" name="Q7 Room types" value="Shared/companion rooms"> Shared / companion rooms</label>
      <label><input type="checkbox" name="Q7 Room types" value="Studios"> Studios</label>
      <label><input type="checkbox" name="Q7 Room types" value="One-bedrooms"> One-bedrooms</label>
      <label><input type="checkbox" name="Q7 Room types" value="Two-bedrooms"> Two-bedrooms</label>
      <label><input type="checkbox" name="Q7 Room types" value="Cottages"> Cottages</label>
    </div>
    <label for="b8">Approximate square footage of your most common room type(s)</label>
    <input type="text" id="b8" name="Q8 Square footage of common room types">
    <label for="b9">Do rooms have private bathrooms? Kitchenettes?</label>
    <input type="text" id="b9" name="Q9 Private bathrooms and kitchenettes">
  </fieldset>

  <fieldset>
    <legend>Building &amp; grounds</legend>
    <label for="b10">Total building square footage <span class="opt">(approximate is fine)</span></label>
    <input type="text" id="b10" name="Q10 Building square footage">
    <label for="b11">Number of floors; elevator available?</label>
    <input type="text" id="b11" name="Q11 Floors and elevator">
    <label for="b12">Outdoor spaces</label>
    <p class="hint">Courtyard, gardens, walking paths, secured outdoor area for <a href="/guides/memory-care/">memory care</a>?</p>
    <textarea id="b12" name="Q12 Outdoor spaces"></textarea>
  </fieldset>

  <fieldset>
    <legend>Staffing</legend>
    <label for="b13">Total staff count <span class="opt">(approximate)</span></label>
    <input type="text" id="b13" name="Q13 Total staff count">
    <label for="b14">Caregiving staff on duty during the day vs overnight</label>
    <p class="hint">Families ask this constantly.</p>
    <input type="text" id="b14" name="Q14 Caregivers day vs overnight">
    <label for="b15">Nursing coverage</label>
    <p class="hint">Is a nurse on site 24/7, on site during business hours, or on call? RN or LPN?</p>
    <input type="text" id="b15" name="Q15 Nursing coverage">
  </fieldset>

{% include q-form-end.html %}

When you're ready for the next section:
**[Care & services →](/for-communities/questionnaire-care/)**
