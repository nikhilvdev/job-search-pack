# The Job Search Pack

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Agent%20Skill-D97757.svg)](https://www.anthropic.com/news/skills)

Five **Agent Skills** that cover the full job search: tailored applications, interview and negotiation prep, and a tracker to keep the whole pipeline organized. Land better roles, faster — with AI doing the heavy lifting on each stage. Ships as both a **Claude Code plugin** and a **Gemini CLI extension** — same `skills/` folder, same `SKILL.md` files, no divergent content to maintain.

## Skills in this pack

| Skill | What it does | Output |
|---|---|---|
| [Resume Tailor](skills/resume-tailor/SKILL.md) | ATS-optimized rewrites for each role | `outputs/[Name]_Resume_[Company]_[Title].md` |
| [Cover Letter Writer](skills/cover-letter-writer/SKILL.md) | Company-researched, never generic | `outputs/[Name]_CoverLetter_[Company]_[Title].md` |
| [LinkedIn Optimizer](skills/linkedin-profile-optimizer/SKILL.md) | Headline, About, and top bullets rewritten | `outputs/[Name]_LinkedIn_Options_[Designation].md` |
| [Salary Negotiator](skills/salary-negotiator/SKILL.md) | Market rates + counter-offer drafts | `outputs/[Name]_SalaryNegotiation_[Company]_[Title].md` |
| [Job Tracker](skills/job-tracker/SKILL.md) | Applications, status, and follow-ups in one place | `outputs/[Name]_Job_Tracker.md` (persistent, updated across sessions) |

Each skill's `SKILL.md` documents its own required/optional inputs, step-by-step process, and output structure in full.

## Install

These are [Agent Skills](https://www.anthropic.com/news/skills) — `SKILL.md` files with YAML frontmatter that Claude loads automatically based on their `description`. There's no separate "run" step; Claude picks up a matching skill on its own once a request fits its trigger conditions.

### Claude Code — as a plugin (recommended)

This repo ships a `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, so the whole pack installs in one step — all five skills at once:

```
/plugin marketplace add nikhilvdev/job-search-pack
/plugin install job-search-pack
```

This also means the plugin can be listed in any marketplace catalog (official or community) that indexes GitHub repos with a `.claude-plugin/marketplace.json` — see [Optimizing for discovery](#optimizing-for-discovery) below.

### Claude Code — manual skill install (CLI / VS Code / JetBrains extensions)

Each skill lives at `skills/<name>/SKILL.md` inside this repo, so a plain `git clone` of the whole repo won't put `SKILL.md` at a single folder's root — clone once, then symlink (or copy) the specific skill folder(s) you want into your skills directory.

Personal skills (available in every project) — install every skill in the pack:
```bash
git clone https://github.com/nikhilvdev/job-search-pack.git ~/job-search-pack
mkdir -p ~/.claude/skills
for d in ~/job-search-pack/skills/*/; do ln -s "${d%/}" ~/.claude/skills/"$(basename "$d")"; done
```

Or install just one skill:
```bash
git clone https://github.com/nikhilvdev/job-search-pack.git ~/job-search-pack
mkdir -p ~/.claude/skills
ln -s ~/job-search-pack/skills/resume-tailor ~/.claude/skills/resume-tailor
```

Project-only skills (checked into a specific repo, shared with teammates who pull it) — copy rather than symlink so the skill ships with the repo:
```bash
mkdir -p .claude/skills
cp -r ~/job-search-pack/skills/resume-tailor .claude/skills/resume-tailor
```

Either way, the target folder must contain `SKILL.md` at its root. Restart Claude Code (or start a new session) so it re-scans the skills directories — no further setup needed.

### Gemini CLI — as an extension (recommended for Gemini)

This repo also ships a `gemini-extension.json` at its root, pointing at the same `skills/` folder used by the Claude Code plugin — Gemini CLI auto-discovers every `skills/<name>/SKILL.md` bundled inside an installed extension, so no separate Gemini-specific skill files are needed:

```bash
gemini extensions install https://github.com/nikhilvdev/job-search-pack
```

Restart your Gemini CLI session afterward so it picks up the newly installed skills. Gemini's Agent Skills use the same `name`/`description` YAML frontmatter convention as Claude's and are triggered the same way — by natural language matching against each skill's `description`, not by explicit slash commands. Run `/skills` in Gemini CLI to confirm all five are listed.

### claude.ai (web) and Claude Desktop

1. Go to **Settings → Capabilities → Skills** (web) or the equivalent Skills section in Desktop settings.
2. Upload the individual `skills/<name>` folder as a `.zip` (so `SKILL.md` sits at the zip root) — one skill per upload, e.g. zip `skills/resume-tailor/` on its own, not the whole repo.
3. Repeat for each skill you want, and enable each for the conversation/project where you want it available.

### Claude API (Agent Skills via the Files/Skills API)

Upload the specific `skills/<name>` folder (containing that skill's `SKILL.md`) through the Skills API and reference it in your `agent_skills` config when creating a run — one skill per upload. See the [Agent Skills docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) for the exact request shape.

## How to invoke a skill

None of these are slash commands — you don't type `/resume-tailor`. Both Claude Code and Gemini CLI load the matching skill automatically when your request fits the trigger described in that skill's `SKILL.md` frontmatter. Just describe what you want in plain language and attach whatever files are relevant.

**Example trigger phrases, one per skill:**

- **Resume Tailor** — *"Tailor my resume for this job posting"* / *"Will my resume pass the ATS for this role?"* (attach resume + paste or attach the job posting)
- **Cover Letter Writer** — *"Write a cover letter for this Product Manager posting at Acme"* (attach resume + posting/company)
- **LinkedIn Optimizer** — *"Optimize my LinkedIn for a Staff Engineer role"* (attach LinkedIn PDF export)
- **Salary Negotiator** — *"Help me negotiate this offer"* / *"Is $145k competitive for a Staff Engineer in Austin?"* (paste the offer details)
- **Job Tracker** — *"Add this application to my tracker"* / *"What applications need a follow-up?"* (no attachment needed)

**What you get back:** each skill delivers a Markdown file as an attachment, not pasted into chat — open it, and for the multi-option skills (Resume Tailor, Cover Letter Writer, LinkedIn Optimizer, Salary Negotiator) pick the option that fits your voice and ask the assistant to finalize it. Job Tracker instead maintains one running file across sessions.

## Optimizing for discovery

This repo is set up to surface in three separate places people "search for skills":

1. **Claude's own auto-matching** (inside Claude Code / claude.ai / Desktop) — driven entirely by each skill's YAML `description`, one per `skills/<name>/SKILL.md`. Each is written with target phrasings, task synonyms, and example requests spelled out, since Claude matches on that text, not the repo name or README.
2. **Claude Code plugin/marketplace search** — `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` carry `keywords`, `category`, `tags`, `description`, and `author` fields covering all five skills, which is what `/plugin marketplace add` / marketplace browsing indexes on.
3. **Plain GitHub/web search** — driven by the repo's topics and README text, not the plugin manifests. Two things worth doing once, outside of Claude:
   - Set repo topics (Settings → topics, or `gh repo edit --add-topic`) to something like: `claude`, `claude-code`, `claude-skill`, `claude-plugin`, `agent-skills`, `linkedin`, `resume`, `cover-letter`, `salary-negotiation`, `job-tracker`, `ats`, `career`, `job-search`.
   - If you want broader reach, submit the plugin to Anthropic's community marketplace (`anthropics/claude-plugins-community`) per [the plugin docs](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace) — it goes through their validation/safety screening before listing.

## License
See [LICENSE](LICENSE).
