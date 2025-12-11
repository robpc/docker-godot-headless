#!/bin/bash
#################################################################
# update-godot.sh
#
# Automates the changes needed when adding/updating the version
# of Godot
#################################################################

# Arguments
VERSION=$1
PREVIOUS=$2

if [ -z "${VERSION}" ]; then
    echo "ERROR: Missing version in first argument"
    exit 1
fi

if [ -z "${PREVIOUS}" ]; then
    echo "ERROR: Missing previous version in second argument"
    exit 1
fi

# Files to change
VERSIONS_FILE=godot4/versions.yml
DOCKER_FILE=godot4/Dockerfile
README_FILE=README.md

if [ ! -f "${VERSIONS_FILE}" -o ! -f "${DOCKER_FILE}" -o ! -f "${README_FILE}" ]; then
    echo "ERROR: Could not find files, perhaps in the wrong directory?"
    exit 1
fi

VERSION_PATTERN='[0-9]+\.[0-9]+(\.[0-9]+)?'

# =====================
# Versions file
# =====================

python3 - <<'PY' "${VERSIONS_FILE}" "${VERSION}"
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
version = sys.argv[2]
pattern = r"[0-9]+\.[0-9]+(\.[0-9]+)?"
text = path.read_text()

def replace_latest(match: re.Match[str]) -> str:
    return f"{match.group(1)}{version}"

text, latest_count = re.subn(rf"(^latest:\s*){pattern}", replace_latest, text, count=1, flags=re.MULTILINE)
if latest_count == 0:
    raise SystemExit("Could not update latest field in versions file")

def replace_first_version(match: re.Match[str]) -> str:
    return f"{match.group(1)}{version}"

text, version_count = re.subn(rf"(^versions:\s*\n\s*-\s*){pattern}", replace_first_version, text, count=1, flags=re.MULTILINE)
if version_count == 0:
    raise SystemExit("Could not update versions list in versions file")

path.write_text(text)
PY

# =====================
# Dockerfile
# =====================
sed --in-place --regexp-extended '/ARG GODOT_VERSION=/'"s/${VERSION_PATTERN}/${VERSION}/" "${DOCKER_FILE}"

# =====================
# README
# =====================

# Example github action
sed --in-place --regexp-extended '/image: godot-headless:/'"s/${VERSION_PATTERN}/${VERSION}/" "${README_FILE}"
# List of tag variations
sed --in-place --regexp-extended '/The tags follow the Godot version/,/Legacy/ { s/'"${VERSION_PATTERN}/${VERSION}"'/g }' "${README_FILE}"
# List of older versions supported
legacy_version_expression='/Prior versions:/ { 
    n;
    n;
    i- `'"${PREVIOUS}"'`
}'
sed --in-place --regexp-extended "${legacy_version_expression}" "${README_FILE}"
