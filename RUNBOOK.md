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

## One-time, manual step: community marketplace listing

Broader discovery via Anthropic's official community marketplace (`anthropics/claude-plugins-community`) is a one-time PR against *their* repo, reviewed by them for validation/safety — not something to automate or re-run per release, since once listed they resolve the plugin by pointing back at this repo's `main`. See [the plugin docs](https://code.claude.com/docs/en/plugins#submit-your-plugin-to-the-community-marketplace) if this hasn't been done yet.
