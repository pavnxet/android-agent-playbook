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
