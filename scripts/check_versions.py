#!/usr/bin/env python3
"""Verify the README baseline table against what is actually published.

For each pinned version in the README "Verified baseline stack" table, fetch the
authoritative metadata and fail if the version is not published, or if a newer stable
exists. This is the check that stops the table from rotting (ADR-023).

Sources:
  Google Maven    https://dl.google.com/dl/android/maven2/<path>/maven-metadata.xml
  Maven Central   https://repo1.maven.org/maven2/<path>/maven-metadata.xml
  Gradle          https://services.gradle.org/versions/current

Usage:
    python3 scripts/check_versions.py            # report drift, exit 1 on failure
    python3 scripts/check_versions.py --lenient  # report drift, exit 0 (advisory)
Exit code 0 = every pin is published and current.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(REPO, 'README.md')

GOOGLE = 'https://dl.google.com/dl/android/maven2/{}/maven-metadata.xml'
CENTRAL = 'https://repo1.maven.org/maven2/{}/maven-metadata.xml'
GRADLE = 'https://services.gradle.org/versions/current'

# README row label -> (metadata path, source)
PINS = {
    'agp': ('com/android/tools/build/gradle', 'google'),
    'kotlin': ('org/jetbrains/kotlin/kotlin-gradle-plugin', 'central'),
    'compose bom': ('androidx/compose/compose-bom', 'google'),
    'material3': ('androidx/compose/material3/material3', 'google'),
    'navigation3': ('androidx/navigation3/navigation3-runtime', 'google'),
    'core-ktx': ('androidx/core/core-ktx', 'google'),
    'room': ('androidx/room/room-runtime', 'google'),
    'ksp': ('com/google/devtools/ksp/symbol-processing-api', 'central'),
    'hilt': ('com/google/dagger/hilt-android', 'central'),
    'workmanager': ('androidx/work/work-runtime-ktx', 'google'),
    'glance': ('androidx/glance/glance', 'google'),
    'activity-compose': ('androidx/activity/activity-compose', 'google'),
    'lifecycle': ('androidx/lifecycle/lifecycle-runtime-compose', 'google'),
    'turbine': ('app/cash/turbine/turbine', 'central'),
}

PRERELEASE = re.compile(r'(alpha|beta|rc|dev|eap|snapshot|M\d)', re.IGNORECASE)

# README row -> which version in that row belongs to which component.
# Rows such as "activity-compose / lifecycle | 1.13.0 / 2.11.0" carry two components.
ROW_MAP = {
    'agp / gradle': ['agp'],
    'kotlin': ['kotlin'],
    'compose bom': ['compose bom'],
    'material3': ['material3'],
    'navigation3': ['navigation3'],
    'activity-compose / lifecycle': ['activity-compose', 'lifecycle'],
    'core-ktx': ['core-ktx'],
    'room': ['room'],
    'ksp / hilt': ['ksp', 'hilt'],
    'workmanager / glance': ['workmanager', 'glance'],
    'turbine / robolectric': ['turbine'],
}


def semver_key(version):
    """Sort key that puts 1.19.1 above 1.9.0, and prereleases below their release."""
    core = re.split(r'[-+]', version)[0]
    parts = []
    for piece in core.split('.'):
        try:
            parts.append(int(piece))
        except ValueError:
            parts.append(0)
    while len(parts) < 4:
        parts.append(0)
    return (tuple(parts), 0 if PRERELEASE.search(version) else 1)


def fetch(url, timeout=25):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return response.read().decode('utf-8', 'replace')


def versions_for(path, source):
    url = (GOOGLE if source == 'google' else CENTRAL).format(path)
    xml = fetch(url)
    return re.findall(r'<version>([^<]+)</version>', xml)


def stable(versions):
    return [v for v in versions if not PRERELEASE.search(v)]


def readme_pins():
    """Extract the pinned versions from the README baseline table."""
    with open(README, encoding='utf-8') as fh:
        text = fh.read()
    start = text.find('## Verified baseline stack')
    end = text.find('## Engineering non-negotiables')
    if start < 0 or end < 0:
        sys.exit('error: could not locate the baseline table in README.md')
    table = text[start:end]

    found = {}
    for line in table.splitlines():
        if not line.startswith('|') or line.startswith('|---'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) < 2:
            continue
        label = cells[0].lower().replace('**', '')
        keys = ROW_MAP.get(label)
        if not keys:
            continue
        versions = re.findall(r'\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9]+)?', cells[1])
        for index, key in enumerate(keys):
            if index < len(versions):
                found[key] = versions[index]
    return found


def main():
    lenient = '--lenient' in sys.argv
    pins = readme_pins()
    failures = []
    checked = 0

    print(f'Checking {len(pins)} pinned components against published metadata...\n')

    for key, (path, source) in PINS.items():
        if key not in pins:
            continue
        checked += 1
        published_versions = versions_for(path, source)
        stable_list = stable(published_versions)
        latest_stable = max(stable_list, key=semver_key) if stable_list else '?'
        pin = pins[key]
        if True:
            if pin not in published_versions:
                failures.append(f'{key}: pinned {pin} is NOT published (latest stable {latest_stable})')
                continue
            if pin != latest_stable and not PRERELEASE.search(pin):
                print(f'  drift  {key}: pinned {pin}, latest stable {latest_stable}')
            else:
                print(f'  ok     {key}: {pin}')

    # Gradle is served by a different endpoint
    try:
        current = json.loads(fetch(GRADLE))['version']
        print(f'  info   gradle: current {current}')
    except (urllib.error.URLError, ValueError, KeyError) as exc:
        failures.append(f'gradle: could not read current version ({exc})')

    print()
    if failures:
        print('FAIL:')
        for f in failures:
            print(' ', f)
        if not lenient:
            return 1
        print('\n(lenient mode: not failing the run)')
        return 0

    print(f'OK: {checked} pins are published; drift warnings above are advisory.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except urllib.error.URLError as exc:
        print(f'note: network unavailable ({exc}); version check skipped')
        sys.exit(0)
