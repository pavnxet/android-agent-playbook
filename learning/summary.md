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

## S-20261114-0006 · DONE · 20-genre registry
Verified 20 more repositories across 10 app genres: 3 paths do not exist, 3 repos are archived, and
the author's swipe-deck library is archived as well. Extended `docs/FEATURE_RECIPES.md` to 20 genres
with status labels and a dead-links table; added playbook Part 17 (38 pages, 22 snippet blocks);
recorded ADR-013 and INCIDENT-006.
next: re-verify the whole registry quarterly; the archived list will grow.

## S-20261114-0007 · DONE · study-app cluster
Verified 13 new repositories for 25 study-app genres: all alive, four claims corrected (book-story has
six formats not seven; notate is e-ink-first; azri is a 1-star but real FSRS-6 implementation;
Coding-Meet stale since 2025-08), and one claim confirmed only by reading the source tree (focuslock).
Registry now 33 genres; playbook 40 pages, 18 parts. ADR-014, INCIDENT-007 logged.
next: re-verify quarterly; Room 3.x migration is the next real decision.

## S-20261114-0008 · DONE · tooling, polish and blueprints
Verified 32 repositories: one 404 (dionsegijn/Konfetti -> DanielMartinus/Konfetti), one untouched
since 2023 (skydoves/Orchestra), one superseded by Navigation 3 (compose-destinations), three
zero-star newcomers. Two claims verified only in repository trees (WormaCeptor's 44 MCP tools,
LeakCanary's shark-dive skill). Registry now 39 sections; playbook 43 pages, 19 parts, 23 snippets.
ADR-015/016, INCIDENT-008 logged.
next: quarterly re-verification; the 2023-era and zero-star entries are the first to re-check.

## S-20261114-0009 · DONE · CI/CD actions verified
Verified 22 actions by release tag: one archived (google-github-actions/release-please-action, moved to
googleapis v5), six cited a major behind (checkout v7, setup-java v6, upload-artifact v7,
action-gh-release v3, setup-android v4, emulator-runner v2.38). Found the same staleness in our own
Part 10 workflow and in secret-scan.yml, and fixed both. Part 20 added; registry section 40; 46 pages.
ADR-017/018, INCIDENT-009 logged.
next: weekly Renovate group for github-actions is the standing fix.

## S-20261114-0010 · DONE · v2.0 production upgrade
Added PROMPTS.md (5 prompts), lint-repo.yml (shell syntax + 100755 check + fence guard + verify_repo
+ lychee offline links), scripts/check_markdown_fences.py, a compiled `starter/` app on the exact
pinned baseline with verify-starter.yml, a capability index and permission-hygiene table in the
registry, README badges and map rows, template pointers, and installer support for FEATURE_RECIPES.md
and PROMPTS.md. ADR-019/020 logged.
next: keep starter and Part 2 in lockstep; the starter build is the proof that the matrix is real.
