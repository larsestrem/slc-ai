---
layout: page
title: "Your Listing in the Directory — Before & After"
description: "What a community's card looks like on directory and city pages before and after claiming: photo thumbnail and named profile manager."
noindex: true
sitemap: false
crumbs:
  - name: For Communities
    url: /for-communities/
  - name: Your card, before & after
    url: /for-communities/example-card/
cards:
  - name: "Alder Grove Senior Living"
    url: /for-communities/example-profile/
    city_name: "Rivertown"
    state_abbrev: "OR"
    care_levels: ["independent-living", "assisted-living", "memory-care", "skilled-nursing"]
    facility_size: "large"
    description: "Alder Grove Senior Living is a 142-resident continuing-care community offering independent living, assisted living, memory care, and skilled nursing on one campus."
    thumb:
      src: /assets/demo/exterior.svg
      alt: "Front entrance of Alder Grove Senior Living"
    managed_by:
      name: "Maria Alvarez"
      role: "Executive Director"
  - name: "Alder Grove Senior Living"
    url: /for-communities/example-profile/
    city_name: "Rivertown"
    state_abbrev: "OR"
    care_levels: ["independent-living", "assisted-living", "memory-care", "skilled-nursing"]
    facility_size: "large"
    description: "Alder Grove Senior Living is a 142-resident continuing-care community offering independent living, assisted living, memory care, and skilled nursing on one campus."
---

<p class="notice sample-banner"><strong>Sample page</strong> using our fictional demo
community. This is the exact card families see on city, county, and state directory pages —
shown as it looks <strong>after</strong> a community claims its listing, and before.</p>

When families browse a directory page, they scan a grid of cards like these. A claimed
listing gets two quiet advantages: **your photo** at the top of the card, and **your profile
manager's name** at the bottom. Neither changes your position on the page — placement is
never paid and the order stays alphabetical — but a card with a real photo and a real name
gets noticed, and clicked, more than a text-only card beside it.

{% assign card_after = page.cards | first %}
{% assign card_before = page.cards | last %}
<h2>After claiming — with a photo and a named manager</h2>
<ul class="grid" style="max-width:24rem">
  {% include facility-card.html facility=card_after %}
</ul>

<h2>Before claiming — text only</h2>
<ul class="grid" style="max-width:24rem">
  {% include facility-card.html facility=card_before %}
</ul>

The photo comes from the first image you send us ([landscape, please](/for-communities/why-landscape-photos/)),
and the manager credit names whoever submitted your listing content —
[we recommend executive staff](/for-communities/#answer-what-you-can-when-you-can).
Ready? **[Claim your listing →](/for-communities/)**
