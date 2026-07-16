#!/usr/bin/env bash
# Build the brew package from the committed tree (git archive HEAD), render
# the formula template against the local tarball, install it, verify the
# installed CLI end-to-end with a real backup, then uninstall.
#
# Refuses to run if macprefs is already installed via brew (it would clobber
# the real install) unless FORCE=1 is set.
set -euo pipefail

VERSION=$(python3 -c "import version; print(version.__version__.lstrip('v'))")
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

if brew list macprefs &>/dev/null && [ "${FORCE:-0}" != "1" ]; then
    echo "macprefs is already installed via brew - refusing to clobber it." >&2
    echo "Re-run with FORCE=1 to uninstall it and test anyway." >&2
    exit 1
fi

TARBALL="$TMP/macprefs-$VERSION.tar.gz"
git archive --prefix="macprefs-$VERSION/" -o "$TARBALL" HEAD
SHA=$(shasum -a 256 "$TARBALL" | cut -d' ' -f1)

sed -e "s|url \".*\"|url \"file://$TARBALL\"|" \
    -e "s|###sha256###|$SHA|" \
    macprefs.template.rb > "$TMP/macprefs.rb"

# Homebrew requires formulae to live in a tap; use a throwaway local one.
TAP="macprefs-ci/local"
brew untap -f "$TAP" >/dev/null 2>&1 || true
brew tap-new --no-git "$TAP" >/dev/null
trap 'brew uninstall --force macprefs >/dev/null 2>&1 || true; brew untap -f "$TAP" >/dev/null 2>&1 || true; rm -rf "$TMP"' EXIT
cp "$TMP/macprefs.rb" "$(brew --repository "$TAP")/Formula/macprefs.rb"

brew install "$TAP/macprefs"

# Formula's own test block (runs `macprefs --help`).
brew test "$TAP/macprefs"

INSTALLED_VERSION=$(macprefs --version)
echo "installed: $INSTALLED_VERSION"
echo "$INSTALLED_VERSION" | grep -q "$VERSION"

# End-to-end: a real backup into a throwaway dir. Backup only reads system
# state and writes to MACPREFS_BACKUP_DIR, so this is safe anywhere.
MACPREFS_BACKUP_DIR="$TMP/backup" macprefs backup
test -d "$TMP/backup/preferences"

echo "brew package build + install + backup smoke test: OK"
