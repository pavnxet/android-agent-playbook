# Feature recipes: capability → verified library

The lookup table an agent should read **before** writing a feature. One repository per capability, with the status checked on 14 November 2026 and the Android APIs each one actually uses.

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
