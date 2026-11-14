#!/usr/bin/env python3
"""Guard against corruption inside Markdown code fences.

Two checks, both cheap and both aimed at real failures seen in this repository:

1. Fence balance - every ``` opener has a closer, and no fence is left open at EOF.
2. LaTeX/OCR artifacts inside fenced blocks - `$=`, `$\\theta`, `^{`, `\\times`-style
   escape leakage and `$<` are what a vision pass or a PDF round-trip leaves behind
   (see learning/INCIDENTS.md, INCIDENT-001). They must never appear in code a reader
   is meant to copy.

Usage: python3 scripts/check_markdown_fences.py
Exit code 0 = clean.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {'.git', 'build', '.gradle', 'node_modules', '.idea'}
ARTIFACTS = ['$=', '$<', r'$\theta', '^{', r'\times', r'\frac']


def markdown_files():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in sorted(files):
            if name.endswith('.md'):
                yield os.path.join(root, name)


def main():
    failures = []
    checked = 0

    for path in markdown_files():
        rel = os.path.relpath(path, REPO)
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()

        in_fence = False
        fence_line = 0
        for number, line in enumerate(lines, start=1):
            if line.lstrip().startswith('```'):
                in_fence = not in_fence
                if in_fence:
                    fence_line = number
                continue
            if not in_fence:
                continue
            checked += 1
            for artifact in ARTIFACTS:
                if artifact in line:
                    failures.append(
                        f'{rel}:{number}: artifact {artifact!r} inside a code fence '
                        f'(opened at line {fence_line}) -> {line.strip()[:80]}'
                    )
        if in_fence:
            failures.append(f'{rel}:{fence_line}: unclosed code fence at end of file')

    if failures:
        print('FAIL: Markdown fence checks found problems:\n')
        for f in failures:
            print(' ', f)
        return 1

    print(f'OK: fences balanced and free of LaTeX artifacts ({checked} fenced lines scanned)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
