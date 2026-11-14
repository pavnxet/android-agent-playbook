<!-- verified-at: initial · 2026-11-14 · postmortems, newest last -->
# INCIDENTS: postmortems

## INCIDENT-001 · "The PDF has broken syntax" · 2026-11-14 · SEV-3 (no damage)
**What happened**: a review pass reported ~24 mangled code strings in the playbook PDF (`provide0kHttp`,
`Dispatchers. 10`, `$<sp="2.3.6"$`, missing `=`, unindented YAML), with page numbers.
**Investigation**: extracted the PDF text layer and searched for each exact string. 23 of 24 were
present and correct; zero LaTeX artifacts existed; none of the "broken" forms existed. The artifacts
matched a vision/OCR pass over a rendered page, not the file.
**Real defect found**: long code lines wrap at page boundaries, so copying from a PDF inserts newlines.
**Fix**: added `docs/CODE_SNIPPETS.md`, generated from the DOCX, and a README warning. No code changed.
**Lesson**: a bug report about document content is verifiable - test the bytes before editing.

## INCIDENT-002 · Three dead repository links circulated as live · 2026-11-14 · SEV-4
**What happened**: three wrapper repositories (`SubhamTyagi/Android-App-Template`,
`nicolas-raoul/Android-WebView-Wrapper`, `nicehash/pwa-to-apk`) were cited as templates; all return 404
via the GitHub API and via `git clone`.
**Fix**: Appendix C documents the dead links and the live alternatives (Capacitor, hand-rolled WebView).
**Lesson**: verify a repository exists before recommending it; a 404 does not say whether a repo is
private, renamed or never existed.

## INCIDENT-003 · `chmod` failed on restored files · 2026-11-14 · SEV-4
**What happened**: restoring the repository from a saved snapshot produced dangling symlinks, so
`chmod +x scripts/init-agent-rules.sh` failed with "Operation not permitted".
**Fix**: copy with dereference (`cp -rL`) so real files land on disk, then set the executable bit.
**Lesson**: after restoring from a snapshot, check `find . -type l` before assuming files are intact.

## INCIDENT-004 · CI failed on a synthetic test fixture · 2026-11-14 · SEV-4 (red build, no damage)
**What happened**: the first push turned the "Secret and PII Safety Scan" workflow red in 14s.
Gitleaks flagged `scripts/verify_repo.py:197`, a test fixture that assigned a key-shaped literal
(a synthetic `sk-` prefixed value, reproduced nowhere in this repository).
Our own scanner had approved it via `scan:allow`; Gitleaks does not read that comment.
**Investigation**: `gh run view --log-failed` -> RuleID `generic-api-key`, entropy 4.12, one leak.
**Fix**: the fixture values are now assembled at runtime (`'sk-' + 'live-' + ...`), so no key-shaped
literal exists in the file; a narrow `.gitleaks.toml` allowlist covers the historical commit so a
full-history scan does not re-report a value that was never a credential. Nothing else allowlisted.
**Lesson**: a local bypass comment is not a CI bypass. Test fixtures must not look like secrets in the
bytes on disk - construct them at runtime instead.

## INCIDENT-005 · Archived libraries recommended as primary picks · 2026-11-14 · SEV-4
**What happened**: a capability list named `arcanegolem/Lycoris` as a ready-to-use PDF viewer and
`android/storage-samples` as a reference; both are archived (2025-02-20 and 2025-08-29). Six further
entries were stale by 1-2.5 years, and one technical claim ("zero AndroidView" in the CameraX demo)
did not survive a code search (30 references).
**Fix**: `docs/FEATURE_RECIPES.md` labels every entry Adopt / Reference only / Archived / Platform with
stars and last push; Part 16 documents what the audit changed.
**Lesson**: a repository that exists is not a repository that works. Check `archived` and `pushed_at`
before recommending, and check the build file before repeating a version claim.

