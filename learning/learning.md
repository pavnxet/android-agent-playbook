<!-- verified-at: initial · 2026-11-14 · edit in place, group by area, no duplicates -->
# LEARNING: durable lessons by area

## [area: android-build]
- AGP 9 removes kapt-era wiring: built-in Kotlin, new DSL, KSP >= 2.3.6, Hilt >= 2.59.2, and four
  obsolete `gradle.properties` flags to delete. Verify with `./gradlew help` and `build --dry-run`.
- The Kotlin daemon property is `kotlin.daemon.jvmargs`, not `kotlin.daemon.jvm.options`; the wrong
  name is silently ignored.
- On a 16 GB machine use `-Xmx3g -Xms512m` plus a 2 GB daemon cap; `-Xms4g` swaps while an editor and
  browser are open.

## [area: android-ui]
- One `UiState` per screen, `stateIn(WhileSubscribed(5_000))`. Multiple independent StateFlows create
  impossible intermediate states.
- `NavHost` is Navigation 2. `NavDisplay` + `@Serializable NavKey` + `rememberNavBackStack` is Nav 3.
- Consume insets exactly once: `Scaffold` innerPadding, or a Material component's own safe area - never
  both. Lists use `contentPadding = innerPadding` + `consumeWindowInsets`.

## [area: android-release]
- Guessed `-keep` rules are how size and startup time are lost; the analyser reports what R8 actually
  kept. Needs `protobuf>=6.33.4`.
- Always archive `mapping.txt` per release, or field stack traces are unreadable.

## [area: docs]
- PDF text layers wrap long lines at page boundaries; copying code from a PDF inserts newlines
  mid-statement. Extract from the DOCX instead (ADR-004, INCIDENT-001).
- A rendered page read by a vision model turns `IO` into `10` and `=` into `$`. Verify claims against
  the text layer before "fixing" a document.

## [area: verification]
- A claim of "the document is broken" is testable: extract the text layer and search for the exact
  string. 23 of 24 alleged breakages did not exist.
- YAML can be validated, not eyeballed: parse it and assert `jobs.*.steps` are mappings.

## [area: agent-process]
- A `SKILL.md` is guidance; the build file and lockfile are ground truth. When they disagree, read the
  build file.
- Do not modularise under five features, and do not let a template contradict that rule (ADR-002).
