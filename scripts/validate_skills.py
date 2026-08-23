#!/usr/bin/env python3
"""Validate every skills/<name>/SKILL.md has a usable YAML frontmatter block.

Checks, per skill:
  - SKILL.md exists
  - a '---' ... '---' frontmatter block is present
  - 'name' is set and matches the containing folder name
  - 'description' is set and long enough to carry real trigger phrasing

Run locally with: python3 scripts/validate_skills.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
MIN_DESCRIPTION_LEN = 40


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[3:end].strip("\n").splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def main() -> int:
    errors: list[str] = []
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())

    if not skill_dirs:
        errors.append(f"no skill directories found under {SKILLS_DIR}")

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue

        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        if fields is None:
            errors.append(f"{skill_dir.name}: SKILL.md has no '---' YAML frontmatter block")
            continue

        name = fields.get("name", "")
        if not name:
            errors.append(f"{skill_dir.name}: frontmatter missing 'name'")
        elif name != skill_dir.name:
            errors.append(
                f"{skill_dir.name}: frontmatter name '{name}' does not match folder name"
            )

        description = fields.get("description", "")
        if not description:
            errors.append(f"{skill_dir.name}: frontmatter missing 'description'")
        elif len(description) < MIN_DESCRIPTION_LEN:
            errors.append(
                f"{skill_dir.name}: description is only {len(description)} chars "
                f"(< {MIN_DESCRIPTION_LEN}) — too short to carry real trigger phrasing"
            )

    if errors:
        print("SKILL.md validation failed:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {len(skill_dirs)} skill(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
