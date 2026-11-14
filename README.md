# Android Agent Playbook

**CLI-first Android architecture rules, a verified 2026 version baseline, `AGENTS.md` templates, copy-paste snippets — plus persistent agent memory and fail-closed publication safety.**

[![Kotlin](https://img.shields.io/badge/Kotlin-2.3%2B-7F52FF?logo=kotlin&logoColor=white)](https://kotlinlang.org)
[![AGP](https://img.shields.io/badge/AGP-9.3.2-3DDC84?logo=android&logoColor=white)](https://developer.android.com/build)
[![Compose](https://img.shields.io/badge/Jetpack%20Compose-2026.x-4285F4?logo=jetpackcompose&logoColor=white)](https://developer.android.com/compose)
[![Material 3](https://img.shields.io/badge/Material%203-M3-757575)](https://m3.material.io)
[![Agent memory](https://img.shields.io/badge/agent%20memory-tiered-6E56CF)](learning/BRIEF.md)
[![Secret scan](https://img.shields.io/badge/secret%20scan-fail--closed-B3261E)](scripts/scan_sensitive.py)
[![Lint Repository](https://github.com/pavnxet/android-agent-playbook/actions/workflows/lint-repo.yml/badge.svg)](https://github.com/pavnxet/android-agent-playbook/actions/workflows/lint-repo.yml)
[![Verify Starter](https://github.com/pavnxet/android-agent-playbook/actions/workflows/verify-starter.yml/badge.svg)](https://github.com/pavnxet/android-agent-playbook/actions/workflows/verify-starter.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Why this exists

An agent writing Android code in 2026 fails in predictable ways: it invents version numbers, wires Navigation 2 when Navigation 3 is current, forgets insets, adds `-keep` rules until the crash stops, and modularises a two-screen app into twelve Gradle modules. Then, on the next session, it forgets everything it learned — and occasionally pastes a token into a commit.

This repository fixes all three, in two layers that work independently:

| Layer | What it gives you | Files |
|---|---|---|
| **1 · Android knowledge** | A 33-page playbook, two `AGENTS.md` app templates, and 20 verified code snippets | `docs/`, `templates/`, `scripts/init-agent-rules.sh` |
| **2 · Agent memory + safety** | Tiered `learning/` memory so an agent never re-discovers a bug, and fail-closed git hooks that block secrets and PII before they are committed | `AGENTS.md`, `learning/`, `.githooks/`, `scripts/scan_sensitive.py`, `.github/workflows/` |

Layer 1 alone makes an agent write correct Android. Layer 2 makes it remember, and makes publication safe.

## Repository map

| Path | Use it when |
|---|---|
| [`templates/AGENTS.md`](templates/AGENTS.md) | **Default.** A 1–4 screen Android app. Single module, package-by-layer, ready to drop in a repo root. |
| [`templates/AGENTS_multimodule.md`](templates/AGENTS_multimodule.md) | You have crossed 4–5 features and need the `:core:*` / `:feature:*:api|impl` graph. |
| [`docs/CODE_SNIPPETS.md`](docs/CODE_SNIPPETS.md) | Your agent needs exact code: version catalog, `gradle.properties`, ViewModel + `UiState`, Hilt, Nav 3, Room repository, signing, R8, tests, CI YAML. |
| [`PROMPTS.md`](PROMPTS.md) | You want to hand a task to an agent right now: five copy-paste prompts (scaffold, vertical slice, modularise, release gate, crash loop) with `[bracketed]` variables. |
| [`starter/`](starter/) | You want proof the baseline compiles: a one-screen app on the exact pinned stack, built and tested by CI on every change. |
| [`docs/FEATURE_RECIPES.md`](docs/FEATURE_RECIPES.md) | Your agent is about to add a capability or genre (PDF export, camera, upload, QR, AI, media, charts, maps, widgets, BLE/USB, swipe, passkeys, animation, billing, OCR). **20 genres + 25 study-app genres + 32 tooling/polish repos**, one verified repository each, with status and permission cost. |
| [`docs/Android_Engineering_Playbook.pdf`](docs/Android_Engineering_Playbook.pdf) | The full manual: 20 parts, 3 appendices, 46 pages. |
| [`scripts/check_markdown_fences.py`](scripts/check_markdown_fences.py) | Repo hygiene: proves no code fence is unbalanced and no LaTeX/OCR artifact leaked into code. |
| [`docs/Android_Engineering_Playbook.docx`](docs/Android_Engineering_Playbook.docx) | You want to edit or extend the manual. |
| [`AGENTS.md`](AGENTS.md) | The protocol an agent follows **in this repository**: memory tiers, safety invariants, git rules, Project Profile (§12). |
| [`learning/`](learning/BRIEF.md) | Cold-start memory: `BRIEF.md` (read first), `DECISIONS.md` (ADRs), `PLAYBOOKS.md` (recipes), `INCIDENTS.md` (postmortems), `learning.md`, `TOOLS.md`, `summary.md`. |
| [`scripts/init-agent-rules.sh`](scripts/init-agent-rules.sh) | One command to install the app rules into an existing Android project. |
| [`scripts/setup.sh`](scripts/setup.sh) · [`setup.ps1`](scripts/setup.ps1) | Install the safety kit: git hooks, private denylist, doctor check. |
| [`scripts/verify_repo.py`](scripts/verify_repo.py) | Self-check: links, anchors, fences, YAML parse, shell syntax, installer behaviour. |
| [`scripts/gen_snippets.py`](scripts/gen_snippets.py) | Regenerate `docs/CODE_SNIPPETS.md` from the DOCX after editing the playbook. |

> **Two `AGENTS.md` files exist on purpose.** The root one is protocol for work on *this repository*. `templates/AGENTS.md` is the rule set for *your Android app*. The installer refuses to target this repository, so they cannot collide. (See `learning/DECISIONS.md` ADR-006.)

## Quick start

### Use the Android rules in your app

```bash
git clone https://github.com/pavnxet/android-agent-playbook && cd android-agent-playbook
./scripts/setup.sh                                   # safety kit for this clone (optional)

./scripts/init-agent-rules.sh /path/to/your-app                # single module (1-4 screens)
./scripts/init-agent-rules.sh /path/to/your-app --multimodule  # 5+ features
```

That writes `AGENTS.md` and `docs/CODE_SNIPPETS.md` into your project. Open it in Claude Code, Codex CLI, Cursor, OpenCode or Antigravity, replace the `[App name]` / `com.<you>.<app>` placeholders, and the agent has the stack, package layout, state rules and verification commands in context.

> Keep `AGENTS.md` lightweight and put heavy code in `docs/CODE_SNIPPETS.md`: the rules file is loaded into every session, so it should carry decisions, not 200 lines of Gradle.

### Adopt the memory + safety layer in any repository

```bash
cp -r learning AGENTS.md .githooks scripts .env.example /path/to/repo/
cd /path/to/repo && ./scripts/setup.sh
```

`setup.sh` links `.githooks`, creates a private `.git/agent-denylist.txt` (never committed), checks your git email is a GitHub noreply address, and runs the doctor. Then fill in §12 of `AGENTS.md` with your project's stack and commands.

## Verified baseline stack

| Layer | Version | Note |
|---|---|---|
| AGP / Gradle | 9.3.2 / 9.7.1 | AGP 9 requires KSP ≥ 2.3.6 and Hilt ≥ 2.59.2 |
| Kotlin | 2.3.0+ | Compose compiler ships with the Kotlin plugin |
| compileSdk / minSdk | 37 / 24 | Fall back to `compileSdk 36` if a library lacks API 37 metadata |
| Compose BOM | 2026.x | Pin the BOM, never individual Compose versions |
| UI / state | Compose + Material 3 | Single Activity, `enableEdgeToEdge()` |
| Navigation | Navigation 3 (`@Serializable NavKey`) | Nav 2.8.x only for legacy code |
| DI / codegen | Hilt, KSP | No kapt in new code |
| Data | Room 2.8.3, DataStore 1.2.0 | Room is the source of truth |
| Network | Retrofit 2.11 + OkHttp 4.12 | kotlinx.serialization converter |
| Testing | Robolectric 4.16 + Turbine 1.2.0 | JVM-first; no emulator for unit tests |

## Engineering non-negotiables

- **Single Activity, 100% Compose, Material 3.** No XML layouts in new screens.
- **One immutable `UiState` per screen**, exposed as `StateFlow`, started with `WhileSubscribed(5_000)`.
- **One-shot effects in a `Channel`**, never inside the state object — otherwise rotation replays navigation.
- **`SavedStateHandle` for user input.** A ViewModel survives rotation, not process death.
- **`enableEdgeToEdge()` before `setContent`**, and consume `Scaffold` insets exactly once.
- **Inject `CoroutineDispatcher`s.** A hardcoded `Dispatchers.IO` is the top cause of flaky tests.
- **KSP over kapt.** AGP 9 needs KSP ≥ 2.3.6 anyway.
- **CLI verification is the review gate:** `./gradlew assembleDebug --stacktrace` and `./gradlew testDebugUnitTest`.
- **Do not modularise until the fifth feature.** Packages first, modules when it hurts.

## Memory tiers (token budget)

| File | Tier | Read mode | Write mode | Budget |
|---|---|---|---|---|
| `AGENTS.md` | A | Quick Card + §12 always | human-edited; agents propose | Quick Card ≤ 25 lines |
| `learning/BRIEF.md` | A | full read at session start | rewritten whole when stale | ≤ 100 lines |
| `learning/learning.md` | B | `grep` keyword, read matched area | edit in place, no duplicates | ≤ 200 lines |
| `learning/DECISIONS.md` | B | `grep` relevant ADRs | append; update status in place | unlimited |
| `learning/EXECUTION_FLOW.md` | B | read the area being touched | living map | ≤ 150 lines |
| `learning/TOOLS.md` | B | consult before adding a dependency | append tool + score | unlimited |
| `learning/summary.md` | C | `tail -40` or `grep IN-PROGRESS` | **append-only** | rotate at ~500 lines |

The rule that makes it work: **recall before exploring**. Before reading code to learn how or why, `grep -rniE "<keywords>" learning/` — do not rediscover what is already recorded.

## Safety: seven fail-closed layers

1. **Pre-write scan** — agents scan text for keys and paths before persisting it.
2. **Doctor** — `python3 scripts/scan_sensitive.py --doctor` verifies hooks and denylist exist.
3. **Pre-commit hook** — scans staged files, blocks the commit on any detection.
4. **Commit-msg hook** — blocks secrets in commit titles and bodies.
5. **Pre-push hook** — scans the outgoing commit range before it leaves the machine.
6. **Private denylist** — `.git/agent-denylist.txt` holds your real name, username and custom terms; it lives in `.git/` and is never committed.
7. **CI** — `secret-scan.yml` runs the scanner plus Gitleaks on every push and pull request.

## Verify it yourself

```bash
python3 scripts/verify_repo.py               # links, anchors, fences, YAML parse, shell, installer
python3 scripts/check_markdown_fences.py     # fence balance + no LaTeX/OCR artifacts in code
python3 scripts/scan_sensitive.py --doctor   # hooks + denylist present
bash -n scripts/*.sh                         # POSIX syntax
cd starter && ./gradlew testDebugUnitTest    # the baseline stack actually compiles
```

Three CI workflows enforce this: `lint-repo.yml` (shell, executable bits, fences, links, self-check), `verify-starter.yml` (the starter app builds and tests), and `secret-scan.yml` (sensitive-content scan plus Gitleaks).

## Companion ecosystem

| Repository | What it gives you | Verified |
|---|---|---|
| [`android/skills`](https://github.com/android/skills) | Google's 36 official agent skills — authoritative on AGP 9, insets, R8, ANR, Nav 3, security | 36 skills, commit `5815d27` |
| [`haidrrrry/compose-kotlin-agent-skills`](https://github.com/haidrrrry/compose-kotlin-agent-skills) | 2026 toolchain router skill with a banned-antipatterns reference | 65★, pushed 2026-07-08 |
| [`liuyi0808/android-review`](https://github.com/liuyi0808/android-review) | OWASP MASVS + Play-policy review gate before release | 19★, pushed 2026-08-27 |
| [`mobile-next/mobile-mcp`](https://github.com/mobile-next/mobile-mcp) | MCP server for device control and screen mirroring | 10,569★, pushed 2026-11-11 |
| [`android/architecture-templates`](https://github.com/android/architecture-templates) | Official starter (`base`, `multimodule`, `base-navigation3`) with `customizer.sh` | 3,173★, pushed 2026-11-13 |
| [`pavnxet/learnings-for-agents`](https://github.com/pavnxet/learnings-for-agents) | The memory + publication-safety template this repository's layer 2 is built on | source of `AGENTS.md`, `learning/`, `.githooks/` |

## How this was verified

Versions, flags and commands were read from the repositories themselves — `gradle/libs.versions.toml`, `gradle.properties`, convention plugins, workflow YAML — not from READMEs. Repository state (stars, last push) was queried through the GitHub API on **14 November 2026**. Code in `docs/CODE_SNIPPETS.md` is generated from the source `.docx`, so it matches the document byte for byte.

Version numbers move. Treat this as a dated snapshot: re-check the matrix when you start a project, and prefer the build file over any document — including this one.

## Credits & license

Built and maintained by [Pavnxet](https://github.com/pavnxet).

- **Android knowledge** distilled from Google's official Android guidance and the community skill repositories credited above.
- **Layer 2** (memory protocol, hooks, scanner, CI scan) is adapted from [`pavnxet/learnings-for-agents`](https://github.com/pavnxet/learnings-for-agents), MIT.
- The verification work, corrections and packaging in layer 1 are original.

[MIT](LICENSE) © 2026 Pavnxet.
