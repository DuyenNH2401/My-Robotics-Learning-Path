import tempfile
import unittest
from pathlib import Path

from tools.validate_vault import find_markdown_files, validate_note, validate_vault


VALID_FRONTMATTER = """---
aliases: []
tags:
  - ros2
area: tutorials
level: beginner
distributions:
  primary: lyrical
sources:
  lyrical: https://docs.ros.org/en/lyrical/example.html
translation-status: complete
---
"""


class ValidateNoteTests(unittest.TestCase):
    def write_note(self, directory: Path, name: str, contents: str) -> Path:
        path = directory / name
        path.write_text(contents, encoding="utf-8")
        return path

    def test_valid_note_returns_no_errors(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            note = self.write_note(vault_root, "valid.md", VALID_FRONTMATTER + "# Note hợp lệ\n")

            self.assertEqual(validate_note(note, vault_root), [])

    def test_missing_lyrical_source_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            note = self.write_note(
                vault_root,
                "missing-source.md",
                VALID_FRONTMATTER.replace("  lyrical: https://docs.ros.org/en/lyrical/example.html\n", "")
                + "# Thiếu nguồn\n",
            )

            self.assertTrue(any("sources.lyrical" in error for error in validate_note(note, vault_root)))

    def test_placeholder_lyrical_source_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            note = self.write_note(
                vault_root,
                "placeholder-source.md",
                VALID_FRONTMATTER.replace("https://docs.ros.org/en/lyrical/example.html", "URL")
                + "# Nguồn giữ chỗ\n",
            )

            self.assertTrue(any("sources.lyrical" in error for error in validate_note(note, vault_root)))

    def test_official_ros_source_is_accepted(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            note = self.write_note(
                vault_root,
                "official-source.md",
                VALID_FRONTMATTER.replace(
                    "https://docs.ros.org/en/lyrical/example.html",
                    "https://github.com/ros2/ros2_documentation/blob/rolling/source/Tutorials.rst",
                )
                + "# Nguồn chính thức\n",
            )

            self.assertEqual(validate_note(note, vault_root), [])

    def test_similarly_named_github_repository_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            note = self.write_note(
                vault_root,
                "unofficial-source.md",
                VALID_FRONTMATTER.replace(
                    "https://docs.ros.org/en/lyrical/example.html",
                    "https://github.com/ros2/ros2_documentation-evil/blob/main/source/Tutorials.rst",
                )
                + "# Nguồn không chính thức\n",
            )

            self.assertTrue(any("sources.lyrical" in error for error in validate_note(note, vault_root)))

    def test_empty_wikilink_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            note = self.write_note(vault_root, "empty-link.md", VALID_FRONTMATTER + "# Link rỗng\n\n[[]]\n")

            self.assertTrue(any("empty wikilink" in error for error in validate_note(note, vault_root)))

    def test_default_obsidian_welcome_file_is_not_a_vault_note(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(vault_root, "Welcome.md", "Welcome to your new vault!")
            note = self.write_note(vault_root, "lesson.md", VALID_FRONTMATTER + "# Bài học\n")

            self.assertEqual(find_markdown_files(vault_root), [note])

    def test_duplicate_alias_reports_alias_and_each_note_path(self):
        """A shared alias would make a wikilink target ambiguous."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            first = self.write_note(
                vault_root,
                "first.md",
                VALID_FRONTMATTER.replace("aliases: []", "aliases:\n  - Node") + "# First\n",
            )
            second = self.write_note(
                vault_root,
                "second.md",
                VALID_FRONTMATTER.replace("aliases: []", "aliases:\n  - Node") + "# Second\n",
            )

            errors, _warnings = validate_vault(vault_root)

            self.assertIn(
                f"duplicate alias: Node ({first.relative_to(vault_root)}, {second.relative_to(vault_root)})",
                errors,
            )

    def test_unresolved_wikilink_is_a_warning_unless_listed_as_planned(self):
        """A future-plan link is intentional, while an unplanned target needs attention."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(vault_root, "source.md", VALID_FRONTMATTER + "# Source\n\n[[Future note]]\n[[Missing note]]\n")
            self.write_note(
                vault_root,
                "00 - Mục lục ROS 2.md",
                VALID_FRONTMATTER + "# Index\n\n## Planned notes\n\n- [[Future note]]\n",
            )

            errors, warnings = validate_vault(vault_root)

            self.assertEqual(errors, [])
            self.assertEqual(warnings, ["source.md: broken wikilink: [[Missing note]]"])

    def test_missing_heading_fragment_is_an_error(self):
        """A renamed target heading must not leave a silently broken deep link."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(vault_root, "target.md", VALID_FRONTMATTER + "# Target\n\n## Có thật\n")
            self.write_note(vault_root, "source.md", VALID_FRONTMATTER + "# Source\n\n[[target#Không có]]\n")

            errors, warnings = validate_vault(vault_root)

            self.assertEqual(warnings, [])
            self.assertEqual(errors, ["source.md: broken internal heading: [[target#Không có]]"])

    def test_inline_alias_is_a_wikilink_target(self):
        """Existing compact frontmatter aliases remain part of the vault index."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(
                vault_root,
                "target.md",
                VALID_FRONTMATTER.replace("aliases: []", "aliases: [short name]") + "# Target\n",
            )
            self.write_note(vault_root, "source.md", VALID_FRONTMATTER + "# Source\n\n[[short name]]\n")

            errors, warnings = validate_vault(vault_root)

            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_scalar_alias_is_a_wikilink_target(self):
        """A single scalar alias resolves just like a YAML alias list."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(
                vault_root,
                "target.md",
                VALID_FRONTMATTER.replace("aliases: []", "aliases: Short name") + "# Target\n",
            )
            self.write_note(vault_root, "source.md", VALID_FRONTMATTER + "# Source\n\n[[Short name]]\n")

            errors, warnings = validate_vault(vault_root)

            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_missing_local_heading_fragment_is_an_error(self):
        """A local deep link must point to a heading in the same note."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(
                vault_root,
                "source.md",
                VALID_FRONTMATTER + "# Source\n\n## Existing heading\n\n[[#Missing heading]]\n",
            )

            errors, warnings = validate_vault(vault_root)

            self.assertEqual(warnings, [])
            self.assertEqual(errors, ["source.md: broken internal heading: [[#Missing heading]]"])

    def test_existing_local_heading_fragment_is_valid(self):
        """A local wikilink resolves when the destination heading exists."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            vault_root = Path(temporary_directory)
            self.write_note(
                vault_root,
                "source.md",
                VALID_FRONTMATTER + "# Source\n\n## Existing heading\n\n[[#Existing heading]]\n",
            )

            errors, warnings = validate_vault(vault_root)

            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()
