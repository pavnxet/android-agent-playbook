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

## ADR-010 · Test fixtures are assembled, never literal · ACCEPTED 2026-11-14
`verify_repo.py` builds its fake credential strings at runtime (`'sk-' + 'live-' + ...`) instead of
embedding them. `.gitleaks.toml` extends the default ruleset and allowlists only those two synthetic
values, with the reason recorded inline.
**Why**: Gitleaks scans file bytes and does not honour `scan:allow`, so a literal fixture is
indistinguishable from a real leak to CI (INCIDENT-004).
**Cost**: one extra config file. **Guard**: the allowlist matches exact synthetic strings, not paths,
so a real key pasted into any file is still caught.

## ADR-011 · Capability registry lives in a generated-safe file · ACCEPTED 2026-11-14
`docs/FEATURE_RECIPES.md` holds the capability -> library registry. It is hand-maintained, unlike
`docs/CODE_SNIPPETS.md`, which `scripts/gen_snippets.py` overwrites from the DOCX.
**Why**: the registry is prose and judgement, not extractable code; putting it in the generated file
would delete it on the next regeneration. The playbook carries the decision layer (Part 16), the
registry carries the per-repository detail.
**Cost**: two places to update when a library changes status - Part 16 and the registry.
**Guard**: `scripts/verify_repo.py` checks both files' links and anchors.

## ADR-012 · Status column beats a recommendation list · ACCEPTED 2026-11-14
Every registry entry is labelled Adopt / Reference only / Archived / Platform, with stars and last
push. Two of the 22 cited repositories were already archived when the list reached us.
**Why**: a bare list of repositories ages into misinformation; a status column makes staleness visible
at the point of use. **Cost**: re-verification is manual, quarterly.

## ADR-013 · Registry is 20 genres, and every entry carries a status · ACCEPTED 2026-11-14
`docs/FEATURE_RECIPES.md` now covers 20 genres (10 capability, 10 app genre) and every entry is
labelled Adopt / Adopt (alternative) / Reference only / Archived / Platform / Does not exist.
**Why**: six of the 20 extended repositories were unusable as cited (3 x 404, 3 x archived, plus an
archived author library), and a bare list cannot express that. **Cost**: two files to update per
change (registry + Part 16/17). **Guard**: the "Dead links and replacements" table plus the
one-line `gh api` re-verification command in the registry.

## ADR-014 · Study-app genres are clusters, not libraries · ACCEPTED 2026-11-14
The 25 study genres are grouped into 13 clusters in `docs/FEATURE_RECIPES.md` (genres 21-33) and
playbook Part 18, and five clusters deliberately have **no library**: MCQ/PYQ/error-log is a Room
schema, and OCR/AI/sync/PDF cross-reference existing entries.
**Why**: a 25-row table invites an agent to add 25 dependencies; a cluster table invites it to add the
two that matter. **Cost**: the reader must follow cross-references. **Guard**: the offline-first rules
in Part 18.3 outrank any library choice.

## ADR-015 · Inspectors are debug-only, and that is a security rule · ACCEPTED 2026-11-14
WormaCeptor, Chucker and LeakCanary are `debugImplementation` only, with no-op artefacts in release and
any local port or MCP endpoint bound to localhost.
**Why**: an inspector exposes HTTP payloads, Room tables and DataStore contents over a local endpoint.
In a release build that is a data-exfiltration surface carrying this app's package name.
**Cost**: release builds need the no-op variants and cannot be inspected in the field.
**Guard**: the dependency block in Part 19.1 is the canonical wiring; review any PR that adds an
`implementation` inspector.

## ADR-016 · Circuit and Orbit are replacements, not add-ons · ACCEPTED 2026-11-14
The registry marks both as "replaces Parts 3-4" and forbids stacking them on this playbook's
ViewModel + StateFlow + NavKey pattern.
**Why**: each ships its own presenter/ViewModel, navigation and test story; running both produces two
sources of truth for screen state. **Cost**: adopting one is a project-level decision, not a dependency.

## ADR-017 · Action pins are verified by release tag, not by memory · ACCEPTED 2026-11-14
Every `uses:` in the playbook and in this repository's own workflows is set to the latest released
major, checked with `gh api repos/OWNER/REPO/releases/latest`. Renovate groups `github-actions`
updates weekly to keep them there.
**Why**: Part 10 was two to three majors behind on four of five actions, and this repository's CI
printed `Node.js 20 is deprecated` as proof. A stale pin fails slowly, not loudly.
**Cost**: majors can break inputs - read the release notes on a bump. **Guard**: Part 20.2 and the
registry section 40 record the verified tags with dates.

## ADR-018 · Signing location is a documented choice, not an accident · ACCEPTED 2026-11-14
Two supported paths: external signing (`r0adkll/sign-android-release`, signs the artifact after
Gradle) or internal signing (env-var `signingConfig`, signs during the build, Part 7.1).
**Why**: external signing keeps secrets out of the build file but means the artifact you tested is not
the artifact you ship; internal signing keeps them identical but puts the keystore path in the build.
**Cost**: a project must state which one it uses. **Guard**: Part 20.3 step 3.

