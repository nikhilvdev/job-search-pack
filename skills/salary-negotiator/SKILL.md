---
name: salary-negotiator
description: Use this skill whenever the user wants help negotiating a job offer or understanding market compensation — e.g. "help me negotiate this offer," "what should I counter with," "is this offer competitive for a Staff Engineer in Austin," "what's the market rate for a Senior PM at a Series B startup," "draft a counter-offer email," or any request to evaluate or push back on salary, bonus, or equity terms. Also applies to "should I accept this offer" and requests to compare a competing offer. Trigger this even if the user only pastes offer numbers with no formal offer letter, and even if they don't use the word "skill." Requires the offer details (base salary at minimum; bonus, equity, location, and level if available) and the target role/title. If web search tools are available, use them to pull current market-rate data; if not, use general knowledge but state explicitly that the figures may be approximate or dated and recommend the user cross-check against a live source (e.g. levels.fyi, Glassdoor, Blind, Payscale).
license: Apache-2.0
---

# Salary Negotiator

Builds a negotiation case grounded in actual leverage and current market data, then drafts counter-offer scripts — not generic "always negotiate" advice, but a specific read on this offer, this market, and this person's actual position.

## Why leverage has to be honest

The easiest way to make this skill useless is to overstate leverage — telling someone to push hard on an offer when they don't actually have a competing offer, an in-demand skill gap, or market data behind them. Bad negotiation advice can cost someone an offer they wanted. Every negotiation strategy this skill produces should be traceable to a specific, real reason the company might say yes — not just confidence that asking is free.

## Required inputs

1. **Offer details** — base salary, at minimum. Bonus, equity, benefits, level, and location if available. Required.
2. **Target role/title and location** — required, though this can often be read directly off the offer itself.
3. **Optional**: a competing offer, current compensation, years of experience, company size/stage, or a specific concern the person wants to focus on (e.g. "I only care about base, not equity").

## Step 1: Extract everything

Pull the full offer as given — base, bonus, equity (and its vesting/strike details if provided), benefits, level, location — plus the target role and any competing offer or current compensation mentioned.

## Step 2: Research market rate

If `WebSearch` or `WebFetch` tools are available, use them to pull current compensation-band data for this role, level, and location. If those tools are not available, use general knowledge but state explicitly in the output that the figures may be approximate or dated, and name a live source (levels.fyi, Glassdoor, Blind, Payscale, or a relevant industry survey) the person should cross-check before relying on the number.

## Step 3: Build the negotiation case

Identify concrete leverage: a competing offer (strongest lever, if present), a skill or specialization that's scarce relative to demand, a gap between this offer and the researched market range, or a demonstrated track record directly relevant to the role. If none of these are strong, say so plainly rather than inventing confidence — a modest, well-justified ask still beats an aggressive one built on nothing.

## Step 4: Draft counter-offer options

Produce at least two strategic postures — for example, an anchor-high approach (ask near the top of the researched range, justified by the strongest leverage point) and a balanced/collaborative approach (ask for a specific, smaller adjustment framed as closing a gap rather than a demand). For each, write both a full email script and short verbal talking points for a call.

## Step 5: Output the document

```markdown
# Salary Negotiation Prep — [Name] — [Company] / [Title]

## Offer summary
[base, bonus, equity, benefits, level, location, as given]

## Market rate read
[source: live search results / general knowledge — flagged explicitly, with staleness caveat if applicable]
[range estimate for this role/level/location, and where this offer sits within it]

## Leverage points
[competing offers, scarce skills, market gap, track record — or an honest note that leverage is limited]

## Negotiation strategy options
1. **Anchor-high**: [specifics]
2. **Balanced**: [specifics]

**Recommended:** [which, and why, given the actual leverage available]

## Counter-offer scripts

### Email version
[full draft]

### Call / verbal talking points
[short bullet script]

## What to avoid saying
[e.g. don't reference a competing offer that doesn't exist, don't frame this as an ultimatum if the role is genuinely wanted]

## Open items to confirm
[anything the person should verify — market data currency, equity terms, etc.]
```

Save the file as `outputs/[Name]_SalaryNegotiation_[Company]_[Title].md` and present it as a file, not inline chat text.

## A note on accuracy

Market compensation data may be approximate, regionally imprecise, or dated — always caveat this explicitly and point to a live source for the person to verify before acting. Never coach the person to bluff about a competing offer that doesn't exist. Never promise or imply a guaranteed negotiation outcome — the value here is a well-reasoned ask and script, not a prediction.
