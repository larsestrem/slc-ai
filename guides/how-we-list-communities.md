---
layout: guide
title: "Why We Don't Show Star Ratings - And How to Find the Real Ones"
description: "We don't display ratings or scores on this site. Here's why, and how to find a community's real ratings - government, Medicare/Medicaid, and family reviews - in one click from its profile."
permalink: /guides/how-we-list-communities/
topic_group: quality
updated: 2026-07-14
related:
  - /guides/interpreting-online-reviews/
  - /guides/reading-inspection-reports-and-ratings/
  - /guides/checking-complaints-and-state-records/
  - /guides/how-to-choose-a-senior-care-facility/
  - /guides/adult-family-homes/
faqs: [{"q": "Why not just show the star rating you found?", "a": "Because we found out the hard way that we could get it wrong. Ratings come from several different data pipelines, get remapped and re-summarized along the way, and change on their own schedule. A wrong number on a page about your parent's care is a real harm, not a minor bug - so we stopped publishing one and started linking directly to where the real, current number lives."}, {"q": "Do you flag or warn about specific communities?", "a": "No. Every profile links to the official record and carries the same note asking you to read it and recent reviews before you decide. We don't single out individual communities, because even a neutral-sounding warning implies we know something we haven't said. We don't say what's in any record - records change, entries can be disputed or resolved, and the source is always more current than we are. The note just asks you to look; what you find, you find at the source, today."}, {"q": "Then why read the record at all if every community has the same note?", "a": "Because the record is worth your time before any big decision, and it's the same reason we link it the same way everywhere. Records reflect a moment in time; problems get fixed, findings get challenged, ownership changes. We point you to the live source instead of characterizing it ourselves, and the community's own response to any issue is worth asking about directly."}, {"q": "Why isn't the directory a complete registry?", "a": "Building and verifying each listing takes real research, and we're still working through the states we cover. If a community you're looking for isn't listed yet, that's a gap in our coverage, not a judgment about the community - check the state licensing lookup directly."}]
---

Type a community's name into our directory and, if it's listed, you'll land on its profile - but you won't find a star rating or a numeric score anywhere on this site. That's deliberate.
This page explains why, and how to actually find a community's real ratings in one click.

## Why we stopped showing ratings ourselves

We used to display a star rating and a category label on every listing. Then an outside review
of the site found a real, confirmed error: a nursing home was shown with a government rating that
was flatly wrong - a sub-score had been stored and displayed as if it were the overall rating.
When we went back and checked the rest of the dataset, we found more of the same. Ratings pass
through several data sources on their way to a page, they get relabeled and re-summarized along
the way, and they change on a schedule we don't control. Any one of those steps can silently
introduce an error - and a wrong number on a page about where your parent might live is a real
harm, not a cosmetic bug.

So we made a structural change instead of trying to patch our way to perfect accuracy forever:
**we don't compute or publish a rating at all.** Every community's profile instead links you
directly to the primary sources - the ones with the real, current, authoritative numbers - so you
see exactly what a regulator or reviewer actually said, not our summary of it.

## Where to find a community's ratings

On every facility's profile, look for the **"Ratings & reviews"** panel near the top of the page,
and the fuller **"Ratings & official records"** section near the bottom. Both list the same thing:
clearly labeled links, never a number we assert ourselves.

- **Government / Medicare rating** (nursing homes) - a direct link to that facility's page on
  **Medicare Care Compare**, the federal government's own rating tool. This is the same source
  we used to summarize (and sometimes get wrong) - now you see it straight from CMS, current as
  of the moment you click, not cached from whenever we last checked.
- **State license & inspections** (assisted living, memory care, small homes - anything without a
  federal nursing-home rating) - a direct link to your state's official licensing lookup, which
  shows license status, inspection findings, and complaint history.
- **Family & resident reviews** - a direct link to every review platform we found a source for
  (Google, Yelp, A Place for Mom, Caring.com, and others, each labeled by name), plus a
  ready-made search link so you can find more. Click through and read the actual reviews and
  whatever star average that platform shows - not our restatement of it.