## ADR-019 · The starter is a build proof, not a template · ACCEPTED 2026-11-14
`starter/` is a one-screen app on the exact pinned baseline, compiled and tested by
`.github/workflows/verify-starter.yml` on every change to that folder. It is not what
`scripts/init-agent-rules.sh` installs - that remains `templates/AGENTS.md`.
**Why**: a version matrix nobody compiles drifts; a compiled one cannot. The two roles are different
(a proof must stay minimal, a template must stay adaptable), so they are separate artefacts.
**Cost**: two places to bump when the baseline moves (Part 2 and `starter/gradle/libs.versions.toml`).
**Guard**: the starter README states the pairing rule; CI fails if the pinned stack stops building.

## ADR-020 · Prompts live in PROMPTS.md, next to the rules · ACCEPTED 2026-11-14
Five copy-paste prompts with `[bracketed]` variables cover scaffold, vertical slice, modularisation,
release gate and crash loop. `init-agent-rules.sh` installs PROMPTS.md alongside AGENTS.md.
**Why**: rules tell an agent *how* to write code; a prompt tells it *what* to do now, with the
evidence command attached. Every prompt ends with "paste the real output".
**Cost**: prompts age with the playbook - re-read them when a Part changes.

## ADR-021 · Local-path detection requires an absolute path · ACCEPTED 2026-11-14
`LOCAL_USER_PATH_UNIX` now asserts that a unix home-directory path (the home and Users roots) is not
preceded by a word character or another slash. Relative source paths such as `ui/home/HomeUiState.kt` therefore pass,
while an absolute home-directory path (for example a keystore under a user's home folder) is still
caught.
**Why**: the starter README table names `ui/home/HomeUiState.kt`, which the old pattern read as a home
directory and blocked the commit (same class of false positive as ADR-008).
**Cost**: none. **Guard**: three regression cases in `scripts/verify_repo.py` (one negative, two positive).

## ADR-022 · Built-in Kotlin replaces the kotlin-android plugin on AGP 9 · ACCEPTED 2026-11-14
The version catalog and every module must not apply `org.jetbrains.kotlin.android`. Compose keeps
`org.jetbrains.kotlin.plugin.compose`; JVM-only modules keep `org.jetbrains.kotlin.jvm`.
**Why**: AGP 9 fails the build outright (INCIDENT-011). **Cost**: none - there is no replacement to
apply. **Guard**: `starter/` is the compiled proof; if it builds, the wiring is right.

## ADR-023 · The baseline table is verified weekly by a script, not by memory · ACCEPTED 2026-11-15
`scripts/check_versions.py` fetches `maven-metadata.xml` for every row of the README baseline table and
fails if a pinned version is unpublished or a newer stable exists. `.github/workflows/verify-versions.yml`
runs it weekly and on demand. The table also carries a "hypothesis, not a pin" warning, and the chain
`material3 -> compileSdk -> AGP -> Gradle -> built-in Kotlin` is stated once, in one line.
**Why**: a real build reported that every structural rule held while every number needed re-checking.
A table that cannot rot is worth more than a table that is right today.
**Cost**: one network call per row per week. **Guard**: the weekly workflow plus `starter/` compiling the
same numbers.

## ADR-024 · Defaults vs available, stated separately · ACCEPTED 2026-11-15
The README separates what every app gets (Compose, Material 3, Nav 3, one StateFlow per screen, injected
dispatchers) from what an app adds when it needs it (Room, DataStore, Retrofit, Hilt, WorkManager).
**Why**: a four-screen timer read the stack as a checklist and nearly installed Room, Retrofit and Hilt.
**Cost**: none.

## ADR-025 · starter/gradle/libs.versions.toml is the single source of versions · ACCEPTED 2026-11-15
Every document that states a version mirrors the starter catalog: README, PROMPTS.md, both templates,
the playbook's Part 2/6.1/Appendix A and therefore CODE_SNIPPETS.md. `scripts/verify_repo.py` reads the
catalog and fails on any mirror that disagrees or on a known-stale string.
**Why**: the repo contradicted itself in ten places within one day of a version bump (INCIDENT-017).
**Cost**: a version bump is now one file plus a rebuild; the guard names every file that still lies.
**Guard**: `python3 scripts/verify_repo.py` (runs in lint-repo.yml on every push).

## ADR-026 · The compiled column wins · ACCEPTED 2026-11-15
Part 2 keeps the two reference-project columns for reading their code, and adds a fourth column for this
repository's baseline. When they disagree, the fourth wins - not because it is newer, but because it is
the only one compiled on every push.
**Why**: a reader had no way to tell which of two tables was authoritative. **Cost**: a five-column
table. **Guard**: starter/ + verify-starter.yml.
