<!-- verified-at: initial · 2026-11-14 · append recipes; keep each under 20 lines -->
# PLAYBOOKS: task recipes

## P1 · Add a feature to a user's Android app
1. `./scripts/init-agent-rules.sh <app> [--multimodule]` if the rules are not installed yet.
2. Read `templates/AGENTS.md` rules + the relevant block in `docs/CODE_SNIPPETS.md`.
3. Create `ui/screens/<feature>/{Screen, ViewModel, UiState}`; one `StateFlow<UiState>`.
4. Data path: repository -> Room (source of truth); network writes into Room.
5. Write one unit test per state transition (snippet 12), then `./gradlew testDebugUnitTest`.

## P2 · Triage a crash reported by an agent or a user
1. `adb logcat -c` then launch, then `adb logcat -d | grep -E "AndroidRuntime|FATAL|Caused by:"`.
2. Read the **last** `Caused by:` - that is the root, not the framework frames above it.
3. ClassNotFound at startup -> suspect a missing R8 keep rule; Resources$NotFound -> bad id/density.
4. Confirm the foreground activity is yours before believing the launch succeeded.

## P3 · Ship a release
1. `./gradlew :app:analyzeReleaseR8Config` before adding any `-keep` rule.
2. Sign from env vars (snippet 10); never commit a keystore.
3. `./gradlew bundleRelease` -> upload the AAB to the internal track first.
4. Archive `mapping.txt`; install one minified build on a device before promoting.

## P4 · Update the playbook
1. Edit the build scripts in the DOCX source, or the DOCX directly.
2. Re-render: `soffice --headless --convert-to pdf docs/Android_Engineering_Playbook.docx`.
3. Regenerate snippets: `python3 scripts/gen_snippets.py`.
4. `python3 scripts/verify_repo.py` must pass before commit.

## P5 · Add a lesson learned
1. Does it change a decision? -> `DECISIONS.md` (ADR, status).
2. Is it a pitfall worth never rediscovering? -> `BRIEF.md` top pitfalls + `learning.md` area.
3. Is it a one-off event? -> `summary.md` entry (append-only), `INCIDENTS.md` if it caused damage.

## P6 · Version archaeology in three minutes
1. List published versions:
   `curl -s https://dl.google.com/dl/android/maven2/<group/path>/<artifact>/maven-metadata.xml | tr '<' '\n' | grep '^version>' | tail -12`
   (Maven Central for Kotlin, KSP, Hilt, Coroutines; `services.gradle.org/versions/current` for Gradle.)
2. Pick the highest stable (ignore alpha/beta/rc unless a feature needs it), then read its AAR metadata -
   this is what tells you the required compileSdk and AGP:
   `unzip -p <artifact>.aar META-INF/com/android/build/gradle/aar-metadata.properties`
3. Confirm the API you are about to call actually exists:
   `javap -classpath classes.jar androidx.compose.material3.MaterialThemeKt` (or the class in question).
   This one step would have caught both API-name errors in INCIDENT-015.

`scripts/check_versions.py` automates step 1 for every row of the README table; it runs weekly in CI.
