<!-- verified-at: initial · 2026-11-14 · append-only; update status in place -->
# DECISIONS: architecture decision records

## ADR-001 · Pin one verified baseline stack · ACCEPTED 2026-11-14
Versions read from `android/nowinandroid` and `cortinico/kotlin-android-template` build files:
AGP 9.3.2, Gradle 9.7.1, Kotlin 2.3, compileSdk 37 (36 fallback), minSdk 24, Compose BOM 2026.x,
Hilt >= 2.59.2, KSP >= 2.3.6.
**Why**: an agent invents versions when none are given; two reference projects disagree, so one
column must be chosen. **Cost**: the matrix dates quickly - re-check at project start.

## ADR-002 · Single module is the default · ACCEPTED 2026-11-14
`templates/AGENTS.md` is single-module, package-by-layer. Multi-module is a documented promotion.
**Why**: Parts 3.2, 13 and 15.1 all warn against modularising a small app, yet an earlier draft of
Appendix A hardcoded 12 modules - the template contradicted the advice. **Cost**: one migration at
the fifth feature, mitigated by the package-to-module mapping table (Part 15.5).

## ADR-003 · Navigation 3, not Navigation 2 · ACCEPTED 2026-11-14
Routes are `@Serializable NavKey` objects rendered by `NavDisplay`, back stack is an observable list.
**Why**: Google's `architecture-templates/base` already ships `NavigationKeys.kt`; Nav 2 graphs would
need migrating. **Cost**: less StackOverflow coverage than Nav 2.

## ADR-004 · Snippets are extracted from the DOCX, never the PDF · ACCEPTED 2026-11-14
`scripts/gen_snippets.py` reads `docs/Android_Engineering_Playbook.docx` and writes
`docs/CODE_SNIPPETS.md`. **Why**: PDF extraction splits long lines at page breaks; a vision pass over
a rendered page reads `IO` as `10` and `=` as `$`. See INCIDENT-001. **Cost**: snippets must be
regenerated after any playbook edit.

## ADR-005 · Adopt the memory + publication-safety layer · ACCEPTED 2026-11-14
Tiered `learning/` memory, `.githooks/`, `scripts/scan_sensitive.py` and the CI secret scan come from
`pavnxet/learnings-for-agents`. **Why**: an Android rules repo is consumed by agents that also need
persistent memory and a fail-closed guard against committing secrets. **Cost**: two protocols to
maintain; the root protocol outranks nothing in the app templates - they are different files.

## ADR-006 · Two `AGENTS.md` files, on purpose · ACCEPTED 2026-11-14
Root `AGENTS.md` = protocol for agents working on THIS repository. `templates/AGENTS.md` = rules for a
USER's Android app, installed by `scripts/init-agent-rules.sh`. **Why**: merging them would ship
protocol boilerplate into every app. **Cost**: must be explained in the README, or it reads as a bug.
The installer refuses to target this repository itself.

## ADR-007 · CI verifies with adb, not an MCP server · ACCEPTED 2026-11-14
MCP device servers need a live device; CI has none. Instrumented verification uses Gradle-managed
devices or a device farm. **Why**: no MCP server can attach to a runner without a device. **Cost**:
the MCP path is only documented for local use (Part 9 and Part 14.2).

## ADR-008 · Scanner ignores env indirection, not the rule · ACCEPTED 2026-11-14
`scan_sensitive.py` suppresses `KEY_ASSIGNMENT` when the value is a reference - `System.getenv(...)`,
`os.environ`, `process.env`, `secrets.*`, `BuildConfig.*` or `${{ secrets.X }}` - because
`storePassword = System.getenv("KEYSTORE_PASSWORD")` is the *safe* pattern, not a leak. Literals are
still caught, and `TOKEN_PREFIX` / `PRIVATE_KEY` / `JWT` rules are unaffected.
**Why**: the first commit was blocked by two false positives on the release-signing snippet; the
alternative (a `// scan:allow` comment in user-facing code) would teach the wrong habit.
**Cost**: `password = System.getenv("X") + "literal"` slips through - acceptable for a docs repo.
**Guard**: `scripts/verify_repo.py` asserts both directions (indirection passes, literals fail).

## ADR-009 · One rule set for every scan mode · ACCEPTED 2026-11-14
`--pre-push` duplicated the pattern loop instead of calling `scan_content()`, so it (a) flagged the
same env-indirection false positives that ADR-008 fixed, and (b) never enforced the private denylist.
It now routes every added diff line through `scan_content()`, the same function `--staged`,
`--commit-msg` and `--all` use.
**Why**: a gate that disagrees with itself trains people to bypass it - the first push was blocked by
two lines the commit gate had already approved.
**Cost**: none; push-time coverage is now a superset of commit-time coverage.
