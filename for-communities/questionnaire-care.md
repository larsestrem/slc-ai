---
layout: page
title: "Listing Questionnaire: Care & Services"
description: "Short online questionnaire for senior living communities: care levels, medical and non-medical services, pets, couples, and age policies. About 10 minutes - answers are sent privately to our editors."
crumbs:
  - name: For Communities
    url: /for-communities/
  - name: "Questionnaire: Care & Services"
    url: /for-communities/questionnaire-care/
---

About 10 minutes. Fill in what you can and skip anything that doesn't apply - partial answers
are welcome. Your answers are **sent privately to our editors**; nothing is published until
we've verified you with your community.

{% include q-form-start.html subject="Listing questionnaire - Care & Services" %}

  <fieldset class="care-picker">
    <legend>Care levels &amp; beds</legend>
    <p class="hint">Check each care level you offer. Selecting one opens a short section for that
    level, starting with how many beds or units it has. Fill in what you know and skip the rest.</p>

    <div class="care-item">
      <input type="checkbox" id="care-il" class="care-toggle" name="Q1 Care levels" value="Independent living">
      <label for="care-il" class="care-toggle-label"><a href="/guides/independent-living/">Independent living</a></label>
      <div class="care-detail">
        <label for="il-units">Independent living: number of units</label>
        <input type="number" id="il-units" name="Independent living units" min="0" inputmode="numeric">
        <label for="il-types">Home types and how many of each <span class="opt">(optional)</span></label>
        <p class="hint">For example: 40 apartments, 20 cottages, 12 garden homes.</p>
        <textarea id="il-types" name="Independent living home types"></textarea>
      </div>
    </div>

    <div class="care-item">
      <input type="checkbox" id="care-al" class="care-toggle" name="Q1 Care levels" value="Assisted living">
      <label for="care-al" class="care-toggle-label"><a href="/guides/assisted-living/">Assisted living</a></label>
      <div class="care-detail">
        <label for="al-beds">Assisted living: licensed beds or apartments</label>
        <input type="number" id="al-beds" name="Assisted living beds" min="0" inputmode="numeric">
        <label for="al-types">Apartment types and how many of each <span class="opt">(optional)</span></label>
        <p class="hint">For example: 20 studio, 30 one-bedroom, 8 two-bedroom.</p>
        <textarea id="al-types" name="Assisted living apartment types"></textarea>
      </div>
    </div>

    <div class="care-item">
      <input type="checkbox" id="care-mc" class="care-toggle" name="Q1 Care levels" value="Memory care">
      <label for="care-mc" class="care-toggle-label"><a href="/guides/memory-care/">Memory care</a></label>
      <div class="care-detail">
        <label for="mc-beds">Memory care: beds or suites</label>
        <input type="number" id="mc-beds" name="Memory care beds" min="0" inputmode="numeric">
        <label for="mc-setting">Is memory care a secured, separate wing or building? Any dedicated programming? <span class="opt">(optional)</span></label>
        <textarea id="mc-setting" name="Memory care setting and programming"></textarea>
      </div>
    </div>

    <div class="care-item">
      <input type="checkbox" id="care-sn" class="care-toggle" name="Q1 Care levels" value="Skilled nursing">
      <label for="care-sn" class="care-toggle-label"><a href="/guides/skilled-nursing/">Skilled nursing</a></label>
      <div class="care-detail">
        <label for="sn-beds">Skilled nursing: licensed beds</label>
        <input type="number" id="sn-beds" name="Skilled nursing beds" min="0" inputmode="numeric">
        <label for="sn-cert">Medicare and/or Medicaid certified? Any beds set aside for short-term rehab vs long-term care? <span class="opt">(optional)</span></label>
        <textarea id="sn-cert" name="Skilled nursing certification and bed mix"></textarea>
      </div>
    </div>

    <div class="care-item">
      <input type="checkbox" id="care-rs" class="care-toggle" name="Q1 Care levels" value="Respite / short stays">
      <label for="care-rs" class="care-toggle-label">Respite / short stays</label>
      <div class="care-detail">
        <label for="rs-beds">Respite: dedicated respite beds, if any</label>
        <input type="number" id="rs-beds" name="Respite dedicated beds" min="0" inputmode="numeric">
        <p class="hint">Leave blank if respite is offered as-available within your other care levels.</p>
        <label for="rs-detail">Which care levels offer respite, and the minimum or typical stay? <span class="opt">(optional)</span></label>
        <textarea id="rs-detail" name="Respite availability and stay length"></textarea>
      </div>
    </div>
  </fieldset>

  <fieldset>
    <legend>Care approach</legend>
    <label for="c2">How do care-level assessments work at your community, and how often are residents reassessed?</label>
    <textarea id="c2" name="Q2 Care assessments"></textarea>
    <label for="c3">Can a resident age in place as needs grow - and where is the line?</label>
    <p class="hint">What needs would require a move?</p>
    <textarea id="c3" name="Q3 Aging in place and its limits"></textarea>
    <label for="c4">Can couples live together when they need different levels of care?</label>
    <input type="text" id="c4" name="Q4 Couples with different care levels">
  </fieldset>

  <fieldset>
    <legend>Medical support</legend>
    <label for="c5">Medication management: reminders only, or full administration?</label>
    <input type="text" id="c5" name="Q5 Medication management">
    <label for="c6">Nursing coverage <span class="opt">(24/7 RN, daytime RN, LPN, on call)</span></label>
    <input type="text" id="c6" name="Q6 Nursing coverage">
    <label for="c7">Therapy services on site <span class="opt">(PT / OT / speech - in-house or visiting?)</span></label>
    <input type="text" id="c7" name="Q7 Therapy services">
    <label for="c8">Visiting practitioners <span class="opt">(physician, podiatry, dentistry, mental health)</span></label>
    <input type="text" id="c8" name="Q8 Visiting practitioners">
    <label for="c9">Do you coordinate with <a href="/guides/hospice-and-palliative-care/">hospice</a> for end-of-life care on site?</label>
    <input type="text" id="c9" name="Q9 Hospice coordination">
    <label for="c10">Conditions you routinely support - and any you cannot</label>
    <p class="hint">Diabetes/insulin, oxygen, catheter, two-person transfers…</p>
    <textarea id="c10" name="Q10 Conditions supported and not supported"></textarea>
  </fieldset>

  <fieldset>
    <legend>Staffing</legend>
    <p class="hint">Families ask about this more than almost anything. We publish these as
    <strong>community-reported</strong> figures, dated, and shown next to the official staffing
    record (Medicare Care Compare or your state licensing record) so families can compare. Share
    only what you're comfortable standing behind. See <a href="/guides/staffing-ratios/">how
    families read staffing numbers</a>.</p>
    <label for="c10a">Overnight coverage <span class="opt">(awake staff, and nurse on site or on call?)</span></label>
    <input type="text" id="c10a" name="Q10a Overnight coverage">
    <label for="c10b">Typical daytime staffing ratios, by care level</label>
    <p class="hint">For example: assisted living about 1 to 8, memory care about 1 to 6. Approximate is fine.</p>
    <textarea id="c10b" name="Q10b Daytime staffing ratios"></textarea>
    <label for="c10c">Most recent caregiver turnover, and the period it covers <span class="opt">(optional)</span></label>
    <input type="text" id="c10c" name="Q10c Caregiver turnover">
  </fieldset>

  <fieldset>
    <legend>Non-medical services</legend>
    <label for="c11">What's included in the base monthly rate?</label>
    <p class="hint">Housekeeping frequency, laundry, linens, utilities, cable/internet…</p>
    <textarea id="c11" name="Q11 Included in base rate"></textarea>
    <label for="c12">What's billed separately, and roughly how is it priced?</label>
    <p class="hint">Care points/levels, à la carte…</p>
    <textarea id="c12" name="Q12 Billed separately and pricing model"></textarea>
    <label for="c13">Personal care help available <span class="opt">(bathing, dressing, escorts to meals/appointments)</span></label>
    <textarea id="c13" name="Q13 Personal care help"></textarea>
  </fieldset>

  <fieldset>
    <legend>Who can live here</legend>
    <label for="c14">Age requirement <span class="opt">(55+, 62+, none)</span> and any exceptions</label>
    <p class="hint">Younger spouse, adult disabled child…</p>
    <input type="text" id="c14" name="Q14 Age requirement and exceptions">
    <label for="c15">Pet policy</label>
    <p class="hint">Allowed? Size/type limits, deposits or fees, and what support exists if a resident can no longer care for the pet.</p>
    <textarea id="c15" name="Q15 Pet policy"></textarea>
    <label for="c16">Do you accept <a href="/guides/medicaid-vs-medicare/">Medicaid</a> (directly or after a private-pay period)? Long-term care insurance?</label>
    <textarea id="c16" name="Q16 Medicaid and LTC insurance"></textarea>
  </fieldset>

  <fieldset>
    <legend>Quality &amp; accountability</legend>
    <p class="hint">Answer these about your general <strong>process</strong>, not any specific
    incident, resident, or family - we publish policies, not case histories, and we won't
    print details tied to an individual.</p>
    <label for="c17">What is your process when a family or resident raises a concern or complaint?</label>
    <p class="hint">Who receives it, and what's the typical response time?</p>
    <textarea id="c17" name="Q17 Complaint intake process"></textarea>
    <label for="c18">How do you investigate and resolve a complaint, and how do you follow up with the family?</label>
    <textarea id="c18" name="Q18 Investigation and follow-up"></textarea>
    <label for="c19">How do complaints feed back into how you operate?</label>
    <p class="hint">Do you track patterns, retrain staff, or change procedures as a result?</p>
    <textarea id="c19" name="Q19 Complaints feeding back into operations"></textarea>
  </fieldset>

{% include q-form-end.html %}

When you're ready: **[Daily life →](/for-communities/questionnaire-daily-life/)**
