---
name: linkedin-profile-optimizer
description: Use this skill whenever the user wants to audit, optimize, rewrite, or reposition a LinkedIn profile toward a specific target role, title, or designation — e.g. "optimize my LinkedIn for a Staff Engineer role," "how does my profile look for VP Engineering," "help me reposition my LinkedIn for Product Management," "rewrite my LinkedIn headline and About section," "review my LinkedIn for a career pivot," "improve my LinkedIn for a promotion case," or any request to review a LinkedIn export/PDF against a job title, career direction, or job description. Also applies to broader career-coaching, personal-branding, job-search, or recruiter-visibility requests that center on a LinkedIn profile. Trigger this even if the user only provides a LinkedIn PDF with no resume, and even if they don't use the word "skill" — any profile-vs-role positioning request qualifies. Requires a LinkedIn profile export (PDF) and a target designation; a resume is optional but improves the result.
license: Apache-2.0
---

# LinkedIn Profile Optimizer

Audits a LinkedIn profile against a specific target designation and produces a decision-support document — not a single prescriptive rewrite, but a set of concrete phrasing **options per profile area** so the person can choose what fits their voice and situation.

## Why options, not one rewrite

A single "here's your new profile" output forces the person to accept or reject wholesale. Giving 2–4 options per area (headline, About, each Experience entry) lets them mix and match, and makes it obvious this is a recommendation, not a fait accompli. Keep this shape even under pressure to "just give me the final version" — if they want that, the person can tell you which option they picked and you write the final copy then.

## Required inputs

1. **LinkedIn profile** — PDF export (or pasted text). Required.
2. **Target designation** — the specific role/title being optimized for (e.g. "Senior Engineering Manager," "Staff Engineer," "Head of Product"). Required — the whole point of this skill is role-specific positioning, not generic polish. If missing, ask for it before proceeding; don't guess.
3. **Resume** — optional. If provided, it's usually richer than the LinkedIn export (metrics, projects, specifics) — see reconciliation step below before trusting it.

If the LinkedIn PDF is missing, ask for it — don't proceed on a resume alone, since LinkedIn's actual current field values (headline, About, Skills as listed) are what a recruiter searches against.

## Step 1: Extract everything

Read the full LinkedIn PDF: name, headline, location, About/Summary, every Experience entry (title, company, exact dates, location, current bullets), Skills as listed, Certifications, Education, Projects, Featured, Recommendations if visible. Do the same for the resume if provided. Don't summarize away details you don't yet know are unimportant — you need the full picture before judging what's weak.

## Step 2: Reconcile LinkedIn vs. resume (only if resume provided)

Resumes are frequently more detailed than LinkedIn — sometimes because the person just hasn't ported content over yet, sometimes because a resume was polished (or AI-assisted) with numbers or projects that were never verified. Both are common. Don't assume either way.

Compare the two documents and flag, specifically:
- Any job title, company, or date that differs between the two
- Any quantified metric in the resume that doesn't appear on LinkedIn
- Any project, achievement, or award in the resume with no LinkedIn counterpart

If there are discrepancies, **ask the user before using resume-only content** — a short, specific set of questions (e.g. "the resume shows a 45% figure for X that isn't on LinkedIn — is that accurate and can I use it?"). Use whatever your environment's clarifying-question mechanism is (buttons if available, plain text otherwise). This isn't optional politeness — using unverified numbers in a professional profile has real consequences if the person can't back them up in an interview. Once confirmed, treat LinkedIn as the source of truth for titles/dates/company names unless the user says otherwise, and treat confirmed resume content as fair game for metrics and projects.

If no resume is provided, skip this step, and mark any bullet that would benefit from a number but doesn't have one as `[ADD METRIC IF AVAILABLE]` rather than inventing one.

## Step 3: Read the target designation correctly

The same underlying experience should be framed differently depending on the target:

- **IC/technical tracks** (Staff Engineer, Principal Engineer, Technical Architect) → lead with system design decisions, technical depth, and scale. Downplay or cut people-management bullets that don't have a technical angle.
- **Management tracks** (Engineering Manager, Senior EM, Director, VP) → lead with team size, delivery outcomes, stakeholder trust, and org-level impact. Technical depth becomes supporting evidence of credibility, not the headline.
- **Hybrid/architecture-leaning management** (e.g. "Engineering Manager, Platform") → balance both, similar to what's usually right for someone who's genuinely done both tracks.
- **Adjacent pivots** (e.g. an engineer targeting Product Management) → identify which existing experience actually transfers (stakeholder work, requirements gathering, roadmap involvement) versus what should be quietly de-emphasized. Be honest if the profile doesn't yet support the pivot — say so rather than force it.

State explicitly, near the top of the output, what should dominate the profile for this specific designation and why — this framing decision drives every option that follows.

## Step 4: Score briefly, then build the options document

Give a short, honest current-state read (not a 17-part audit — this skill's output is options-first). Cover in 3–5 sentences: what's currently working, the biggest gap relative to the target designation, and a rough current-fit score (0–100) with one line of reasoning. This sets context; it isn't the deliverable.

Then produce the `.md` file using this structure:

```markdown
# LinkedIn Optimization Options — [Name] — Target: [Designation]

## Positioning read
[3–5 sentences: current fit, biggest gap, what should dominate for this designation, rough score]

## Area: Headline
**Current:** [as-is]
**Options:**
1. [option — one strategy, e.g. leadership-forward]
2. [option — another strategy, e.g. technical-forward]
3. [option — balanced]
**Recommended:** Option [X] — [one-line why, tied to the designation]

## Area: About / Summary
**Current:** [as-is, or "not present"]
**Options:**
1. [full rewrite variant A]
2. [full rewrite variant B — different opening angle or emphasis]
**Recommended:** [which, and why]

## Area: Skills
**Current:** [as listed]
**Recommended tiering for this designation:**
- Tier 1 (must-have, pin these): ...
- Tier 2 (supporting): ...
- Remove/de-prioritize: [with reason — e.g. outdated, off-target for this designation]

## Area: Experience — [most recent/relevant role] ([dates])
**Current:** [as-is]
**Options:**
1. [bullet set A]
2. [bullet set B — different emphasis, e.g. scale vs. leadership]
**Recommended:** [which, and why]

[Repeat per role. For roles more than ~2 tiers removed from the target designation's seniority, or older than ~5-7 years, give one tightened option rather than multiple — they don't need the same weight.]

## Area: Projects / Featured
[Only if source material supports it — don't invent projects]

## Open items to confirm
[Any resume/LinkedIn discrepancies still unresolved, missing metrics marked [ADD METRIC IF AVAILABLE], anything the user should double check]
```

Save the file as `outputs/[Name]_LinkedIn_Options_[Designation].md` (use the person's actual name and a slugified designation) and present it as a file, not inline chat text — this is meant to be a working reference document, not something to read once and lose in scrollback.

## A note on accuracy

Every rule from the original brief that inspired this skill still applies: don't invent metrics, don't invent projects, don't exaggerate seniority, don't overclaim expertise (e.g. don't lead with "AI Leadership" positioning if the evidence is one or two projects — that's a secondary angle, not the headline, until there's more behind it). If something is thin, say it's thin and offer the honest option rather than a padded one.
