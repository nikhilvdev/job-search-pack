# linkedin-profile-optimizer

A Claude Skill that audits a LinkedIn profile against a specific target designation (role/title) and produces a decision-support Markdown document with multiple phrasing options per profile area — headline, About, Skills, and each Experience entry — rather than a single prescriptive rewrite.

## Inputs
- **LinkedIn profile export (PDF)** — required
- **Target designation** (e.g. "Staff Engineer", "VP Engineering") — required
- **Resume (PDF)** — optional; if provided, the skill reconciles it against LinkedIn and asks before trusting any metric or project that doesn't appear on LinkedIn itself

## Output
A single `.md` file: `[Name]_LinkedIn_Options_[Designation].md`, containing a brief positioning read followed by 2–4 concrete options per profile area, each with a recommendation.

## Install
Load `SKILL.md` as a Claude Skill (via the "Save skill" prompt when shared, or by placing this folder in your skills directory).

## License
See LICENSE.
