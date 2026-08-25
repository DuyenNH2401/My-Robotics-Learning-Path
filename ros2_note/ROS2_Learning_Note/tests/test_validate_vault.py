import tempfile
import unittest
from pathlib import Path

from tools.validate_vault import find_markdown_files, validate_note


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


if __name__ == "__main__":
    unittest.main()
