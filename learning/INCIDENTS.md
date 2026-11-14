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
