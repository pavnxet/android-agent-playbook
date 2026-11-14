# Feature recipes: capability → verified library

The lookup table an agent should read **before** writing a feature. Twenty genres plus a study-app cluster, one repository per genre, with the status checked on 14 November 2026 and the Android APIs each one actually uses.

**How to use this file.** Name the capability, then read only that repository's entry. If the entry says *reference only* or *archived*, read it for the pattern and write the code yourself against the current API — do not add it as a dependency.

**The governing rule** (same as the playbook): prefer the platform API, then AndroidX, then a third-party library. A library is justified only where no official API exists, and only while it is alive.

| Status | Meaning |
|---|---|
| **Adopt** | Maintained, current toolchain, safe as a dependency |
| **Reference only** | Read the pattern, write your own — stale, tiny, or a sample |
| **Archived** | Do not use; the owner has retired it |
| **Platform** | No library needed — use the AndroidX/official API directly |

---

## 1 · Compose → PDF

| Repository | Status | Take from it |
|---|---|---|
| [jksalcedo/compose-to-pdf](https://github.com/jksalcedo/compose-to-pdf) | **Adopt** — 32★, pushed 2026-09-30, AGP 9.4.1 / Gradle 9.6 / Compose BOM 2026.09.00 | Renders Compose UI straight to a multi-page vector PDF via `PdfDocument`; no HTML or XML step |
| [big-jared/kmpdf](https://github.com/big-jared/kmpdf) | **Adopt** — 11★, pushed 2026-11-11 | Standard page sizes (A4/Letter/A5), loops for dynamic reports, byte-array export you can upload |
| [Chethan616/Artefact](https://github.com/Chethan616/Artefact) | **Reference only** — 537★, pushed 2026-11-14, **Rust core** | Merge, split, sign, and DOCX/XLSX/PPTX viewing — but adopting it means adopting a Rust toolchain |
| [arcanegolem/Lycoris](https://github.com/arcanegolem/Lycoris) | **Archived** (2025-02-20) | Nothing. For viewing, use `androidx.pdf:pdf-viewer` (alpha) or an external viewer intent |

Permissions: none for app-storage output. Use SAF only when the user picks the destination.

## 2 · In-app updates from GitHub Releases

| Repository | Status | Take from it |
|---|---|---|
| [pavi2410/kmp-app-updater](https://github.com/pavi2410/kmp-app-updater) | **Adopt** — 35★, pushed 2026-04-13 | The only maintained option: pluggable update sources, GitHub Releases included |
| [supersu-man/apkupdater-library](https://github.com/supersu-man/apkupdater-library) | **Reference only** — 18★, pushed 2026-01-05 | `/releases/latest` tag vs `versionName`, download and install-prompt wiring |
| [azzadpandit1122/AutoUpdateSdk](https://github.com/azzadpandit1122/AutoUpdateSdk) | **Reference only** — 2★, no push since 2025-09 | Compose update UI ideas; not a dependency you want to own |
| [Trilokia/publishly-android](https://github.com/Trilokia/publishly-android) | **Reference only** — 0★, pushed 2026-10-25 | "What's new" release-notes UI; brand new, unproven |

**Policy gate:** `REQUEST_INSTALL_PACKAGES` + self-updating is fine for APKs distributed outside Play, and a Play policy violation inside it. If the app ships on Play, use the Play In-App Update API instead. Always verify a checksum or signature before installing, compare versions from the tag (not the release title), and fail closed on an unparseable tag.

## 3 · Camera capture

| Repository | Status | Take from it |
|---|---|---|
| [android/camera-samples](https://github.com/android/camera-samples) | **Platform** — 5,469★, pushed 2026-11-03 | Official, Compose-first CameraX and Camera2 samples; the reference to copy |
| [ioannisa/CameraX-Composable-Demo](https://github.com/ioannisa/CameraX-Composable-Demo) | **Reference only** — 27★, pushed 2026-04-25, CameraX 1.6.0 | Photo capture, front/back switch, tap-to-focus, pinch-zoom. Its "zero `AndroidView`" claim does not hold — a code search finds 30 references |

Permissions: `CAMERA` + a camera feature declaration; request at first use and keep the rest of the app usable when denied.

## 4 · Gallery picking, cropping, compression

| Repository | Status | Take from it |
|---|---|---|
| [ismoy/ImagePickerKMP](https://github.com/ismoy/ImagePickerKMP) | **Adopt** — 233★, pushed 2026-11-10 | Camera + gallery picking, multi-select, crop, compress, EXIF extraction in one Compose API |

Permissions: none on API 33+ with the Android Photo Picker. Do not request `READ_MEDIA_IMAGES` unless you have a legacy path that genuinely needs it.

## 5 · Multipart upload with progress

| Repository | Status | Take from it |
|---|---|---|
| [raheemadamboev/ktor-client-upload-file](https://github.com/raheemadamboev/ktor-client-upload-file) | **Reference only** — 0★, pushed 2024-12-26 | The `onUpload` → ViewModel → progress-bar wiring. Write the client yourself against current Ktor |

Sketch: `MultiPartFormDataContent` + `onUpload { sent, total -> }` → a `StateFlow<Float>` in the ViewModel → `LinearProgressIndicator`. Cancellation is the coroutine's `Job`, not a library feature.

## 6 · Notifications, WorkManager, foreground services

| Repository | Status | Take from it |
|---|---|---|
| [NicosNicolaou16/SampleForegroundService](https://github.com/NicosNicolaou16/SampleForegroundService) | **Adopt as reference** — 12★, pushed 2026-06-19, compileSdk/targetSdk 37 | Android 14+ `foregroundServiceType` declarations, persistent notifications, boot receivers |
| [google-developer-training/…workmanager](https://github.com/google-developer-training/basic-android-kotlin-compose-training-workmanager) | **Platform** — 49★, pushed 2026-11-10 | Work chains, constraints, status notifications |

Permissions: `POST_NOTIFICATIONS` (runtime, API 33+) and `FOREGROUND_SERVICE` + the typed permission such as `FOREGROUND_SERVICE_DATA_SYNC`. The type must be declared **and** justified on Android 14+.

## 7 · QR / barcode

| Repository | Status | Take from it |
|---|---|---|
| [carllosnc/qrdroid](https://github.com/carllosnc/qrdroid) | **Adopt as reference** — 0★, pushed 2026-11-10 | Full app: CameraX `ImageAnalysis` + ML Kit barcode 17.3.0, Navigation 3, generator too |

Permissions: `CAMERA` — the same prompt the camera feature uses.

## 8 · Rich text and Markdown

| Repository | Status | Take from it |
|---|---|---|
| [MohamedRejeb/compose-rich-editor](https://github.com/MohamedRejeb/compose-rich-editor) | **Adopt** — 1,867★, pushed 2026-11-11 | `RichTextState`, HTML and Markdown import/export, undo/redo, image embedding |

## 9 · Storage, permissions, biometrics

| Repository | Status | Take from it |
|---|---|---|
| [google/accompanist](https://github.com/google/accompanist) | **Platform, maintenance mode** — 7,852★, pushed 2025-08-18 | `accompanist-permissions` (`rememberPermissionState`) is still the pragmatic answer. Do not adopt its pager or navigation modules — those were upstreamed and are deprecated |
| [android/storage-samples](https://github.com/android/storage-samples) | **Archived** (2025-08-29) | Read for SAF / `MediaStore` / `FileProvider` patterns, then write against current docs |
| [arnab-kundu/Storage](https://github.com/arnab-kundu/Storage) | **Reference only** — 2★, 2025-10-06 | Small scoped-storage and zip/unzip example; predates current policy |
| [pranaypatel512/BiometricAuthentication](https://github.com/pranaypatel512/BiometricAuthentication) | **Reference only** — 2★, 2024-11 | `BiometricPrompt` wiring. Use `androidx.biometric:biometric` directly |
| [quangchien99/Biometrics-Helper](https://github.com/quangchien99/Biometrics-Helper) | **Reference only** — 0★, 2024-05 | Crypto-bound biometric auth; 2.5 years stale, read only |

Permissions: `USE_BIOMETRIC`; SAF pickers need no permission at all.

## 10 · On-device generative AI

| Repository | Status | Take from it |
|---|---|---|
| [android/ai-samples](https://github.com/android/ai-samples) | **Platform** — 724★, pushed 2026-11-03 | Official; includes the `jetpacker` sample. ML Kit GenAI, Gemini Nano summarization and image description, with cloud fallback patterns |

---

## Handing a capability to an agent

Name the capability, the repository, and the rules file — in that order:

> Implement PDF export with `jksalcedo/compose-to-pdf` (see `docs/FEATURE_RECIPES.md`), and the GitHub release check with `pavi2410/kmp-app-updater`. Follow the MVVM + StateFlow rules in `AGENTS.md`: one `UiState` per screen, effects in a `Channel`, injected dispatcher, one unit test per state transition. Write to app storage first; use SAF only when the user picks a destination.

Two libraries for one job is how a module ends up with a Ktor client and a Retrofit client, both half-wired. One capability, one repository, one entry in this table.

## Re-verifying

```bash
# status of every repository in this file
gh api repos/OWNER/REPO --jq '"\(.stargazers_count)★ \(.pushed_at[0:10]) archived=\(.archived)"'
```

Re-run it quarterly, or before you add a dependency. Two of the twenty-two in this list were already archived when it was written.

---

# Extended genres

Ten more app categories. Same rule: one repository per genre, status checked before it is recommended.

## 11 · Audio and video streaming

| Repository | Status | Take from it |
|---|---|---|
| [android/media-samples](https://github.com/android/media-samples) | **Platform** — 1,379★, pushed 2026-11-03 | Official Media3 samples: Compose video player, Picture-in-Picture, background `MediaSessionService` |
| [android/uamp](https://github.com/android/uamp) | **Archived** (last push 2026-01-09) | Nothing new — 13,160 stars of history, and Media3 replaced its entire architecture. Read `media-samples` instead |

Permissions: `FOREGROUND_SERVICE` + `FOREGROUND_SERVICE_MEDIA_PLAYBACK` + `POST_NOTIFICATIONS`. The media type is mandatory on Android 14+.

## 12 · Charts, analytics, expense dashboards

| Repository | Status | Take from it |
|---|---|---|
| [patrykandpatrick/vico](https://github.com/patrykandpatrick/vico) | **Adopt** — 3,206★, pushed 2026-11-13 | Line, column and combo charts with markers, zoom and scroll; the most maintained Compose charting library |
| [ehsannarmani/ComposeCharts](https://github.com/ehsannarmani/ComposeCharts) | **Adopt (alternative)** — 922★, pushed 2026-07-30 | Animated pie, donut, line and bar charts with minimal setup |

One of the two, not both. `vico` if you need cartesian zoom and custom markers; `ComposeCharts` if you need a pie or donut quickly.

## 13 · Maps, GPS, offline navigation

| Repository | Status | Take from it |
|---|---|---|
| [maplibre/maplibre-native](https://github.com/maplibre/maplibre-native) | **Adopt** — 2,316★, pushed 2026-11-14 | GPU vector tiles, custom styles, offline regions, no API key or per-call billing |
| [mapsforge/mapsforge](https://github.com/mapsforge/mapsforge) | **Adopt (alternative)** — 1,424★, pushed 2026-10-28 | Offline `.map` archives and rendering — the live successor to the osmdroid approach |
| [osmdroid/osmdroid](https://github.com/osmdroid/osmdroid) | **Archived** (2024-11-20) | Read for `.mbtiles`/`.zip` archive handling, then use Mapsforge or MapLibre |
| [android/location-samples](https://github.com/android/location-samples) | **Archived** (2023-08-23) | Nothing — predates the current permission model. Use `android/platform-samples/samples/location` |

Permissions: `ACCESS_FINE_LOCATION` (+ `ACCESS_COARSE_LOCATION`), `INTERNET`. `ACCESS_BACKGROUND_LOCATION` only for genuine background tracking, and Play requires a written justification for it.

## 14 · Home-screen widgets and Quick Settings tiles

| Repository | Status | Take from it |
|---|---|---|
| [android/platform-samples](https://github.com/android/platform-samples) | **Platform** — 1,762★, pushed 2026-11-14 | Jetpack Glance app widgets, Quick Settings tiles, share-sheet targets, plus `samples/location` |

Widgets are a separate composition surface: `GlanceAppWidget` + `GlanceAppWidgetReceiver`, no Compose UI tree sharing. Update them through WorkManager or a repository Flow, never from the UI process directly.

## 15 · Bluetooth LE and USB serial hardware

| Repository | Status | Take from it |
|---|---|---|
| [NordicSemiconductor/Android-BLE-Library](https://github.com/NordicSemiconductor/Android-BLE-Library) | **Adopt** — 2,429★, pushed 2026-10-13 | GATT over coroutines and Flow; removes the classic threading bugs |
| [mik3y/usb-serial-for-android](https://github.com/mik3y/usb-serial-for-android) | **Adopt** — 5,723★, pushed 2026-11-10 | USB-OTG serial for Arduino, ESP32, CP210x, CH340 |

Permissions: `BLUETOOTH_SCAN` + `BLUETOOTH_CONNECT` (runtime, API 31+). USB needs no manifest permission — it needs a `device_filter` intent and a per-device system dialog.

## 16 · Swipe card decks and swipe-to-action rows

| Repository | Status | Take from it |
|---|---|---|
| [saket/swipe](https://github.com/saket/swipe) | **Adopt** — 857★, pushed 2026-03-09 | Swipe-to-reveal list actions with spring physics and haptic thresholds |
| [alexstyl/compose-tinder-card](https://github.com/alexstyl/compose-tinder-card) | **Archived** (2024-06-26) | Read the deck gesture maths, then implement with Compose Foundation `AnchoredDraggable` |
| `alexstyl/swipeablecard` (as commonly cited) | **Does not exist** (404) | — |

A card deck is `AnchoredDraggableState` with four anchors plus a fling threshold. That is a platform primitive now; a library buys you very little.

## 17 · Authentication, passkeys, cloud sync

| Repository | Status | Take from it |
|---|---|---|
| [android/identity-samples](https://github.com/android/identity-samples) | **Platform** — 522★, pushed 2026-11-03 | Credential Manager: FIDO2 passkeys, Sign in with Google, password autofill |
| [supabase-community/supabase-kt](https://github.com/supabase-community/supabase-kt) | **Adopt** — 853★, pushed 2026-11-13 | Auth, PostgREST, Realtime, Storage over Ktor |
| [firebase/quickstart-android](https://github.com/firebase/quickstart-android) | **Platform** — 9,344★, pushed 2026-11-14 | Auth, Firestore, FCM, Remote Config |

Pick one backend. Two sync clients in one module is the most expensive kind of duplication to unwind later.

## 18 · Vector animation and skeleton loaders

| Repository | Status | Take from it |
|---|---|---|
| [airbnb/lottie-android](https://github.com/airbnb/lottie-android) | **Adopt** — 35,771★, pushed 2026-02-15 | `lottie-compose` for After Effects JSON animations |
| [valentinilk/compose-shimmer](https://github.com/valentinilk/compose-shimmer) | **Adopt** — 1,087★, pushed 2026-07-09 | Synchronised shimmer placeholders for loading states |

Skeletons belong to the `Loading` branch of your `UiState` — not to a separate "is shimmering" flag. One state machine, one truth.

## 19 · In-app purchases and subscriptions

| Repository | Status | Take from it |
|---|---|---|
| [googlesamples/play-billing-samples](https://github.com/googlesamples/play-billing-samples) | **Platform** — 34★, pushed 2026-10-05 | One-time purchases, subscriptions, acknowledgement, restore |
| `android/play-billing-samples` (as commonly cited) | **Does not exist** (404) | The samples moved to the `googlesamples` organisation |

Permissions: `com.android.vending.BILLING`. No runtime prompt, but test purchases need a licence-tester account. Always acknowledge a purchase within three days or it is refunded automatically.

## 20 · Offline OCR and on-device ML

| Repository | Status | Take from it |
|---|---|---|
| [googlesamples/mlkit](https://github.com/googlesamples/mlkit) | **Platform** — 4,310★, pushed 2026-10-26 | TextRecognition (Latin and Devanagari), on-device translation, face detection, pose |
| [android/health-samples](https://github.com/android/health-samples) | **Platform** — 351★, pushed 2026-09-16 | Health Connect, health-platform-v1 and health-services samples |
| `android/health-connect-samples` (as commonly cited) | **Does not exist** (404) | `android/health-samples` |

OCR runs offline once the model is present; the first use downloads it unless you bundle it. Health Connect needs per-data-type consent through its own UI, and every type you request is a Play declaration.

---

## Dead links and replacements

Six of the twenty repositories in the extended batch cannot be used as cited. Verify before you recommend:

```bash
gh api repos/OWNER/REPO --jq '"\(.stargazers_count)★ \(.pushed_at[0:10]) archived=\(.archived)"'
```

| Cited | Reality | Replacement |
|---|---|---|
| `alexstyl/swipeablecard` | 404 — never existed at that path | `saket/swipe`; `AnchoredDraggable` for decks |
| `alexstyl/compose-tinder-card` | Archived 2024-06 | same as above |
| `android/play-billing-samples` | 404 — moved | `googlesamples/play-billing-samples` |
| `android/health-connect-samples` | 404 | `android/health-samples` |
| `android/uamp` | Archived 2026-01 | `android/media-samples` |
| `osmdroid/osmdroid` | Archived 2024-11 | `mapsforge/mapsforge` or `maplibre/maplibre-native` |
| `android/location-samples` | Archived 2023-08 | `android/platform-samples/samples/location` |

**Why this table exists**: a 13,000-star repository can be dead. Stars measure history, not health — `archived` and `pushed_at` measure health.

---

# Study and EdTech genres

Twenty-five study-app genres collapse into thirteen clusters, mapped to 18 repositories. Five of them already appear above (`compose-to-pdf`, `googlesamples/mlkit`, `android/ai-samples`, `supabase-community/supabase-kt`, `android/architecture-templates`) and are cross-referenced rather than repeated.

**The spine is the same for all of them**: Room is the source of truth, the UI observes Room, the network is an optional writer. See playbook Part 18.3.

## 21 · Flashcards and spaced repetition

| Repository | Status | Take from it |
|---|---|---|
| [bootuz/azri-android](https://github.com/bootuz/azri-android) | **Reference only** — 1★, pushed 2026-10-21, AGP 9.2.1 | A real FSRS-6 implementation, nested deck folders, reverse cards, daily queues. One star, so read the algorithm, do not inherit the app |
| [jvsena42/loopky](https://github.com/jvsena42/loopky) | **Reference only** — 12★, pushed 2026-11-12 | Anki `.apkg` and `.csv` import, Again/Hard/Good/Easy intervals, pronunciation checks, two-pane tablet layout |

FSRS state is the one thing you cannot recompute: persist the review log in Room and derive scheduling from it.

## 22 · MCQ simulators, PYQ banks, error logbooks

No library needed. This is a Room schema plus a timer:

- `question(id, topic, difficulty, negativeMark, sourceYear, bodyJson)` — `kotlinx.serialization` for options and explanation
- `attempt(questionId, chosenOption, correct, secondsSpent, markedForReview, timestamp)`
- `errorLog(questionId, reason, revisionDue)` — filtered views for "wrong", "unattempted", "silly mistake"
- One `StateFlow<TestUiState>` per test session, a `Channel` for the submit effect, and a `SavedStateHandle` so a killed process does not lose the attempt.

## 23 · Pomodoro, focus analytics, habits

| Repository | Status | Take from it |
|---|---|---|
| [nsh07/Tomato](https://github.com/nsh07/Tomato) | **Adopt as reference** — 1,539★, pushed 2026-11-13 | Material 3 Expressive UI, Room 3.0.3, Vico 3.3.1 charts, peak-hour analytics, Android 16 Live Updates |

Note the forward signal: Tomato runs **Room 3.0.3** while the playbook baseline pins 2.8.3. Both work; plan the migration.

## 24 · App and distraction blocking

| Repository | Status | Take from it |
|---|---|---|
| [dhruv4740/focuslock](https://github.com/dhruv4740/focuslock) | **Reference only** — 0★, pushed 2026-11-09 | `FocusAccessibilityService`, `UsageMonitorService` (UsageStatsManager), `SurfaceBlocker` overlay, friction gates. Verified in the source tree, not the README |

Permissions: `PACKAGE_USAGE_STATS` (special access), `SYSTEM_ALERT_WINDOW`, and an accessibility service the user must enable manually. Play scrutinises accessibility use — declare a genuine purpose or expect removal.

## 25 · Stylus notes and infinite canvas

| Repository | Status | Take from it |
|---|---|---|
| [allient/folio](https://github.com/allient/folio) | **Adopt as reference** — 16★, pushed 2026-11-11 | Pressure and tilt brushes, 35 paper templates, minimap, lasso-to-text, side-by-side book + notebook |
| [alexdremov/notate](https://github.com/alexdremov/notate) | **Reference only** — 63★, pushed 2026-08-29 | Quadtree stroke indexing, level-of-detail tile caching, shape snapping, scribble-to-erase. Built for **Onyx Boox e-ink** devices — read it for the canvas, not the input model |

## 26 · PDF and EPUB reading, annotation

| Repository | Status | Take from it |
|---|---|---|
| [Acclorite/book-story](https://github.com/Acclorite/book-story) | **Adopt as reference** — 1,428★, pushed 2026-11-05 | Material You reader, **six** formats (pdf, epub, fb2, html, md, txt), chapters, categories, SAF |

Six formats, not seven: there is no `.mobi` or `.azw3` support to promise.

## 27 · YouTube lecture chapters

| Repository | Status | Take from it |
|---|---|---|
| [PierfrancescoSoffritti/android-youtube-player](https://github.com/PierfrancescoSoffritti/android-youtube-player) | **Adopt** — 3,704★, pushed 2026-11-13 | IFrame wrapper with `seekTo(seconds)`; host it in an `AndroidView` and drive chapter jumps from your UiState |

Keep the timestamp index in Room (`chapter(videoId, startSec, title, questionId)`) so a tap on a chapter or an MCQ jumps straight to the second.

## 28 · Lecture recording and offline speech-to-text

| Repository | Status | Take from it |
|---|---|---|
| [vilassn/whisper_android](https://github.com/vilassn/whisper_android) | **Adopt as reference** — 693★, pushed 2026-03-18 | Whisper over TFLite, WAV capture, Compose waveform |
| [shaikmohammed8/LocalMind](https://github.com/shaikmohammed8/LocalMind) | **Reference only** — 5★, pushed 2026-01-15 | The `ggml` JNI path — smaller binary, faster on modern CPUs, more build complexity |

Run transcription as WorkManager work with a foreground notification. A 40-minute lecture does not belong in a ViewModel coroutine.

## 29 · LaTeX maths and formula handbooks

| Repository | Status | Take from it |
|---|---|---|
| [huarangmeng/latex](https://github.com/huarangmeng/latex) | **Adopt** — 135★, pushed 2026-11-13 | Pure Compose/KMP parser and renderer: `Latex` and `LatexAutoWrap` composables, fractions, integrals, limits, matrices, chemical formulas, KaTeX metrics, no WebView |

Pairs with `jksalcedo/compose-to-pdf` (genre 1): one rendering path for screen and A4 paper.

## 30 · Text-to-speech readers

| Repository | Status | Take from it |
|---|---|---|
| [nedmah/TextLector](https://github.com/nedmah/TextLector) | **Adopt as reference** — 15★, pushed 2026-06-01 | Offline TTS for PDF/EPUB/TXT, paragraph-synchronised highlighting, 0.5x–2.0x, system voices or sherpa-onnx Piper |
| [Coding-Meet/TextToSpeech-CMP](https://github.com/Coding-Meet/TextToSpeech-CMP) | **Reference only** — 47★, no push since 2025-08-19 | The clearest word-by-word highlight technique with pause/resume position tracking |

## 31 · Book OCR and AI doubt solving

Cross-reference: **genre 20** (`googlesamples/mlkit` for Latin/Devanagari OCR with CameraX) and **genre 10** (`android/ai-samples` for Gemini Nano on-device summarization and grounded answers).

## 32 · Daily quiz feed and peer study rooms

Cross-reference: **genre 17** (`supabase-community/supabase-kt`) — PostgREST for the quiz feed, Realtime channels for leaderboards and shared rooms.

## 33 · Export study material to PDF

Cross-reference: **genre 1** (`jksalcedo/compose-to-pdf`).

---

## Study-app rules that outrank the library choice

1. **Room is the truth.** Decks, review logs, PYQs, attempts, error entries, timer sessions, highlights and transcripts all live in Room; the UI never waits on a socket.
2. **The network is an optional writer.** Supabase or WorkManager push and pull in the background, then write back into Room.
3. **Long work is WorkManager work.** Transcription, OCR of a chapter and PDF export run with a foreground notification, not in a ViewModel coroutine.
4. **Conflicts are decided once.** Single-user study app: last-write-wins on a server timestamp, documented in `learning/DECISIONS.md`.
5. **Never lose FSRS state.** The review log is durable; the scheduler is derived.

---

# Tooling, polish kits and blueprints

Thirty-two repositories in six categories. This section is different from the genre sections: most of these are **components you add to a screen**, not capabilities that define an app.

## 34 · Runtime debugging an agent can drive

| Repository | Status | Take from it |
|---|---|---|
| [wormaceptor/WormaCeptor](https://github.com/wormaceptor/WormaCeptor) | **Adopt (debug only)** — 46★, pushed 2026-11-13, 44 MCP tools confirmed | Live HTTP/WebSocket traffic, Room tables, DataStore, crashes and FPS readable by an agent from a debug build |
| [ChuckerTeam/chucker](https://github.com/ChuckerTeam/chucker) | **Adopt (debug only)** — 4,588★, pushed 2026-11-14 | OkHttp inspector; `library-no-op` in release |
| [square/leakcanary](https://github.com/square/leakcanary) | **Adopt (debug only)** — 30,009★, pushed 2026-10-21 | Leak detection plus a real `shark-dive` skill at `.claude/skills/shark-dive/SKILL.md` |
| [cashapp/paparazzi](https://github.com/cashapp/paparazzi) | **Adopt** — 2,640★, pushed 2026-11-13 | JVM screenshot tests for Compose - no device, no emulator |
| [airbnb/Showkase](https://github.com/airbnb/Showkase) | **Adopt** — 2,323★, pushed 2026-10-26 | Auto-collected `@Preview` catalog |

**Security rule, not a build rule:** `debugImplementation` only, no-op artefacts in release, and any local port or MCP endpoint bound to localhost. A debug inspector that reaches production is a data-exfiltration surface carrying your package name.

## 35 · Blur, glass, sheets, confetti

| Repository | Status | Take from it |
|---|---|---|
| [chrisbanes/haze](https://github.com/chrisbanes/haze) | **Adopt** — 2,686★, pushed 2026-11-14 | Haze 2: `hazeBlur`, `hazeGlass`, progressive background blur |
| [skydoves/Cloudy](https://github.com/skydoves/Cloudy) | **Adopt (alternative)** — 1,294★, pushed 2026-09-13 | GPU `RenderEffect` blur on API 31+, CPU fallback below |
| [DanielMartinus/Konfetti](https://github.com/DanielMartinus/Konfetti) | **Adopt** — 3,394★, pushed 2026-11-04 | Confetti celebrations |
| [ThalzeronLabs/compose-bottom-sheets](https://github.com/ThalzeronLabs/compose-bottom-sheets) | **Reference only** — 0★, pushed 2026-11-11 | Awaitable sheets: `confirm`, `choose`, `date`, `time`, `input` |
| [lucf15/ModalBottomSheet](https://github.com/lucf15/ModalBottomSheet) | **Reference only** — 7★, pushed 2025-10-20 | Fixes nested scrolling and IME padding |
| [Bomsamdi/top_sheet](https://github.com/Bomsamdi/top_sheet) | **Reference only** — 0★, pushed 2026-08-31 | A sheet that slides from the top |

One blur library, not two. Blurred surfaces must be static or small - blurring a scrolling list is the most expensive thing in this section.

## 36 · Inputs, content, compliance

| Repository | Status | Take from it |
|---|---|---|
| [kizitonwose/Calendar](https://github.com/kizitonwose/Calendar) | **Adopt** — 5,627★, pushed 2026-08-13 | Month/week/year views, ranges, GitHub-style heatmaps |
| [mikepenz/AboutLibraries](https://github.com/mikepenz/AboutLibraries) | **Adopt** — 4,498★, pushed 2026-11-14 | Generates the OSS licence screen from the version catalog - a Play requirement |
| [mikepenz/multiplatform-markdown-renderer](https://github.com/mikepenz/multiplatform-markdown-renderer) | **Adopt** — 1,137★, pushed 2026-11-14 | Markdown with tables, code highlighting, Coil 3 images |
| [anhaki/PickTime-Compose](https://github.com/anhaki/PickTime-Compose) | **Adopt** — 41★, pushed 2026-03-10 | Wheel time picker |
| [TuleSimon/xMaterialccp](https://github.com/TuleSimon/xMaterialccp) | **Adopt** — 70★, pushed 2026-01-28 | Country-code picker |
| [skydoves/Orchestra](https://github.com/skydoves/Orchestra) | **Archived in practice** — 465★, **no push since 2023-01-02** | Use `skydoves/Balloon` for tooltips instead |

## 37 · Media, files, zoom, filters

| Repository | Status | Take from it |
|---|---|---|
| [saket/telephoto](https://github.com/saket/telephoto) | **Adopt** — 1,573★, pushed 2026-07-22 | `ZoomableImage` with tile sub-sampling - huge diagrams without OOM |
| [vinceglb/FileKit](https://github.com/vinceglb/FileKit) | **Adopt** — 1,566★, pushed 2026-11-09 | `openFilePicker`, `openFileSaver`, `openDirectoryPicker`, compression |
| [Xiryl/compose-stories](https://github.com/Xiryl/compose-stories) | **Reference only** — 10★, pushed 2025-09-14 | Story player mechanics |
| [nsozturk/quick-filter-kotlin](https://github.com/nsozturk/quick-filter-kotlin) | **Reference only** — 0★, pushed 2026-07-07 | Faceted search chips and filter panel |

## 38 · Architecture frameworks and encrypted storage

| Repository | Status | Take from it |
|---|---|---|
| [slackhq/circuit](https://github.com/slackhq/circuit) | **Adopt (replaces Parts 3-4)** — 1,860★, pushed 2026-11-14 | Compose UDF: `@Composable` presenters, type-safe navigation, retained state |
| [orbit-mvi/orbit-mvi](https://github.com/orbit-mvi/orbit-mvi) | **Adopt (replaces Parts 3-4)** — 1,346★, pushed 2026-08-31 | MVI container, lifecycle-safe collection, test DSL |
| [skydoves/sandwich](https://github.com/skydoves/sandwich) | **Adopt (orthogonal)** — 1,779★, pushed 2026-11-14 | Sealed `ApiResponse` for Retrofit and Ktor |
| [sqlcipher/sqlcipher-android](https://github.com/sqlcipher/sqlcipher-android) | **Adopt** — 281★, pushed 2026-10-27 | AES-256 encrypted SQLite; `SupportOpenHelperFactory` for Room |
| [raamcosta/compose-destinations](https://github.com/raamcosta/compose-destinations) | **Skip on new apps** — 3,386★, pushed 2025-10-12 | Built for Nav 2; Navigation 3 already gives type-safe NavKeys |

Circuit and Orbit are not add-ons - each replaces the ViewModel, navigation and testing story of this playbook. Pick one or neither. SQLCipher is the only reasonable way to encrypt Room at rest; key management stays yours (Android Keystore, never hardcoded).

## 39 · Blueprints to read, not copy

| Repository | Status | Read it for |
|---|---|---|
| [JunkFood02/Seal](https://github.com/JunkFood02/Seal) | **Blueprint** — 30,656★, pushed 2026-09-25 | Wrapping a CLI binary and managing a download queue |
| [skydoves/Pokedex](https://github.com/skydoves/Pokedex) | **Blueprint** — 8,387★, pushed 2026-10-31 | Hilt + Room + Retrofit + Flow MVVM |
| [Pool-Of-Tears/Myne](https://github.com/Pool-Of-Tears/Myne) | **Blueprint** — 1,546★, pushed 2026-09-21 | MVVM + Room ebook downloader |
| [hieuwu/android-groceries-store](https://github.com/hieuwu/android-groceries-store) | **Blueprint** — 274★, pushed 2025-10-22 | Catalog and order flow with Supabase + Room + Hilt |
| [tokn-authenticator/tokn](https://github.com/tokn-authenticator/tokn) | **Blueprint** — 94★, pushed 2026-11-13 | Keystore-backed secrets, QR scanning, encrypted backup |
| [Ivorisnoob/OpenStream](https://github.com/Ivorisnoob/OpenStream) | **Blueprint** — 58★, pushed 2026-11-05 | Media3 ExoPlayer, PiP, subtitles, offline downloads |

---

## Corrections from this batch

| Cited | Reality | Replacement |
|---|---|---|
| `dionsegijn/Konfetti` | **404** | `DanielMartinus/Konfetti` (3,394★, 2026-11-04) |
| `skydoves/Orchestra` | Alive but untouched since **2023-01-02** | `skydoves/Balloon` for tooltips; write the rest |
| `raamcosta/compose-destinations` | 13 months stale and superseded by Navigation 3 | Nav 3 `NavKey` + `NavDisplay` (playbook Part 4.4) |
| `ThalzeronLabs/compose-bottom-sheets`, `Bomsamdi/top_sheet`, `nsozturk/quick-filter-kotlin` | 0 stars, weeks old | Read them; do not depend on them yet |

Two claims were true but **only visible in the repository tree**: WormaCeptor's 44 MCP tools and LeakCanary's `.claude/skills/shark-dive/` skill. A README is a summary, not an inventory.

---

# 40 · CI/CD pipeline

Twenty-two actions and workflows, checked by release tag on 14 November 2026. **Action majors move faster than any other dependency in an Android project** - this section was written because the playbook's own workflow was two to three majors behind.

| Stage | Action | Latest | Note |
|---|---|---|---|
| Checkout | `actions/checkout` | **v7.0.1** | `fetch-depth: 0` for changelogs and tag-derived version codes |
| JDK | `actions/setup-java` | **v6.3.0** | Temurin 21 |
| Gradle | `gradle/actions/setup-gradle` | **v6.4.1** | Wrapper validation, caching, build scans |
| Android SDK | `android-actions/setup-android` | **v4.0.4** | cmdline-tools, build-tools, platforms;android-37 |
| Emulator | `ReactiveCircus/android-emulator-runner` | **v2.38.0** | KVM on ubuntu-latest |
| Emulator (hardened) | `step-security/android-emulator-runner` | v2.38.0 | 0★ fork; read the source before trusting it with secrets |
| Test report | `mikepenz/action-junit-report` | v6.7.1 | Inline PR annotations from JUnit XML |
| Signing | `r0adkll/sign-android-release` | v1 | Signs unsigned APK/AAB from a base64 keystore |
| GitHub Release | `softprops/action-gh-release` | **v3.0.4** | Attach APK, AAB, mapping.txt |
| Play upload | `r0adkll/upload-google-play` | v1.1.5 | AAB + deobfuscation mapping per track |
| Play all-in-one | `deep-rent/publish-android-release` | v2.1.3 | 4★, unproven |
| Play metadata | `Triple-T/gradle-play-publisher` | 4.1.2 | Listings, screenshots, notes from Git |
| Firebase testers | `wzieba/Firebase-Distribution-Github-Action` | v1.7.1 | Last push 2025-03 |
| Notifications | `appleboy/telegram-action` | v1.1.2 | APK + changelog to a chat |
| Screenshots | `fastlane/fastlane` | 2.241.2 | `supply`, `screengrab` |
| Egress audit | `step-security/harden-runner` | v2.22.4 | Stops a compromised plugin exfiltrating `KEYSTORE_BASE64` |
| SAST | `github/codeql-action` | codeql-bundle-v2.27.4 | `language: java-kotlin` |
| Dependency updates | `renovatebot/github-action` | v46.3.13 | Grouped PRs for the version catalog |
| Artifacts | `actions/upload-artifact` / `download-artifact` | **v7.0.2 / v8.0.2** | Different majors on purpose |
| Release automation | `googleapis/release-please-action` | **v5.0.0** | Conventional Commits to semver |
| Dependency graph | `vanniktech/gradle-dependency-graph-generator-plugin` | 0.8.0 | Gradle plugin, not an action |
| Version codes | `github.run_number` + `-P` flags | - | No action needed |

## Corrections from this batch

| Cited | Reality | Use instead |
|---|---|---|
| `google-github-actions/release-please-action` | **Archived** (last push 2024-05) | `googleapis/release-please-action` v5.0.0 - different org, so the old pin still resolves and does nothing new |
| `actions/setup-java@v5` | Latest is **v6.3.0** | `@v6` |
| `actions/checkout@v5` / `@v6` | Latest is **v7.0.1** | `@v7` |
| `actions/upload-artifact@v4` | Latest is **v7.0.2** | `@v7` (download-artifact is v8) |
| `softprops/action-gh-release@v2` | Latest is **v3.0.4** | `@v3` |
| `android-actions/setup-android@v3` | Latest is **v4.0.4** | `@v4` |
| `android-emulator-runner v2.35.0` | Latest is **v2.38.0** | `@v2` |

**This playbook was guilty too.** Its Part 10 workflow sat on checkout@v4, setup-java@v4, setup-gradle@v4, upload-artifact@v4 and action-gh-release@v2, and the repository's own CI printed `Node.js 20 is deprecated, forced to run on Node.js 24` as evidence. It is now on v7 / v6 / v6 / v7 / v3.

## One-time setup that actually bites

1. `git update-index --chmod=+x gradlew` - otherwise every Linux runner fails with `Permission denied`.
2. Base64 the upload keystore into a single line; store `KEYSTORE_BASE64`, `KEY_ALIAS`, `KEYSTORE_PASSWORD`, `KEY_PASSWORD` as secrets; back the keystore up outside CI.
3. Choose where signing happens: external (`r0adkll/sign-android-release`) keeps `signingConfigs` out of the build but signs *after* Gradle, so the tested artifact is not the shipped one; internal (env-var `signingConfig`, playbook Part 7.1) signs during the build. Pick one and document it.
4. Pin by major tag and let Renovate move it, or pin by commit SHA for a hardened chain - never mix conventions in one workflow.
5. `harden-runner` first step, CodeQL on a schedule. Together they answer what left the runner and what in the code was reachable.

The cheapest long-term fix for this whole section is one Renovate rule: group `github-actions` updates and open them weekly. Every stale pin above would have been a merged PR instead of a discovery.
