"""Validate the ROS 2 Vietnamese knowledge-vault conventions.

The validator deliberately understands only the small YAML subset used by the
vault frontmatter, so it has no third-party dependency.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import urlparse


FRONTMATTER_DELIMITER = "---"
EMPTY_WIKILINK = re.compile(r"\[\[\s*(?:\|[^\]]*)?\]\]")
WIKILINK = re.compile(
    r"\[\[\s*(?:(?P<target>[^\]|#]+?)(?:#(?P<heading>[^\]|]+))?|#(?P<local_heading>[^\]|]+))(?:\|[^\]]*)?\s*\]\]"
)
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
UNFINISHED_MARKERS = re.compile(r"\b(?:TODO|TBD|FIXME)\b|\{\{.+?\}\}|<placeholder>", re.IGNORECASE)
EXCLUDED_DIRECTORIES = {".git", ".obsidian", ".agents", ".codex", "docs", "Attachments", "tools", "tests"}
EXCLUDED_FILENAMES = {"Welcome.md"}


def is_official_ros_source(value: object) -> bool:
    """Return whether a source URL is an official ROS 2 Lyrical source."""
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    if parsed.scheme != "https":
        return False
    if parsed.netloc == "docs.ros.org":
        return parsed.path.startswith("/en/lyrical/")
    if parsed.netloc == "raw.githubusercontent.com":
        return parsed.path.startswith("/ros2/ros2_documentation/lyrical/")
    if parsed.netloc == "github.com":
        return (
            parsed.path.startswith("/ros2/ros2_documentation/blob/lyrical/")
            or parsed.path.startswith("/ros2/ros2_documentation/tree/lyrical/")
        )
    return False


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
    current_key: str | None = None
    for index, line in enumerate(lines[1:end], 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")):
            value = line.strip()
            container = metadata.get(current_key) if current_key else None
            if isinstance(container, list) and value.startswith("- "):
                container.append(value[2:].strip().strip('"\''))
            elif isinstance(container, dict) and ":" in value:
                key, value = value.split(":", 1)
                container[key.strip()] = value.strip().strip('"\'')
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if value:
            if value == "[]":
                metadata[key] = []
            elif value.startswith("[") and value.endswith("]"):
                metadata[key] = [item.strip().strip('"\'') for item in value[1:-1].split(",") if item.strip()]
            else:
                metadata[key] = value.strip('"\'')
            current_key = None
        else:
            # A blank frontmatter key may introduce either a YAML list or a
            # small string mapping.  The first indented line determines it.
            next_line = lines[index + 1] if index + 1 < end else ""
            if next_line.lstrip().startswith("- "):
                sequence: list[str] = []
                metadata[key] = sequence
            else:
                mapping: dict[str, str] = {}
                metadata[key] = mapping
            current_key = key
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
    elif not is_official_ros_source(sources["lyrical"]):
        errors.append("invalid sources.lyrical official URL")

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


def _link_targets(contents: str) -> list[tuple[str, str | None]]:
    """Return non-empty wikilink note targets and optional heading fragments."""
    return [
        (
            (match.group("target") or "").strip(),
            (match.group("heading") or match.group("local_heading") or "").strip() or None,
        )
        for match in WIKILINK.finditer(contents)
    ]


def _planned_notes(vault_root: Path) -> set[str]:
    """Read future note titles from the index's `Planned notes` section."""
    index = vault_root / "00 - Mục lục ROS 2.md"
    if not index.exists():
        return set()
    planned: set[str] = set()
    in_section = False
    for line in index.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_section = line[3:].strip().casefold() == "planned notes"
            continue
        if in_section:
            planned.update(target for target, _heading in _link_targets(line))
    return planned


def _headings(contents: str) -> set[str]:
    return {match.group(1).strip().casefold() for match in HEADING.finditer(contents)}


def _aliases(metadata: dict[str, object]) -> list[str]:
    """Normalize supported scalar and list alias forms without accepting mappings."""
    aliases = metadata.get("aliases", [])
    if isinstance(aliases, str):
        return [aliases]
    if isinstance(aliases, list):
        return [alias for alias in aliases if isinstance(alias, str)]
    return []


def validate_vault(vault_root: Path) -> tuple[list[str], list[str]]:
    """Validate cross-note aliases and wikilink destinations in a vault."""
    notes = find_markdown_files(vault_root)
    errors: list[str] = []
    warnings: list[str] = []
    targets: dict[str, list[Path]] = {}
    contents_by_path: dict[Path, str] = {}

    for path in notes:
        contents = path.read_text(encoding="utf-8")
        contents_by_path[path] = contents
        metadata, _body = parse_frontmatter(contents)
        targets.setdefault(path.stem.casefold(), []).append(path)
        for alias in _aliases(metadata):
            targets.setdefault(alias.casefold(), []).append(path)

    for target, paths in sorted(targets.items()):
        unique_paths = sorted(set(paths))
        if len(unique_paths) > 1:
            display = next(
                alias
                for path in unique_paths
                for alias in [path.stem]
                if alias.casefold() == target
            ) if any(path.stem.casefold() == target for path in unique_paths) else None
            if display is None:
                for path in unique_paths:
                    metadata, _body = parse_frontmatter(contents_by_path[path])
                    aliases = _aliases(metadata)
                    display = next((alias for alias in aliases if alias.casefold() == target), target)
                    break
            rendered_paths = ", ".join(str(path.relative_to(vault_root)) for path in unique_paths)
            errors.append(f"duplicate alias: {display} ({rendered_paths})")

    planned = {title.casefold() for title in _planned_notes(vault_root)}
    for source_path, contents in contents_by_path.items():
        for target, heading in _link_targets(contents):
            matches = [source_path] if not target else targets.get(target.casefold(), [])
            source = source_path.relative_to(vault_root)
            if not matches:
                message = f"broken wikilink: [[{target}]]"
                if target.casefold() in planned:
                    continue
                warnings.append(f"{source}: {message}")
                continue
            if len(set(matches)) > 1:
                errors.append(f"{source}: ambiguous wikilink: [[{target}]]")
                continue
            if heading and heading.casefold() not in _headings(contents_by_path[matches[0]]):
                errors.append(f"{source}: broken internal heading: [[{target}#{heading}]]")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate ROS 2 Vietnamese vault notes.")
    parser.add_argument("vault_root", nargs="?", default=".", type=Path)
    parser.add_argument("--strict", action="store_true", help="treat unresolved wikilinks as errors")
    arguments = parser.parse_args()
    vault_root = arguments.vault_root.resolve()
    errors: list[str] = []
    for path in find_markdown_files(vault_root):
        for error in validate_note(path, vault_root):
            errors.append(f"{path.relative_to(vault_root)}: {error}")
    cross_vault_errors, warnings = validate_vault(vault_root)
    errors.extend(cross_vault_errors)
    for warning in warnings:
        print(f"warning: {warning}")
    if arguments.strict:
        errors.extend(warnings)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated {len(find_markdown_files(vault_root))} Markdown note(s): no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
