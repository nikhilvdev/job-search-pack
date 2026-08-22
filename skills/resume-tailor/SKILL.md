---
name: resume-tailor
description: Use this skill whenever the user wants to tailor, rewrite, or optimize a resume for a specific job posting or role — e.g. "tailor my resume for this Senior Data Scientist posting," "rewrite my resume for this job description," "make my resume ATS-friendly for this role," "optimize my resume so it passes the applicant tracking system," "how well does my resume match this job posting," or any request to align a resume's content and keywords with a specific listing rather than produce a generic resume. Also applies to "will my resume get past the ATS for X" and requests to close keyword gaps between a resume and a job description. Trigger this even if the user pastes the job posting as plain text or a URL rather than a file, and even if they don't use the word "skill." Requires a resume (PDF or pasted text) and the target job posting (pasted text, PDF, or URL); if given a URL, fetch it if tools allow, otherwise ask the user to paste the posting text.
license: Apache-2.0
---

# Resume Tailor

Rewrites a resume against a specific job posting — not a generic polish, but a targeted alignment of content, terminology, and keywords to what this particular listing is actually asking for, plus honest flags on anything the resume can't support.

## Why gap analysis before rewriting

A tailored resume is only as good as the honesty of the gap analysis behind it. Skipping straight to "here's a punched-up resume" hides the difference between *reframing true experience in the JD's language* (fine) and *claiming something that isn't there* (not fine, and often obvious to an interviewer within minutes). Surface the gap analysis in the output so the person can see exactly what was reworded versus what's missing versus what got flagged as unsupportable — that's the actual value here, not just prettier bullets.

## Required inputs

1. **Resume** — PDF or pasted text. Required.
2. **Job posting** — pasted text, PDF, or a URL. Required — the entire point of this skill is JD-specific tailoring, not generic resume improvement. If missing, ask for it before proceeding; don't guess at what a role needs from a title alone.
3. **LinkedIn profile export** — optional. Useful for cross-checking that a claim used here would also be defensible/consistent with what's public elsewhere.

If given a URL for the job posting, fetch it if you have a tool that allows that; if not, tell the user and ask them to paste the posting text instead — don't proceed on a title alone.

## Step 1: Extract everything

Read the full resume: every bullet, employer, title, exact dates, and any metrics already present. Read the full job posting: required qualifications, preferred qualifications, responsibilities, and the *exact phrasing* it uses for skills and tools — ATS keyword matching is often literal-string-sensitive, so note when the posting says "stakeholder management" versus "cross-functional leadership" even if the resume's underlying experience is the same thing worded differently.

## Step 2: Three-way gap analysis

Sort the posting's requirements and keywords into three buckets:

- **Already covered** — the resume demonstrates this, possibly under different wording than the posting uses. Note the wording gap even when the substance is there; that's usually the easiest, highest-value fix.
- **Missing** — the posting asks for it and nothing in the resume speaks to it, but it's plausible the person has relevant experience they just didn't think to include. Ask, don't assume either way.
- **Cannot honestly claim** — the resume gives no basis for this and the person hasn't said otherwise. This bucket stays a flagged gap, not a rewrite target — see Step 3.

## Step 3: Decide what's fair to reword vs. what can't be added

Reframing existing true experience into the posting's terminology is fair game: if the resume says "led a team through a platform migration" and the posting wants "cross-functional stakeholder management," and that migration genuinely involved managing stakeholders across teams, use their language. Inventing a tool, certification, metric, or responsibility that wasn't there is not fair game, no matter how close the posting's ask is to what the person "basically" did. When in doubt, ask rather than assume the closer interpretation is safe to write down.

## Step 4: Build the tailored resume

Rewrite with two things in mind simultaneously: keyword alignment with the posting, and ATS-safe formatting. Keep formatting plain-text-parseable — standard section headers ("Experience," "Education," "Skills"), no tables, columns, text boxes, headers/footers, or graphics, since many ATS parsers mangle those into garbled or dropped text. Keep date formatting consistent throughout.

## Step 5: Score briefly, then output

Give a short match read — not a full audit, just enough to orient the person: rough keyword/requirement match percentage, the single biggest remaining gap, and any ATS-formatting risk in the original resume that's being fixed. Then produce the `.md` file using this structure:

```markdown
# Tailored Resume — [Name] — [Company] / [Job Title]

## Match read
[rough match %, biggest gap, ATS formatting risk notes]

## Keyword gap analysis
- Already covered (reworded to posting's terminology): ...
- Missing (plausible but unconfirmed — ask): ...
- Cannot honestly claim (flagged, not added to the resume): ...

## Tailored Resume

### [Name] — [contact line]

### Summary
[if the original has one, or if a summary genuinely helps orient this specific posting]

### Skills
[reordered/reworded to match posting terminology where the substance is genuinely there]

### Experience

**[Title] — [Company]** ([dates])
- [rewritten bullet]
- [rewritten bullet]

**[Title] — [Company]** ([dates])
- [rewritten bullet]

### Education / Certifications
[as-is, unless posting-relevant certifications are missing and worth flagging]

## ATS formatting notes
[anything fixed or worth knowing about parseability]

## Open items to confirm
[unconfirmed "missing" bucket items, anything the person should double-check before submitting]
```

Save the file as `outputs/[Name]_Resume_[Company]_[Title].md` (use the person's actual name, the company, and a slugified job title) and present it as a file, not inline chat text.

## A note on accuracy

Never fabricate employers, titles, dates, degrees, tools, certifications, or metrics. Never claim a required qualification the resume doesn't support — flag it as an open item instead of quietly writing it in. "ATS optimization" means honest alignment of real experience to the posting's language and clean, parseable formatting — not keyword-stuffing a skills section with terms the resume can't back up in an interview.
