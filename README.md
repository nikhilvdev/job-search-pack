# linkedin-profile-optimizer

A Claude Skill that audits a LinkedIn profile against a specific target designation (role/title) and produces a decision-support Markdown document with multiple phrasing options per profile area — headline, About, Skills, and each Experience entry — rather than a single prescriptive rewrite.

See [SKILL.md](SKILL.md) for the full skill definition (trigger conditions, step-by-step process, output structure).

## Inputs
- **LinkedIn profile export (PDF)** — required
- **Target designation** (e.g. "Staff Engineer", "VP Engineering") — required
- **Resume (PDF)** — optional; if provided, the skill reconciles it against LinkedIn and asks before trusting any metric or project that doesn't appear on LinkedIn itself

## Output
A single `.md` file: `outputs/[Name]_LinkedIn_Options_[Designation].md`, containing a brief positioning read followed by 2–4 concrete options per profile area, each with a recommendation.

## Install

This is an [Agent Skill](https://www.anthropic.com/news/skills) — a `SKILL.md` file with YAML frontmatter that Claude loads automatically based on its `description`. There's no separate "run" step to install; you place the folder where the surface you're using looks for skills, and Claude picks it up on its own once the request matches.

### Claude Code (CLI / VS Code / JetBrains extensions)

Personal skills (available in every project):
```bash
mkdir -p ~/.claude/skills
git clone <this-repo-url> ~/.claude/skills/linkedin-profile-optimizer
```

Project-only skill (checked into a specific repo, shared with teammates who pull it):
```bash
mkdir -p .claude/skills
git clone <this-repo-url> .claude/skills/linkedin-profile-optimizer
```

Either way, the folder must contain `SKILL.md` at its root (it does). Restart Claude Code (or start a new session) so it re-scans the skills directories — no further setup needed.

### claude.ai (web) and Claude Desktop

1. Go to **Settings → Capabilities → Skills** (web) or the equivalent Skills section in Desktop settings.
2. Upload this folder as a `.zip`, or point the "Add skill" flow at `SKILL.md` directly if a file picker is offered.
3. Enable the skill for the conversation/project where you want it available.

### Claude API (Agent Skills via the Files/Skills API)

Upload `SKILL.md` (and this folder) through the Skills API and reference it in your `agent_skills` config when creating a run. See the [Agent Skills docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) for the exact request shape — the skill package itself (this repo) doesn't change between surfaces.

## How to invoke it

This skill is **not** a slash command — you don't type `/linkedin-profile-optimizer`. Claude loads it automatically when your request matches the trigger described in `SKILL.md`'s frontmatter. Just describe what you want in plain language and attach the PDF(s).

**It will trigger on requests like:**
- "Optimize my LinkedIn for a Staff Engineer role" *(+ attach LinkedIn PDF export)*
- "How does my profile look for a VP Engineering position?"
- "Help me reposition my LinkedIn for a Product Management pivot"
- "Review this LinkedIn export against the Senior Engineering Manager title"
- Attaching just a LinkedIn PDF with no resume and asking "what should I change to target [role]?"

**What to provide:**
1. Your LinkedIn profile export as a PDF ([Me → Resources → Save to PDF](https://www.linkedin.com/) on your own profile), attached to the message.
2. The exact target designation/title you're optimizing for — be specific ("Staff Engineer" not "a promotion").
3. *(Optional but recommended)* Your resume as a PDF, if it has more detail (metrics, projects) than what's currently on LinkedIn.

**Example prompt:**
> Here's my LinkedIn export and resume. Optimize my profile for a "Head of Product" role — I'm currently a Senior PM and want to make the case for the jump.

If you only give a target designation with no PDF, Claude will ask for the LinkedIn export before proceeding — it won't work from a resume alone, since recruiters search against LinkedIn's actual live field values.

**What you get back:** a single Markdown file (`outputs/[Name]_LinkedIn_Options_[Designation].md`) delivered as an attachment/file, not pasted into chat — open it, pick the options that match your voice, and ask Claude to write the final copy for whichever ones you choose.

## License
See [LICENSE](LICENSE).
