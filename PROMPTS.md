# Prompts

Five copy-paste prompts that pair the rules in [`templates/AGENTS.md`](templates/AGENTS.md) with the code in [`docs/CODE_SNIPPETS.md`](docs/CODE_SNIPPETS.md) and the library picks in [`docs/FEATURE_RECIPES.md`](docs/FEATURE_RECIPES.md).

Replace every `[bracketed]` value. Each prompt is written to be pasted whole — the last line of every one tells the agent how to prove it finished, because "done" without a command is an opinion.

**Before the first prompt**, install the rules once:

```bash
./scripts/init-agent-rules.sh /path/to/your-app          # single module (1-4 screens)
./scripts/init-agent-rules.sh /path/to/your-app --multimodule   # 5+ features
```

---

## 1 · Scaffold a new 1–4 screen Android app

Use when the project is empty and the app is small. Single module, package-by-layer, no premature modularisation.

```text
Scaffold a new Android app in [PROJECT_PATH] called [APP_NAME], package [com.example.app].

Rules: read AGENTS.md in the project root (installed from
pavnxet/android-agent-playbook templates/AGENTS.md) and follow it exactly. Code comes from
docs/CODE_SNIPPETS.md; capability libraries come from docs/FEATURE_RECIPES.md.

Stack, pinned - do not invent versions:
- AGP 9.5.1, Gradle 9.9.1, Kotlin 2.4.21, KSP 2.3.14, Hilt 2.60.1
- compileSdk 37, minSdk 24; do NOT apply org.jetbrains.kotlin.android (built into AGP 9)
- Compose BOM 2026.09.00 + material3 1.5.0-rc01 pinned (the BOM does not move material3)
- Navigation 3 1.2.1; Room 2.8.5, DataStore, Retrofit + OkHttp, kotlinx.serialization only if needed

Structure (single module, package by layer):
- ui/theme/{Color,Type,Theme}.kt
- ui/navigation/{NavigationKeys.kt, Navigation.kt}
- ui/screens/[feature]/{[Feature]Screen.kt, [Feature]ViewModel.kt, [Feature]UiState.kt}
- data/local/, data/remote/, data/repository/, domain/model/, di/

gradle.properties: use the 16 GB profile from CODE_SNIPPETS.md (gradle.properties) -
-Xmx3g -Xms512m, kotlin.daemon.jvmargs=-Xmx2g, parallel + caching + configuration cache
with problems=fail.

Screens: [SCREEN_ONE], [SCREEN_TWO], [SCREEN_THREE].
Per screen: one immutable UiState in a StateFlow started with WhileSubscribed(5_000),
one-shot effects in a Channel, SavedStateHandle for user input, injected @IoDispatcher.

Tests: one unit test per state transition with StandardTestDispatcher + Turbine and a fake
repository (no mocks). Add a Room entity/DAO/repository for [FIRST_ENTITY].

Prove it: run ./gradlew assembleDebug --stacktrace and ./gradlew testDebugUnitTest, paste
the real output, and list every file you created.
```

---

## 2 · Add a vertical feature slice from FEATURE_RECIPES.md

Use when the app exists and you want one capability wired end to end.

```text
Add a vertical slice for [CAPABILITY] (e.g. "PDF export", "QR scanner", "charts") to
[PROJECT_PATH].

1. Open docs/FEATURE_RECIPES.md and find the section for [CAPABILITY]. Use the entry marked
   "Adopt" (or "Adopt as reference"). If the entry is "Archived", "Reference only" or
   "Does not exist", stop and tell me which live alternative you are using instead and why.
2. Read AGENTS.md for the architecture rules and docs/CODE_SNIPPETS.md for the patterns.

Implement, top to bottom:
- ui/screens/[feature]/[Feature]UiState.kt - one immutable data class (or sealed interface)
- ui/screens/[feature]/[Feature]ViewModel.kt - StateFlow<UiState> via
  stateIn(viewModelScope, WhileSubscribed(5_000), initial), Channel<[Feature]Effect> for
  one-shot events, SavedStateHandle for anything the user typed
- data/repository/[Feature]Repository.kt - the only path to data; Room is the source of
  truth, the network writes into Room; inject @IoDispatcher
- ui/screens/[feature]/[Feature]Screen.kt - stateless content composable + a stateful
  [Feature]Route that collects with collectAsStateWithLifecycle()
- add the library dependency to gradle/libs.versions.toml, not to a build file inline

Do not add a permission unless the recipe's section explicitly requires it. If it does,
declare it in the module that uses it and say so in your summary.

Tests: one test per state transition, plus one for the error path. Fakes over mocks.

Prove it: ./gradlew testDebugUnitTest and ./gradlew lintDebug, paste the real output, and
name the recipe entry you followed.
```

---

## 3 · Promote a single-module app to multi-module

Use at the fifth feature, not before. This is mechanical — nothing is rewritten.

