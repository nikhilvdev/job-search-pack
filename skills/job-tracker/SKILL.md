---
name: job-tracker
description: Use this skill whenever the user wants to log, update, or review job applications — e.g. "add this application to my tracker," "log that I applied to Acme for the Staff Engineer role," "update the status on my Beta Corp application to Interview," "what applications need a follow-up," "show me my job search pipeline," "I heard back from X, mark it as rejected," or any request to record or check on job-search progress over time. This skill maintains one persistent tracker file across sessions — on first use it creates the tracker; on later use it reads the existing tracker before adding, updating, or querying it, and never overwrites or drops existing entries. Trigger this even if the user gives only partial details (e.g. just a company name and status change) — ask for the minimum needed to identify or create a row rather than guessing. No file attachment is required to use this skill; it manages its own persistent output file.
license: Apache-2.0
---

# Job Tracker

Maintains a single running tracker of job applications across sessions — add an application, update its status, or query the pipeline, without ever losing data from a previous session.

## Why this skill is different from the rest of the pack

Every other skill in this pack produces one document from one conversation. This one is stateful: it reads an existing file, changes a small part of it, and writes the whole thing back — over and over, across many separate conversations. The core discipline here isn't "produce good content," it's "never silently lose or corrupt what's already there." Always read the full existing tracker before writing anything, and always write back the full table, not just the part you touched.

## Required inputs

Inputs depend on which operation is being requested — there's no fixed upfront list:

- **Add an application**: company + role, at minimum. Status defaults to "Applied" unless the user says otherwise. Date applied, posting URL, contact, and notes are optional — include them if given, don't block on them if not.
- **Update an application**: enough to identify the existing row — company + role, or company alone if there's no ambiguity — plus what's changing.
- **Query the tracker**: no new inputs needed beyond the user's intent (e.g. "what's overdue for a follow-up," "show me everything at Offer stage").

If a request is ambiguous about which row it refers to, ask rather than guess — see Step 4.

## Step 1: Locate or create the tracker

Check whether `outputs/[Name]_Job_Tracker.md` already exists. If it does, read it in full before doing anything else — never write to it blind, based only on what's been said in the current conversation. If it doesn't exist yet, create it fresh using the template in Step 6.

## Step 2: Determine the operation

Classify the request as one of: **Add**, **Update**, or **Query**. Each has a different read-modify-write shape, handled below.

## Step 3: Add flow

Before appending a new row, check the existing table for a likely duplicate — same company and same or similar role already present. If there's a plausible match, ask whether this is a new application (e.g. a re-application, or a different role at the same company) or an update to the existing row, rather than assuming either way.

## Step 4: Update flow

Find the row(s) that match what the user described. If more than one row is a plausible match — for example, two applications at the same company for different roles, or a prior application and a fresh re-application — ask the user to disambiguate before writing anything. Apply only the specific change the user stated; don't infer additional progress they didn't mention (e.g. "I had a call with them" doesn't automatically mean the status moves to "Interview" — ask, or use their own words for the status, rather than assuming a stage transition).

## Step 5: Query flow

This is read-only — filter and summarize the existing table (e.g. follow-ups due = "Applied" status with no logged contact in the last 7+ days, or everything currently at "Offer" stage) and answer directly. Do not write to the file for a pure query.

## Step 6: Rewrite the full file

Whenever a write happens (Add or Update), always read-modify-write the *complete* file — every row not touched by this operation must be carried forward unchanged. Never regenerate the tracker from just the current conversation's context; the file is the source of truth, not your memory of past sessions.

```markdown
# Job Search Tracker — [Name]

## Summary
[counts by status; number of follow-ups currently due]

## Applications
| Company | Role | Status | Date Applied | Last Contact | Next Follow-up | Source / URL | Notes |
|---|---|---|---|---|---|---|---|
| [Company] | [Role] | [Applied/Interview/Offer/etc.] | [date] | [date or —] | [date or —] | [url or —] | [notes] |

## Follow-ups due
[rows from above where a follow-up is overdue or approaching]

## Archive (Rejected / Withdrawn)
| Company | Role | Status | Date Applied | Notes |
|---|---|---|---|---|
```

Save the file as `outputs/[Name]_Job_Tracker.md` — note this is one file reused across every session for a given person, unlike the other skills in this pack, which each produce a new, separately-named file per invocation (e.g. `[Name]_Resume_[Company]_[Title].md`). The tracker's whole purpose is to accumulate state over time, so it keeps one stable filename instead.

## A note on accuracy

Never overwrite or silently drop existing rows when updating — always full read-modify-write, and treat the existing file as the source of truth over anything assumed from conversation context alone. Ask for disambiguation before updating when more than one row could plausibly match. Never infer or fabricate a status change, interview outcome, or offer detail the user hasn't explicitly stated. Keep date formats consistent across the file.
