#!/bin/sh
# init-agent-rules.sh - copy the playbook's agent rules into an Android project.
#
# Usage:
#   ./scripts/init-agent-rules.sh /path/to/android-project [--multimodule]
#
# Copies templates/AGENTS.md (or AGENTS_multimodule.md with --multimodule) to
# <target>/AGENTS.md, and docs/CODE_SNIPPETS.md to <target>/docs/CODE_SNIPPETS.md.
# Refuses to overwrite an existing AGENTS.md unless --force is passed.

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

usage() {
  cat <<'USAGE'
Usage: init-agent-rules.sh <target-android-project> [options]

Options:
  --multimodule   Install the multi-module template (5+ features)
                  instead of the single-module default.
  --force         Overwrite an existing AGENTS.md in the target.
  -h, --help      Show this help.

Example:
  ./scripts/init-agent-rules.sh ~/dev/my-app
  ./scripts/init-agent-rules.sh ~/dev/big-app --multimodule
USAGE
}

TARGET=""
MULTI=0
FORCE=0

for arg in "$@"; do
  case "$arg" in
    --multimodule) MULTI=1 ;;
    --force) FORCE=1 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "error: unknown option '$arg'" >&2; usage >&2; exit 2 ;;
    *) TARGET="$arg" ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "error: target project path is required" >&2
  usage >&2
  exit 2
fi

if [ ! -d "$TARGET" ]; then
  echo "error: '$TARGET' is not a directory" >&2
  exit 2
fi

if [ "$MULTI" -eq 1 ]; then
  SRC_AGENTS="$REPO_DIR/templates/AGENTS_multimodule.md"
  FLAVOUR="multi-module (5+ features)"
else
  SRC_AGENTS="$REPO_DIR/templates/AGENTS.md"
  FLAVOUR="single-module (1-4 screens)"
fi
SRC_SNIPPETS="$REPO_DIR/docs/CODE_SNIPPETS.md"

for f in "$SRC_AGENTS" "$SRC_SNIPPETS"; do
  if [ ! -f "$f" ]; then
    echo "error: missing source file '$f' - is this script inside the repository?" >&2
    exit 1
  fi
done

TARGET_ABS=$(CDPATH= cd -- "$TARGET" && pwd)
if [ "$TARGET_ABS" = "$REPO_DIR" ]; then
  echo "error: refusing to install the app rules into the playbook repository itself" >&2
  echo "       (the root AGENTS.md here is the agent protocol, not an app template)" >&2
  exit 2
fi

DEST_AGENTS="$TARGET/AGENTS.md"
if [ -e "$DEST_AGENTS" ] && [ "$FORCE" -ne 1 ]; then
  echo "refusing to overwrite existing '$DEST_AGENTS' (pass --force to replace it)" >&2
  exit 1
fi

mkdir -p "$TARGET/docs"
cp "$SRC_AGENTS" "$DEST_AGENTS"
cp "$SRC_SNIPPETS" "$TARGET/docs/CODE_SNIPPETS.md"

echo "Android agent rules installed into: $TARGET"
echo "  template : $FLAVOUR"
echo "  AGENTS.md                     <- templates/$(basename "$SRC_AGENTS")"
echo "  docs/CODE_SNIPPETS.md         <- docs/CODE_SNIPPETS.md"
echo ""
echo "Next, from $TARGET:"
echo "  ./gradlew assembleDebug --stacktrace"
echo "  ./gradlew testDebugUnitTest"
echo "  ./gradlew lintDebug"
echo ""
echo "Then replace the bracketed placeholders in AGENTS.md (app name, package)."