Each link is labeled with exactly where it goes, so you always know whether you're looking at a
government source or a commercial review site - they measure very different things. Our guides on
[reading government inspection ratings](/guides/reading-inspection-reports-and-ratings/) and
[interpreting online reviews](/guides/interpreting-online-reviews/) explain what each one can and
can't tell you.

## The same note on every community

We don't assert anything about any community's quality, and we don't single out individual
communities with a warning - even a neutral "look closely at this one" would imply we know
something we haven't said. So **every profile carries the same note**: read this community's
official record and recent reviews before you decide, with the official record linked first.
Communities can [claim their listing](/for-communities/) to add context in their own words,
including [how they handle concerns](/guides/why-good-communities-get-complaints/) - often the most
useful thing you can learn.

## How to judge what you find when you click through

Whatever rating or review you find at the source, a few things are worth keeping in mind:

- **A cluster of specific, repeated complaints** (the same safety issue, named by multiple
  families or inspections) is a serious signal, wherever it appears.
- **A thin handful of mixed or negative reviews** can just mean a small or newer community that
  hasn't built a public record yet - not necessarily a problem. See how we think about
  [small-sample noise cutting both ways](/guides/interpreting-online-reviews/#why-good-facilities-can-carry-mediocre-scores).
- **A lower rating isn't automatically disqualifying.** Proximity and visit frequency matter - a
  lower-rated community you can realistically visit often may be a better real-world choice than
  a higher-rated one you'll rarely see. Our [guide to choosing a
  facility](/guides/how-to-choose-a-senior-care-facility/#step-3-build-a-shortlist) walks through
  weighing distance against rating directly.
- **Government and review-site numbers measure different things**, and shouldn't be read as
  interchangeable - a federal inspection score reflects staffing and clinical data; a review
  average reflects families' day-to-day experience.
- **Every community gets complaints - the response is the signal.** Running a senior care
  community is genuinely hard work, and even excellent ones accumulate hard reviews and the
  occasional citation. What separates them is
  [how they handle complaints and what changes afterward](/guides/why-good-communities-get-complaints/).

None of this replaces reading the real numbers yourself at the source, and your own visit still
tells you more than any number can.

## Coverage isn't complete

Our directory currently contains {{ site.data.stats.visible_total.facilities }} verified listings
across {{ site.data.stats.visible_total.cities }} cities in
{{ site.data.stats.visible_total.states }} states. It is **not a complete registry** - those
states license more communities than we've verified and added so far, and we're still working
state by state. If a community isn't listed yet, check your state's licensing lookup directly
([how to read the record fairly](/guides/checking-complaints-and-state-records/)) rather than
assuming its absence means anything about the community itself.

## Common questions

**Why not just show the star rating you found?**
Because we found out the hard way that we could get it wrong. Ratings come from several different
data pipelines, get remapped and re-summarized along the way, and change on their own schedule. A
wrong number on a page about your parent's care is a real harm, not a minor bug - so we stopped
publishing one and started linking directly to where the real, current number lives.

**Do you flag or warn about specific communities?**
No. Every profile links to the official record and carries the same note asking you to read it
and recent reviews before you decide. We don't single out individual communities, because even a
neutral-sounding warning implies we know something we haven't said. We don't say what's in any
record - records change, entries can be disputed or resolved, and the source is always more
current than we are. The note just asks you to look; what you find, you find at the source, today.

**Then why read the record at all if every community has the same note?**
Because the official record is worth your time before any big decision - that's true everywhere,
which is why we link it the same way everywhere. Records reflect a moment in time; problems get
fixed, findings get challenged, ownership changes. We point you to the live source instead of
characterizing it ourselves, and the community's own response to any issue is worth asking about
directly.

**Why isn't the directory a complete registry?**
Building and verifying each listing takes real research, and we're still working through the
states we cover. If a community you're looking for isn't listed yet, that's a gap in our
coverage, not a judgment about the community - check the state licensing lookup directly.
