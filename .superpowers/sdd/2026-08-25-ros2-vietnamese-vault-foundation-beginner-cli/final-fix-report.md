# Final fix report

## Scope

- Tightened `sources.lyrical` provenance to published Lyrical documentation and the exact Lyrical branch forms of `ros2/ros2_documentation`.
- Corrected the turtle teleoperation node name to `/teleop_turtle`.
- Normalized the Beginner CLI sources frontmatter and added official Jazzy and Humble tutorial URLs.

## Red-green evidence

### RED

Command:

```console
$ python3 -m unittest tests/test_validate_vault.py -v
```

Exact result:

```text
Ran 16 tests in 0.006s

FAILED (failures=2)
```

The two expected failures were:

```text
FAIL: test_jazzy_docs_source_is_rejected_for_lyrical
AssertionError: False is not true

FAIL: test_raw_lyrical_github_source_is_accepted
AssertionError: Lists differ: ['invalid sources.lyrical official URL'] != []
```

This demonstrated that the former host-only predicate accepted Jazzy under `sources.lyrical` and did not accept the official raw Lyrical source form.

### GREEN

Command:

```console
$ python3 -m unittest tests/test_validate_vault.py -v
```

Exact result:

```text
Ran 16 tests in 0.005s

OK
```

The passing regressions cover a rejected Jazzy `docs.ros.org` URL, an accepted Lyrical published URL (the valid baseline fixture), an accepted Lyrical GitHub blob URL, and an accepted Lyrical raw GitHub URL.

## Full verification

```console
$ python3 -m unittest discover -s tests -v
Ran 16 tests in 0.004s

OK

$ python3 tools/validate_vault.py . --strict
Validated 26 Markdown note(s): no errors.

$ python3 -m json.tool '05 - Tài nguyên/beginner-cli-sources.json' >/dev/null
manifest JSON: exit 0

$ python3 - <<'PY' ...
Manifest coverage: 10 expected ordered entries, 10 unique slugs, all note targets present in index.

$ if rg -n '/turtle_teleop' . -g '*.md' -g '*.py' -g '*.json'; then exit 1; else echo 'Legacy /turtle_teleop occurrences: none'; fi
Legacy /turtle_teleop occurrences: none

$ git diff --check
<no output; exit 0>
```
