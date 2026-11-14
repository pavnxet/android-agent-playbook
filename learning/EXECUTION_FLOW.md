<!-- verified-at: initial · 2026-11-14 · living map; update when structure changes -->
# EXECUTION_FLOW: repository map and context loading

## What this repository is
Documentation and rules. There is no application code and nothing to compile; the "build" is the
PDF/DOCX pair and the snippet file derived from it.

## Map
- `README.md` - entry point: two layers, quick start, verified stack, credits
- `AGENTS.md` - protocol for an agent working in THIS repo (memory, safety, git rules)
- `templates/AGENTS.md` - single-module app rules (1-4 screens) - the default for users
- `templates/AGENTS_multimodule.md` - multi-module app rules (5+ features)
- `docs/Android_Engineering_Playbook.pdf|docx` - the 33-page manual (source of truth)
- `docs/CODE_SNIPPETS.md` - generated from the DOCX; the only safe place to copy code from
- `scripts/init-agent-rules.sh` - installs a template into a user's Android project
- `scripts/gen_snippets.py` - DOCX -> CODE_SNIPPETS.md
- `scripts/verify_repo.py` - links, anchors, fences, YAML parse, shell syntax, installer behaviour
- `scripts/scan_sensitive.py` + `.githooks/` + `.github/workflows/secret-scan.yml` - safety gates
- `learning/` - this memory hierarchy (committed; never ignored)

## Context loading order (cheapest first)
1. `AGENTS.md` Quick Card -> 2. `learning/BRIEF.md` -> 3. `grep -rniE "<keywords>" learning/`
-> 4. the one doc section you need -> 5. the PDF only if the DOCX cannot answer it.

## Verification chain (never claim done without it)
```
python3 scripts/scan_sensitive.py --doctor   # hooks + denylist present
python3 scripts/verify_repo.py               # links, anchors, fences, YAML, shell, installer
bash -n scripts/*.sh                         # POSIX syntax
```
Then, for a user's app, the playbook's own gate:
```
./gradlew assembleDebug --stacktrace && ./gradlew testDebugUnitTest
```
