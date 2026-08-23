# Publishing Runbook

How a change to this pack goes live on Claude Code, Gemini CLI, and OpenAI Codex CLI, and what's automated vs. manual.

## The core fact: there's no registry

Unlike npm or PyPI, none of the three platforms pull from a package registry — they all install straight from this GitHub repo:

- Claude Code: `.claude-plugin/marketplace.json` points its one plugin entry at `source: "./"` — the repo root.
- Gemini CLI: `gemini extensions install <repo-url>` clones the repo directly.
- OpenAI Codex CLI: `codex plugin marketplace add owner/repo` clones the repo directly.

So **merging to `main` is the publish step** for all three. There is no separate "build and publish" action to run — CI's job is to stop a broken change from reaching `main` in the first place, since `main` is what every platform reads from a moment later.

## What CI checks automatically

[`.github/workflows/validate.yml`](.github/workflows/validate.yml) runs on every push and PR to `main`:

1. [`scripts/validate_skills.py`](scripts/validate_skills.py) — every `skills/<name>/SKILL.md` has a `---` frontmatter block, a non-empty `name` that matches its folder name, and a `description` long enough to actually carry trigger phrasing (each platform's auto-matching is driven entirely by that field).
2. [`scripts/check_manifest_versions.py`](scripts/check_manifest_versions.py) — `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `gemini-extension.json`, and `.codex-plugin/plugin.json` are all valid JSON, and the three that carry an independent `version` field (`.claude-plugin/plugin.json`, `gemini-extension.json`, `.codex-plugin/plugin.json`) report the **same** version. This is the thing most likely to silently drift, since it means editing three files in three different formats for one version bump.

Run both locally before opening a PR:
```bash
python3 scripts/validate_skills.py
python3 scripts/check_manifest_versions.py
```

[`.github/workflows/release.yml`](.github/workflows/release.yml) runs when a tag matching `v*` is pushed — it creates a GitHub Release with auto-generated notes from the commits/PRs since the last tag. This isn't required for updates to reach users (see above), but it gives anyone who pins to a specific ref (`--ref`, `@<tag>`) something to point at, and leaves a changelog trail.

## Maintainer checklist for shipping a change

1. Edit the skill(s) under `skills/<name>/SKILL.md` and/or the platform manifests.
2. If the change is user-facing (new skill, changed behavior, new platform support), bump `version` in all three of:
   - `.claude-plugin/plugin.json`
   - `gemini-extension.json`
   - `.codex-plugin/plugin.json`

   Keep them identical — CI fails the PR otherwise (`check_manifest_versions.py`).
3. Open a PR. `validate.yml` runs automatically; fix anything it flags.
4. Merge to `main`. That's live for all three platforms at this point.
5. For a version bump worth a changelog entry, tag and push it:
   ```bash
   git tag v2.1.0
   git push origin v2.1.0
   ```
   This triggers `release.yml`, which creates the GitHub Release.

## How users already on each platform actually get the update

Merging to `main` makes the new content available to install, but existing installs don't necessarily refresh themselves instantly — each platform has its own pull model:

- **Claude Code** — since 2.0.70, marketplaces support per-marketplace auto-update, and Claude Code refreshes the marketplace clone before a `plugin@marketplace` lookup regardless. On older versions, users may need to re-add the marketplace or reinstall the plugin to pick up a change.
- **Gemini CLI** — updates are pulled explicitly: `gemini extensions update job-search-pack`, or install with `--auto-update` up front. Either way, the CLI does not hot-reload — the user needs to restart their Gemini CLI session for the update to take effect.
- **OpenAI Codex CLI** — `codex plugin marketplace upgrade` (optionally scoped to a specific marketplace name) refreshes the marketplace's `plugin.json` from the configured ref; the user then reinstalls/updates the plugin from the `/plugins` browser and restarts Codex to pick it up.

None of this is something this repo's CI can push through to a user's machine — it's worth stating in a release's notes when a change is meaningful enough that people should manually re-sync (e.g. "run `gemini extensions update job-search-pack` to get this").

## Getting listed so people can find it without already having the repo URL

Installing already works today with just the repo URL/slug (`/plugin marketplace add nikhilvdev/job-search-pack`, `gemini extensions install <url>`, `codex plugin marketplace add nikhilvdev/job-search-pack`) — none of this is required to make the pack *usable*. It's only for making it *discoverable* to people who aren't already looking at this repo.

### Claude: submit to `claude-community`

This is a **web-form submission, not a PR** — there's no file to edit in `anthropics/claude-plugins-community` directly, and it can't be scripted from here since it's a login-gated form; a human has to click through it.

1. Run `claude plugin validate .` from the repo root first — the review pipeline runs the identical check on submission. (Confirmed passing as of the last run in this repo.)
2. Submit via one of:
   - [claude.ai/admin-settings/directory/submissions/plugins/new](https://claude.ai/admin-settings/directory/submissions/plugins/new) — requires a Team/Enterprise org with directory management access.
   - [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit) — for individual authors not on a Team/Enterprise org (this is the one that applies to a personal repo like this one).
3. Automated safety screening + review runs after submission. Once approved, the plugin is pinned to a commit SHA in `anthropics/claude-plugins-community`'s `marketplace.json`, and Anthropic's CI auto-bumps that pin as new commits land on `main` — so re-submission isn't needed for ordinary updates. The public catalog syncs nightly, so there's a lag between approval and the plugin actually showing up; check by searching the [community catalog](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json) directly.
4. There's a separate, Anthropic-curated `claude-plugins-official` marketplace with no public application process — Anthropic adds plugins to it at their own discretion, not from the submission form above.

### Gemini: auto-discovered by the official Extensions Gallery — no form, no PR

Unlike the other two, this one needs no submission step at all — [geminicli.com/extensions](https://geminicli.com/extensions/) crawls public GitHub repos daily and lists anything that qualifies, automatically. Two requirements, both already satisfied by this repo:

1. `gemini-extension.json` must sit at the repo root (it does — see [gemini-extension.json](gemini-extension.json)).
2. The repo's GitHub **About** topics must include the exact topic `gemini-cli-extension` — that's the tag the crawler filters on. **Done**: added via `gh repo edit --add-topic gemini-cli-extension` (swapped out for `career-change`, since GitHub caps repos at 20 topics and this one is a functional requirement, not just a search keyword).

Nothing further to do here — just wait for the next daily crawl. If it doesn't show up within a few days, re-check that both conditions above still hold (a topic can get dropped if the repo's topic list is ever reset wholesale rather than edited incrementally).

### OpenAI Codex: no equivalent public curated-submission process (yet)

Unlike Claude, [`openai/skills`](https://github.com/openai/skills) doesn't document a public process for a third party to get into its `.curated/` tier (installable by name, e.g. `$skill-installer linear`) — that tier reads as OpenAI-curated. Its `.experimental/` tier ("community and exploratory skills, installed by folder path or GitHub URL") is the closer fit, and the closest verified path there is opening a PR against `openai/skills` adding an entry that points at this repo — which requires signing their CLA on the PR. That repo isn't ours to edit directly, so this is also a manual, human step, not something CI here can do. In the meantime, `codex plugin marketplace add nikhilvdev/job-search-pack` already works standalone with no listing required.