```text
Promote [PROJECT_PATH] from single-module to multi-module.

Rules: switch AGENTS.md to templates/AGENTS_multimodule.md from
pavnxet/android-agent-playbook, and follow its dependency rules exactly.

Target graph:
- :app - Application, MainActivity, top-level NavDisplay, DI entry points
- :core:model (pure JVM), :core:data, :core:database, :core:network,
  :core:designsystem, :core:ui, :core:navigation, :core:common, :core:testing
- :feature:[name]:api (NavKey + contract), :feature:[name]:impl (screen, ViewModel, DI)

Split mechanically, using the package-to-module mapping in playbook Part 15.5:
ui/theme -> :core:designsystem; ui/navigation -> :core:navigation + feature api;
ui/screens/[feature] -> :feature:[feature]:impl; domain/model -> :core:model;
data/local -> :core:database; data/remote -> :core:network; data/repository -> :core:data;
di/ -> each module's own di/ package.

Rules that must hold afterwards:
- dependencies point inward (feature -> core -> model); a core module never imports a feature
- no feature depends on another feature's impl
- only :app and a feature's own impl see that impl module
- nothing Android-framework-specific in :core:model

Add convention plugins in build-logic for application, library, compose, hilt and room so
module build files stay under ~10 lines. Do not change behaviour: the app must look and
behave identically after the split.

Prove it: ./gradlew assembleDebug testDebugUnitTest, then ./gradlew :app:dependencies to
show the graph has no cycles, and paste the real output.
```

---

## 4 · Pre-release security, R8 and Play policy gate

Use before the first upload, and before every production promotion.

```text
Run the pre-release gate on [PROJECT_PATH] for release [VERSION_NAME] ([VERSION_CODE]).

1. R8 keep rules - do not guess. Run:
   ./gradlew :app:analyzeReleaseR8Config          (AGP >= 9.3; needs protobuf >= 6.33.4)
   Report what R8 actually kept, and justify every -keep rule you propose adding in a
   comment next to it. Never add rules until a crash stops.
2. Release build integrity: ./gradlew bundleRelease assembleRelease --stacktrace, then
   install the minified release build and confirm it starts. Archive mapping.txt.
3. Secrets: no keystore, password, API key or token in the repository or in any tracked
   file. Signing material comes from environment variables (see CODE_SNIPPETS.md, Release
   signing). Run python3 scripts/scan_sensitive.py --all if this repo has the safety kit.
4. OWASP MASVS spot-check: exported components have permissions or are intentionally
   public; no sensitive data in logs; tokens in EncryptedSharedPreferences or the Keystore;
   cleartext traffic disabled; WebView JS disabled unless required.
5. Play Data Safety: list every permission in AndroidManifest.xml and every data type the
   app collects, and check each one is declared in the store listing. Flag anything
   declared but unused, and anything used but undeclared.
6. Policy blockers: REQUEST_INSTALL_PACKAGES (self-update) is not allowed for Play-
   distributed apps; BIND_ACCESSIBILITY_SERVICE needs a stated purpose; background location
   needs a justification.

Output a table: check | status (PASS / FAIL / NEEDS DECISION) | evidence (the command and
its real output). Do not claim PASS without evidence.
```

---

## 5 · Headless CLI and logcat crash diagnosis loop

Use when a build installs but crashes, or when behaviour differs on device.

```text
Diagnose the crash in [PACKAGE_NAME] on the connected device. Work headlessly - no
Android Studio.

Loop:
1. adb logcat -c                                  # clear the buffer
2. ./gradlew assembleDebug --stacktrace           # build
3. adb install -r app/build/outputs/apk/debug/app-debug.apk
4. adb shell am start -n [PACKAGE_NAME]/.MainActivity
5. sleep 3; adb shell dumpsys activity activities | grep -i mResumedActivity
   -> if the launcher is in the foreground, the app died on launch. Do not continue.
6. adb logcat -d > crash.txt
   grep -nE "AndroidRuntime|FATAL|Caused by:" crash.txt
7. Read the LAST "Caused by:" line - that is the root exception. The lines above it are
   framework frames; the lines below are wrapped causes.
8. Map it: ClassNotFoundException at startup -> missing R8 keep rule or bad DI graph;
   Resources$NotFoundException -> bad id or missing density; NullPointerException in a
   composable -> state read before initialisation; NetworkOnMainThreadException -> a
   dispatcher was not injected.
9. Fix the cause, not the symptom. Re-run the loop from step 1.

If the UI itself is the question, prefer structure over pixels:
  adb exec-out uiautomator dump /dev/tty      (or: android layout)
  adb exec-out screencap -p > screen.png      (only when appearance matters)

Stop and ask me after three distinct failed fixes rather than guessing a fourth.

Report: the root cause in one sentence, the evidence line from logcat, the change you made,
and the command that proves the crash is gone.
```
