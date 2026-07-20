#!/usr/bin/env python3
"""Fail if a config file shadows a [tool.*] section in pyproject.toml.

Every tool configured in pyproject.toml also discovers standalone config
files, and the standalone file wins -- mostly silently: uv.toml disables
[tool.uv] with no warning, an empty pytest.ini shadows
[tool.pytest.ini_options], and a ruff.toml in a subdirectory replaces
(not extends) the root lint rules for that subtree. This check bans the
whole discovery chain so pyproject.toml stays the single source of truth.

Scans tracked and untracked-unignored files, so a stray local file fails
`rite check` before it is ever committed.
"""

import subprocess
import sys

# basename -> (tool that reads it, what happens when it exists)
FORBIDDEN = {
    "uv.toml": ("uv", "read instead of [tool.uv], which is then ignored with no warning"),
    "pytest.toml": ("pytest", "outranks [tool.pytest.ini_options]"),
    ".pytest.toml": ("pytest", "outranks [tool.pytest.ini_options]"),
    "pytest.ini": ("pytest", "outranks [tool.pytest.ini_options], even when empty"),
    ".pytest.ini": ("pytest", "outranks [tool.pytest.ini_options], even when empty"),
    "ruff.toml": ("ruff", "replaces, not extends, [tool.ruff] for its whole subtree"),
    ".ruff.toml": ("ruff", "replaces, not extends, [tool.ruff] for its whole subtree"),
    "pylintrc": ("pylint", "outranks [tool.pylint.*]"),
    ".pylintrc": ("pylint", "outranks [tool.pylint.*]"),
    "pylintrc.toml": ("pylint", "outranks [tool.pylint.*]"),
    ".pylintrc.toml": ("pylint", "outranks [tool.pylint.*]"),
    "pyrightconfig.json": ("pyright", "always beats [tool.pyright]"),
    ".coveragerc": ("coverage", "outranks pyproject.toml; could weaken the coverage gate"),
    ".gitleaks.toml": ("gitleaks", "auto-loaded; an [allowlist] would weaken the secret scan"),
    "tox.ini": ("pytest/coverage", "its [pytest] and [coverage:*] sections shadow pyproject.toml; this repo does not use tox"),
    "setup.cfg": ("pytest/coverage/pylint", "its tool sections shadow pyproject.toml; this repo does not use setuptools config"),
}


def repo_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [path for path in result.stdout.split("\0") if path]


def main() -> int:
    offenders = []
    for path in repo_files():
        basename = path.rsplit("/", 1)[-1]
        if basename in FORBIDDEN:
            tool, why = FORBIDDEN[basename]
            offenders.append(f"{path} ({tool}: {why})")
    if offenders:
        print("Config files must not shadow pyproject.toml [tool.*] sections:", file=sys.stderr)
        for offender in offenders:
            print(f"  {offender}", file=sys.stderr)
        print(
            "\nDelete the file(s) and keep the config in pyproject.toml. If a standalone"
            "\nfile is genuinely needed, move that tool's config there deliberately and"
            "\nremove its entry from ci/scripts/check-config-shadowing.py.",
            file=sys.stderr,
        )
        return 1
    print(f"config:check ok -- none of the {len(FORBIDDEN)} shadowing config filenames present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
