---
name: cover-letter-writer
description: Use this skill whenever the user wants a cover letter written or rewritten for a specific job posting or company — e.g. "write a cover letter for this Product Manager role at Acme," "draft a cover letter for this job posting," "help me write a cover letter that isn't generic," "cover letter for my application to [Company]," or any request for a company- and role-specific cover letter rather than a template. Also applies to requests to research a company before writing. Trigger this even if the user only pastes a job posting URL and company name with no resume attached yet — ask for the resume/experience source first — and even if they don't use the word "skill." Requires a resume or equivalent summary of experience, and the target job posting/company. If web search or web fetch tools are available, use them for company research; if not, say so explicitly and ask the user for a few company-specific facts rather than writing from generic knowledge alone.
license: Apache-2.0
---

# Cover Letter Writer

Writes a cover letter grounded in two real things: the candidate's actual experience and the company's actual, current situation — not a template with the company name swapped in.

## Why this has to be company-researched

The failure mode this skill exists to prevent is the cover letter that could be sent to any company with a find-and-replace on the name — "I've always admired your innovative culture and dynamic team." That sentence is worthless to a hiring manager precisely because it's true of nothing in particular. Every letter this skill produces needs at least one detail — a product, a recent announcement, a specific stated value, something from the posting itself — that couldn't be copy-pasted into a letter for a different company.

## Required inputs

1. **Resume, or a summary of relevant experience** — required. This is the substance side of the letter; without it there's nothing real to connect to the company.
2. **Job posting and company name** — required. If only a company name is given with no posting, ask for the posting or at least the role title — the letter needs to speak to a specific role, not just "a job at this company."
3. **Optional**: hiring manager name, a referral or personal connection, a tone preference, or specific achievements the person wants highlighted. Ask if useful, but don't block on these.

## Step 1: Extract everything

Pull the relevant experience from the resume (or summary), and the responsibilities/requirements/tone from the job posting, plus the company name.

## Step 2: Research the company

If `WebSearch` or `WebFetch` tools are available, use them to find recent news, the company's product or mission, and any culture signals worth referencing. If those tools are not available, say so explicitly in your response before writing anything, and either work from what's stated in the job posting itself or ask the user for 2–3 company-specific facts to work with. Do not fill this gap with generic praise — that's exactly the genericness this skill exists to avoid. A shorter, more honest letter beats a longer one padded with unverifiable enthusiasm.

## Step 3: Find genuine connection points

Identify 2–3 real overlaps between the candidate's actual experience and the company's actual stated needs, mission, or product direction — not "I am a hard worker who would be a great fit," but something specific enough that it demonstrates the person read the posting and knows something true about the company.

## Step 4: Draft options

Produce at least two full letters using different opening/angle strategies — for example, one that leads with a specific relevant achievement, and one that leads with genuine alignment to the company's mission or current direction. This mirrors the idea that a single "final" letter forces an all-or-nothing acceptance; two real options let the person pick the one that sounds like them.

## Step 5: Output the document

```markdown
# Cover Letter — [Name] — [Company] / [Job Title]

## Company research summary
[source: web search / user-provided facts / job posting only — state which, plainly]
[mission/product, recent news, culture signals actually found]

## Connection points identified
1. [genuine overlap between candidate experience and company's actual needs]
2. [genuine overlap]
3. [genuine overlap, if there's a third worth including]

## Cover Letter — Option A ([opening strategy, e.g. "leads with a specific achievement"])
[full letter]

## Cover Letter — Option B ([different opening strategy, e.g. "leads with mission alignment"])
[full letter]

## Recommended
[which option, and why, given the role/company/candidate]

## Open items to confirm
[any company facts that came from general knowledge rather than live research and should be double-checked, any missing details that would strengthen the letter]
```

Save the file as `outputs/[Name]_CoverLetter_[Company]_[Title].md` and present it as a file, not inline chat text.

## A note on accuracy

Never invent company facts, news, product details, or values — if research tools are unavailable, say so in the output rather than silently writing from possibly stale or generic training knowledge. Never invent a personal connection, referral, or interaction with the company that the user didn't actually mention. If the genuine connection points are thin because the research is thin, say so and keep the letter honest rather than padding it with unverifiable enthusiasm.
