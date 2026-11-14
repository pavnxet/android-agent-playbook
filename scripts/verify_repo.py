#!/usr/bin/env python3
"""Self-check for the android-agent-playbook repository.

Verifies, without network access:
  - every relative link in every Markdown file resolves to a real file
  - every in-page anchor link resolves to a real heading
  - code fences in docs/CODE_SNIPPETS.md are balanced and free of known artifacts
  - the YAML block parses and every job exposes a steps list
  - Kotlin blocks have balanced braces and parentheses
  - scripts/*.sh pass `bash -n`
  - scripts/init-agent-rules.sh behaves: single, --multimodule, overwrite guard,
    missing argument, unknown flag, and refusal to target this repository itself

Usage: python3 scripts/verify_repo.py
Exit code 0 = all checks passed.
"""

import os
import re
import subprocess
import sys
import tempfile
import shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = True


def fail(msg):
    global ok
    ok = False
    print('FAIL', msg)


def rel(path):
    return os.path.relpath(path, REPO)


# ---------- 1. relative links ----------
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
md_files = []
for root, dirs, files in os.walk(REPO):
    if '.git' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.md'):
            md_files.append(os.path.join(root, f))

for path in md_files:
    base = os.path.dirname(path)
    text = open(path, encoding='utf-8').read()
    for _label, target in LINK_RE.findall(text):
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        fpath = os.path.normpath(os.path.join(base, target.split('#')[0]))
        if not os.path.exists(fpath):
            fail(f'{rel(path)}: broken link -> {target}')

# ---------- 2. anchors ----------
def anchor(title):
    a = title.lower()
    a = re.sub(r'[^a-z0-9 \-]', '', a)
    return a.strip().replace(' ', '-')


for path in md_files:
    text = open(path, encoding='utf-8').read()
    heads = {anchor(h) for h in re.findall(r'^#{1,6} (.+)$', text, re.M)}
    for _label, target in LINK_RE.findall(text):
        if target.startswith('#') and target[1:] not in heads:
            fail(f'{rel(path)}: dead anchor -> {target}')

# ---------- 3. snippet file hygiene ----------
snip_path = os.path.join(REPO, 'docs', 'CODE_SNIPPETS.md')
if not os.path.exists(snip_path):
    fail('docs/CODE_SNIPPETS.md is missing')
    snip = ''
else:
    snip = open(snip_path, encoding='utf-8').read()
    if snip.count('```') % 2:
        fail('CODE_SNIPPETS.md: unbalanced code fences')
    for bad in ['Dispatchers. 10', 'Dispatchers.10', 'provide0kHttp', 'HeapDump0n', '$<', '^{']:
        if bad in snip:
            fail(f'CODE_SNIPPETS.md: stray artifact {bad!r}')

# YAML: parse it, then assert structure
try:
    import yaml
except ImportError:
    yaml = None
    print('note: PyYAML not installed - skipping YAML parse (pip install pyyaml)')
if yaml is not None:
    blocks = re.findall(r'```yaml\n(.*?)```', snip, re.S)
    if not blocks:
        fail('no yaml block found in CODE_SNIPPETS.md')
    for b in blocks:
        try:
            doc = yaml.safe_load(b)
        except Exception as exc:  # noqa: BLE001
            fail(f'yaml does not parse: {exc}')
            continue
        jobs = (doc or {}).get('jobs') or {}
        if not jobs:
            fail('yaml has no jobs')
        for name, job in jobs.items():
            steps = job.get('steps')
            if not isinstance(steps, list) or not steps:
                fail(f'job {name} has no steps list')
                continue
            for i, step in enumerate(steps):
                if not isinstance(step, dict):
                    fail(f'job {name} step {i} is not a mapping')

