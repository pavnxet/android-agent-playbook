<!-- verified-at: initial · 2026-11-14 · append tools with a score; consult before adding dependencies -->
# TOOLS: vetted tool catalog

Scores: 5 = use by default, 4 = use when its niche applies, 3 = acceptable, 2 = avoid unless forced.

| Tool | Score | Use it for | Notes |
|---|---|---|---|
| `./gradlew` | 5 | every build, test, lint | never bare `gradle`; the wrapper pins the version |
| `adb` | 5 | install, launch, logcat, UI dump | `adb exec-out uiautomator dump /dev/tty` when `android` CLI is absent |
| `apkanalyzer` | 4 | static APK questions: is class X in the dex, what did the manifest merger drop | faster than rebuilding to answer |
| `jadx` | 3 | reading third-party bytecode | heavy output; use targeted queries |
| `android` CLI (android/skills devtools) | 4 | `layout` JSON, `screen capture`, emulator management | not part of the SDK; install separately |
| `mobile-next/mobile-mcp` | 4 | MCP device control on a local machine | 10.5k stars; needs an attached device |
| `CursorTouch/Android-MCP` | 3 | accessibility-tree automation, no helper APK | needs a device |
| `python3` + PyYAML | 4 | validating the CI YAML in snippets | stdlib + one dep |
| `python-docx` | 4 | regenerating snippets from the DOCX | required by `scripts/gen_snippets.py` |
| LibreOffice `soffice` | 3 | DOCX -> PDF rendering check | slow; use once per document change |
| R8 `analyzeReleaseR8Config` | 5 | keep-rule analysis on AGP >= 9.3 | requires `protobuf>=6.33.4` |

## Do not add
- A second markdown linter, a doc site generator, or a Node toolchain: the repository is Markdown,
  two binaries and four small scripts. Every added dependency is a maintenance tax on a docs repo.
