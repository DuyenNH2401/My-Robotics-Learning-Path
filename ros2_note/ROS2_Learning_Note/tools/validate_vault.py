"""Validate the ROS 2 Vietnamese knowledge-vault conventions.

The validator deliberately understands only the small YAML subset used by the
vault frontmatter, so it has no third-party dependency.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_DELIMITER = "---"
EMPTY_WIKILINK = re.compile(r"\[\[\s*(?:\|[^\]]*)?\]\]")
UNFINISHED_MARKERS = re.compile(r"\b(?:TODO|TBD|FIXME)\b|\{\{.+?\}\}|<placeholder>", re.IGNORECASE)
EXCLUDED_DIRECTORIES = {".git", ".obsidian", ".agents", ".codex", "docs", "Attachments", "tools", "tests"}
EXCLUDED_FILENAMES = {"Welcome.md"}


def parse_frontmatter(contents: str) -> tuple[dict[str, object], str]:
    """Return the supported frontmatter mapping and the Markdown body."""
    lines = contents.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
        return {}, contents

    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == FRONTMATTER_DELIMITER)
    except StopIteration:
        return {}, contents

    metadata: dict[str, object] = {}
    current_mapping: dict[str, str] | None = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            if current_mapping is not None and ":" in line:
                key, value = line.strip().split(":", 1)
                current_mapping[key.strip()] = value.strip().strip('"\'')
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value:
            metadata[key] = value.strip('"\'')
            current_mapping = None
        else:
            mapping: dict[str, str] = {}
            metadata[key] = mapping
            current_mapping = mapping
    return metadata, "\n".join(lines[end + 1 :])


def validate_note(path: Path, vault_root: Path) -> list[str]:
    """Return convention violations for one Markdown note."""
    del vault_root  # Reserved for future vault-wide checks.
    contents = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(contents)
    errors: list[str] = []

    if not metadata.get("title") and not re.search(r"^#\s+\S", body, re.MULTILINE):
        errors.append("missing title or H1")
    for key in ("area", "level", "translation-status"):
        if not metadata.get(key):
            errors.append(f"missing {key}")

    distributions = metadata.get("distributions")
    if not isinstance(distributions, dict) or not distributions.get("primary"):
        errors.append("missing distributions.primary")
    sources = metadata.get("sources")
    if not isinstance(sources, dict) or not sources.get("lyrical"):
        errors.append("missing sources.lyrical")

    if EMPTY_WIKILINK.search(contents):
        errors.append("empty wikilink")
    if metadata.get("translation-status") == "complete" and UNFINISHED_MARKERS.search(body):
        errors.append("unfinished placeholder in complete note")
    return errors


def find_markdown_files(vault_root: Path) -> list[Path]:
    """Find vault notes while excluding app metadata, tooling, and project docs."""
    return sorted(
        path
        for path in vault_root.rglob("*.md")
        if not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(vault_root).parts)
        and path.name not in EXCLUDED_FILENAMES
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ROS 2 Vietnamese vault notes.")
    parser.add_argument("vault_root", nargs="?", default=".", type=Path)
    arguments = parser.parse_args()
    vault_root = arguments.vault_root.resolve()
    errors: list[str] = []
    for path in find_markdown_files(vault_root):
        for error in validate_note(path, vault_root):
            errors.append(f"{path.relative_to(vault_root)}: {error}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(find_markdown_files(vault_root))} Markdown note(s): no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