# Kotlin: balanced delimiters
for b in re.findall(r'```kotlin\n(.*?)```', snip, re.S):
    if b.count('{') != b.count('}'):
        fail(f'kotlin block brace mismatch: {b.strip()[:50]!r}')
    if b.count('(') != b.count(')'):
        fail(f'kotlin block paren mismatch: {b.strip()[:50]!r}')

# ---------- 4. shell syntax ----------
for name in ('init-agent-rules.sh', 'setup.sh'):
    path = os.path.join(REPO, 'scripts', name)
    if not os.path.exists(path):
        fail(f'scripts/{name} is missing')
        continue
    r = subprocess.run(['bash', '-n', path], capture_output=True, text=True)
    if r.returncode:
        fail(f'bash -n scripts/{name}: {r.stderr.strip()}')

# ---------- 5. installer behaviour ----------
script = os.path.join(REPO, 'scripts', 'init-agent-rules.sh')
if os.path.exists(script):
    if not os.access(script, os.X_OK):
        fail('scripts/init-agent-rules.sh is not executable')

    tmp = tempfile.mkdtemp()
    try:
        proj = os.path.join(tmp, 'fake-app')
        os.makedirs(proj)

        r = subprocess.run([script, proj], capture_output=True, text=True)
        if r.returncode or not os.path.exists(os.path.join(proj, 'AGENTS.md')):
            fail('single-module install failed: ' + r.stderr.strip())
        elif 'single-module' not in r.stdout:
            fail('single-module install did not report its flavour')

        r2 = subprocess.run([script, proj], capture_output=True, text=True)
        if r2.returncode == 0:
            fail('installer overwrote an existing AGENTS.md without --force')

        r2b = subprocess.run([script, proj, '--force'], capture_output=True, text=True)
        if r2b.returncode:
            fail('installer rejected --force: ' + r2b.stderr.strip())

        big = os.path.join(tmp, 'fake-big')
        os.makedirs(big)
        r3 = subprocess.run([script, big, '--multimodule'], capture_output=True, text=True)
        if r3.returncode or 'multi-module' not in r3.stdout:
            fail('multi-module install failed')
        else:
            installed = open(os.path.join(big, 'AGENTS.md'), encoding='utf-8').read()
            if ':feature:<name>:impl' not in installed:
                fail('multi-module template content not installed')

        r4 = subprocess.run([script], capture_output=True, text=True)
        if r4.returncode == 0:
            fail('installer accepted a missing target path')

        r5 = subprocess.run([script, '--nonsense', big], capture_output=True, text=True)
        if r5.returncode == 0:
            fail('installer accepted an unknown flag')

        r6 = subprocess.run([script, REPO], capture_output=True, text=True)
        if r6.returncode == 0:
            fail('installer allowed itself to overwrite this repository AGENTS.md')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

# ---------- 6. scanner semantics ----------
scanner_path = os.path.join(REPO, 'scripts', 'scan_sensitive.py')
if os.path.exists(scanner_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('scan_sensitive', scanner_path)
    scanner = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(scanner)
    except Exception as exc:  # noqa: BLE001
        fail(f'cannot import scan_sensitive.py: {exc}')
        scanner = None
    if scanner is not None:
        # Synthetic values, assembled at runtime so no key-shaped literal exists in the
        # source file (gitleaks scans file bytes and would flag one). See ADR-010.
        FAKE_PASSWORD = 'hunter2' + 'hunter2'
        FAKE_API_KEY = 'sk-' + 'live-' + 'abcdef' + '123456'

        # env indirection must pass; literals must be caught
        cases = [
            ('storePassword = System.getenv("KEYSTORE_PASSWORD")', False),
            ('KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}', False),
            ('password = "' + FAKE_PASSWORD + '"', True),
            ('api_key = "' + FAKE_API_KEY + '"', True),
        ]
        for line, should_flag in cases:
            flagged = bool(scanner.scan_content('probe.kt', line, []))
            if flagged != should_flag:
                fail(f'scanner semantics: {line!r} flagged={flagged} expected={should_flag}')

print()
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
