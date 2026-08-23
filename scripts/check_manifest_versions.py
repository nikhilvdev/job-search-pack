#!/usr/bin/env python3
"""Validate the platform manifests are well-formed JSON and their versions agree.

.claude-plugin/plugin.json, gemini-extension.json, and .codex-plugin/plugin.json
each carry an independent 'version' field for their platform (Claude Code,
Gemini CLI, OpenAI Codex CLI). This repo ships one pack, so those three must
always report the same version — this script is what enforces that in CI.
.claude-plugin/marketplace.json has no 'version' field of its own (a
marketplace entry just points at the plugin), so it's checked for valid JSON
only.

Run locally with: python3 scripts/check_manifest_versions.py
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

ALL_MANIFESTS = [
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / "gemini-extension.json",
    ROOT / ".codex-plugin" / "plugin.json",
]

VERSIONED_MANIFESTS = [
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / "gemini-extension.json",
    ROOT / ".codex-plugin" / "plugin.json",
]


def main() -> int:
    errors: list[str] = []
    versions: dict[str, str] = {}

    for path in ALL_MANIFESTS:
        rel = path.relative_to(ROOT)
        if not path.exists():
            errors.append(f"missing manifest: {rel}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: invalid JSON — {e}")
            continue
        if path in VERSIONED_MANIFESTS:
            version = data.get("version")
            if not version:
                errors.append(f"{rel}: missing 'version' field")
            else:
                versions[str(rel)] = version

    distinct_versions = set(versions.values())
    if len(distinct_versions) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in versions.items())
        errors.append(f"version mismatch across manifests: {detail}")

    if errors:
        print("Manifest validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1

    version = next(iter(distinct_versions), "unknown")
    print(f"OK: {len(ALL_MANIFESTS)} manifest(s) validated, version {version} in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