## INCIDENT-006 · Six of twenty extended repositories unusable as cited · 2026-11-14 · SEV-4
**What happened**: of 20 repositories in the extended genre list, three paths returned 404
(`alexstyl/swipeablecard`, `android/play-billing-samples`, `android/health-connect-samples`) and three
were archived (`android/uamp` 2026-01, `osmdroid/osmdroid` 2024-11, `android/location-samples`
2023-08). A fourth, `alexstyl/compose-tinder-card`, is archived too.
**Fix**: registry sections 11-20 carry status labels and a "Dead links and replacements" table;
playbook Part 17 documents the six; replacements are `saket/swipe` + `AnchoredDraggable`,
`googlesamples/play-billing-samples`, `android/health-samples`, `android/media-samples`,
`mapsforge/mapsforge` and `android/platform-samples/samples/location`.
**Lesson**: a 13,000-star repository can be dead. Stars measure history; `archived` and `pushed_at`
measure health. Check both before recommending anything.

## INCIDENT-007 · A true claim I nearly marked false · 2026-11-14 · SEV-4 (process)
**What happened**: `dhruv4740/focuslock` has no README describing UsageStatsManager, AccessibilityService
or overlay blocking, and the manifest path I first probed did not exist (`app/` rather than `android/`).
It looked like an unverifiable claim.
**Investigation**: listed the repository tree - `FocusAccessibilityService`, `OnDemandAccessibility`,
`UsageMonitorService`, `SurfaceBlocker`. The claim is accurate.
**Fix**: registry genre 24 records it as verified *in the source tree*, and the entry says so explicitly.
**Lesson**: absence in a README is not absence in a repository. Before contradicting a claim, check the
source tree - and check the project layout before concluding a file is missing.

## INCIDENT-008 · Two true claims invisible to a README · 2026-11-14 · SEV-4 (process, positive)
**What happened**: `wormaceptor/WormaCeptor` was claimed to expose "44 MCP tools" and
`square/leakcanary` to ship a `shark-dive` agent skill. Neither is in the respective READMEs.
**Investigation**: README grep found 44 tools for WormaCeptor; the LeakCanary README mentions neither
shark-dive nor skills, but the tree contains `.claude/skills/shark-dive/SKILL.md`,
`docs/shark-dive-reference.md` and two shark-dive release workflows.
**Fix**: both recorded as verified, with the note that the evidence is the tree.
**Lesson**: the second instance in one week (see INCIDENT-007). README-first verification produces
false negatives; always list the tree for a claim about tooling or agent integration.

## INCIDENT-009 · This playbook's own CI was 2-3 action majors behind · 2026-11-14 · SEV-3
**What happened**: an audit of 22 CI actions found the playbook's Part 10 workflow pinned
checkout@v4, setup-java@v4, setup-gradle@v4, upload-artifact@v4 and action-gh-release@v2, while the
released majors were v7, v6, v6, v7 and v3. The evidence had been in front of us: this repository's
own CI run printed `Node.js 20 is deprecated, forced to run on Node.js 24` and we treated it as noise.
**Fix**: Part 10 and `.github/workflows/secret-scan.yml` bumped to the verified majors; Part 20 and
registry section 40 document the table; ADR-017 makes tag verification a rule.
**Lesson**: deprecation annotations are a dependency alert, not decoration. If a runner warns that a
runtime is being force-upgraded, the action is stale - check the tag that same day.

## INCIDENT-010 · The registry listed dead repos as live (carried into v2.0) · 2026-11-14 · SEV-4
**What happened**: a v2.0 brief asked for `docs/FEATURE_RECIPES.md` to list 45+ repositories,
including `alexstyl/swipeablecard` (404), `android/play-billing-samples` (404),
`android/health-connect-samples` (404), `android/uamp` (archived), `osmdroid/osmdroid` (archived),
`android/location-samples` (archived) and `arcanegolem/Lycoris` (archived).
**Fix**: the existing registry was kept - it already labels every entry Adopt / Reference only /
Archived / Platform / Does not exist - and a capability index plus a permission-hygiene table were
added on top. Nothing was regressed to satisfy the brief's wording.
**Lesson**: "create file X with content Y" can be a request to regress. When the file already exists
and is more accurate than the spec, improve it in place and say what you declined to change.

