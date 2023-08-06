"""
Module to determine if the installed version of a package is available in the
repository.
"""

import argparse
import sys
from typing import NamedTuple, Optional

from getversions.core import get_avail_installed_versions

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


class ParsedArgs(NamedTuple):
    """Parsed agruments."""

    package: str


def parse_args(args: Optional[Sequence[str]] = None) -> ParsedArgs:
    """Parse an iterable of arguments, or the command line arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m getversions.newinstalledversion",
        description=" ".join(
            (
                "Determine if the version of a package installed for the"
                "current interpretor is not yet available in the repository.",
            )
        ),
    )
    parser.add_argument(
        "package", help="Name of the package for which to get version info"
    )
    parsed_args = parser.parse_args(args)
    return ParsedArgs(parsed_args.package)


def is_installed_version_in_repo(package: str) -> bool:
    """Return `True` if the installed version is available in the repository."""
    avail_versions, installed_version = get_avail_installed_versions(package)
    return installed_version in avail_versions


def main(args: Optional[Sequence[str]] = None) -> int:
    """
    Process command line arguments if they are present, and call
    `is_installed_version_in_repo` with the relevant arguments.

    Args:
        args: Arguments to be processed by `parse_args`. Defaults to the command
        line arguments.

    Returns:
        0 if the installed version is not available in the repository, and is hence
        a new version.
    """
    parsed_args = parse_args(args)
    return is_installed_version_in_repo(parsed_args.package)


if __name__ == "__main__":
    raise (SystemExit(main()))
