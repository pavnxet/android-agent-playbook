<!-- verified-at: initial · 2026-11-14 · append-only; rotate to archive/ at ~500 lines -->
# SUMMARY: session history (newest last)

## S-20261114-0001 · DONE · playbook v1
Read 122 SKILL.md files across four agent-skill repos plus two project templates; wrote the 25-page
playbook (versions, architecture, edge-to-edge, Nav 3, build, release, testing, CLI loop, CI).
next: fold in the 24-repository list.

## S-20261114-0002 · DONE · playbook v2
Audited 24 community repos via the GitHub API. All exist; seven claims failed (adb-mcp has 81 tools,
not 73; NexPlugs is AGP 8.10.1; two templates stale; one vision claim unverified). Added Part 14.
next: architecture doctrine review.

## S-20261114-0003 · DONE · playbook v3 and v4
Added Part 15 (MVVM vs MVI on the input axis, verified against `architecture-templates/base`).
Then fixed the real defects: split Appendix A into single-module + multi-module, lowered Gradle heap,
added adb fallbacks for the `android` CLI, neutralised audit phrasing. Rejected the claimed code
mangling after checking the text layer (0 LaTeX artifacts, 23/24 strings exact).
next: package as a repository.

## S-20261114-0004 · DONE · repository assembled and committed
Built `android-agent-playbook`: README, MIT license, templates/, docs/, scripts/, and the memory +
safety layer adopted from `pavnxet/learnings-for-agents`. Self-check `scripts/verify_repo.py` passes;
installer tested for single, multi-module, overwrite-guard, force, missing-arg, bad-flag and
self-target. The scanner was refined once (ADR-008) after two false positives on the signing snippet.
Publishing is blocked in this environment: the GitHub App cannot create repositories
(`Resource not accessible by integration`). The repo must be created by a human, then pushed.
next: create the remote, push, tag v1.0.0; keep the version matrix current.

## S-20261114-0005 · DONE · capability registry
Verified 22 repositories across 10 capabilities: all exist, two are archived, six are stale enough to
be reference-only, one claim failed inspection. Added `docs/FEATURE_RECIPES.md`, playbook Part 16
(35 pages now), README and template pointers, ADR-011/012, INCIDENT-005. Snippets regenerated (21
blocks). next: re-verify the registry quarterly.