## INCIDENT-011 · AGP 9 hard-fails on org.jetbrains.kotlin.android · 2026-11-14 · SEV-2 (build blocked)
**What happened**: the first `verify-starter` run died in 45s with
`Failed to apply plugin 'org.jetbrains.kotlin.android' - no longer required for Kotlin support since
AGP 9.0`. The playbook's own Part 6 convention-plugin example applied exactly that plugin.
**Investigation**: Now in Android's plugin catalog on AGP 9.3.2 carries no `kotlin-android` entry at
all; only `org.jetbrains.kotlin.plugin.compose`, `kotlin-jvm`, `kotlin-serialization`, ksp and hilt.
The `KotlinAndroidProjectExtension` still exists because AGP registers it.
**Fix**: removed from the starter (root, module, catalog) and the build went green; Part 6.1/6.2
corrected and a new Part 6.6 documents the rule with the verbatim error.
**Lesson**: a starter that compiles is worth more than a version table. This contradiction sat in the
playbook for six revisions and only a real build found it.

## INCIDENT-012 · material3 1.5 forces compileSdk 37 and AGP 9.1 · 2026-11-15 · SEV-2 (two CI cycles)
**Reported by**: the agent that built Focus Timer 1.0/2.0 with this playbook.
**Symptom** (verbatim, in this order):
`Dependency 'androidx.compose.material3:material3-ripple-android:1.5.0-rc01' requires libraries and
applications that depend on it to compile against version 37 or later of the Android APIs. :app is
currently compiled against android-36.` - and then, after bumping compileSdk:
`... requires Android Gradle plugin 9.1.0 or higher. This build currently uses Android Gradle plugin 8.13.2.`
**Cause**: AAR metadata inside material3 1.5.x. The Compose BOM does not move material3, so it has to be
pinned - and pinning it silently upgrades the whole toolchain.
**Fix**: compileSdk 37, AGP >= 9.1, Gradle 9.x, no kotlin-android plugin. The chain is now stated in the
README and in both templates.
**Time lost**: 2 CI cycles. **Lesson**: a single dependency can dictate the build system. The README now
carries the chain as one line so an agent can reason forward instead of discovering it backwards.

## INCIDENT-013 · SDK platform ids are versioned from 37 · 2026-11-15 · SEV-3 (one CI cycle)
**Symptom**: `Warning: Failed to find package 'platforms;android-37'` followed by exit code 1.
**Cause**: from API 37 the published platform packages are `platforms;android-37.0`, `37.1`, `37.2` -
a versioned id, not the bare `android-37` every tutorial uses.
**Fix**: install the versioned id, and call sdkmanager by absolute path (it is not on PATH on the runner):
`SDKM="$(ls -d "${ANDROID_HOME:-$ANDROID_SDK_ROOT}"/cmdline-tools/*/bin/sdkmanager | head -1)"`.
Also: `android-actions/setup-android@v3` still tries to install the long-removed `tools` package and
fails; `@v4` works.
**Time lost**: 1 CI cycle.

## INCIDENT-014 · kotlinOptions string DSL is an error on Kotlin 2.3+ · 2026-11-15 · SEV-3
**Symptom**: `Using 'jvmTarget: String' is an error. Please migrate to the compilerOptions DSL.`
**Cause**: Kotlin 2.3 removed the `kotlinOptions { jvmTarget = "17" }` string form.
**Fix**: `kotlin { compilerOptions { jvmTarget.set(JvmTarget.JVM_17) } }`. Note this lives on the Kotlin
extension that AGP 9 registers, not on the Android extension.
**Time lost**: 1 CI cycle.

## INCIDENT-015 · Two API names that no longer exist · 2026-11-15 · SEV-4
**Symptom**: compile errors in code written from memory, not from a snippet file.
**Cause**: `NotificationCompat.Builder.setChronometerCountdown(...)` is `setChronometerCountDown(...)`
(capital D) - verified in androidx source; and Glance's `ActionCallback` is
`androidx.glance.appwidget.action.ActionCallback` (declared in `RunCallbackAction.kt`), not
`androidx.glance.action.ActionCallback`, which contains only `Action`, `ActionParameters`,
`LambdaAction` and `StartActivityAction`. `updateAll` lives in `androidx.glance.appwidget`.
**Fix**: recorded here so the next agent checks the signature instead of the blog post. `javap` on the
AAR settles it in one call (PLAYBOOKS P6, step 3).
