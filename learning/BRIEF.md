<!-- verified-at: initial · 2026-11-14 · rewritten whole, not appended -->
# BRIEF: cold-start summary

## State (≤ 5 lines)
`android-agent-playbook` is a documentation + rules repository, not an app. It holds a 33-page
Android engineering playbook (PDF + DOCX), two `AGENTS.md` app templates, 20 verified code
snippets, and this memory/safety layer. Content verified 14 November 2026 against source repos.

## Active work / handoff
- S-20261114-0004 · DONE · next: publish v1.0.0, then keep the version matrix current · blocked on: none

## Top pitfalls (≤ 10, most expensive to rediscover first)
- docs: never copy code from the PDF; extract from the DOCX -> `docs/CODE_SNIPPETS.md` [area: docs]
- android: AGP 9 hard-requires KSP >= 2.3.6 and Hilt >= 2.59.2; older versions fail the build [area: android-build]
- android: `NavHost` is Navigation 2; a 2026 stack uses `NavDisplay` + `@Serializable NavKey` [area: android-ui]
- android: a ViewModel survives rotation, not process death - typed input needs `SavedStateHandle` [area: android-ui]
- android: `-keep` rules are guessed until proven - run `:app:analyzeReleaseR8Config` first [area: android-release]
- android: do not modularise under 5 features; `templates/AGENTS.md` is the single-module default [area: android-arch]
- naming: root `AGENTS.md` = protocol for THIS repo; `templates/AGENTS.md` = rules for a USER's app [area: docs]
- security: `learning/` is committed, so it must never contain secrets, real names or local paths [area: security]

## Verified commands
- safety doctor: `python3 scripts/scan_sensitive.py --doctor` (~1s)
- self-check: `python3 scripts/verify_repo.py` (~1s)
- regenerate snippets: `python3 scripts/gen_snippets.py` (needs `python-docx`)

## Where to look (task -> place)
- Android rules an agent must follow -> `templates/AGENTS.md` / `templates/AGENTS_multimodule.md`
- exact code, Gradle, YAML -> `docs/CODE_SNIPPETS.md`
- why a decision was made -> `learning/DECISIONS.md`
- what went wrong before -> `learning/INCIDENTS.md`
- task recipes -> `learning/PLAYBOOKS.md`
- tool choices -> `learning/TOOLS.md`
