"""
Module to print the available and installed versions of a package in the repository.
"""

import argparse
import sys
from typing import NamedTuple, Optional

from getversions.core import get_avail_installed_versions, get_installed_version

if sys.version_info[:2] >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


class ParsedArgs(NamedTuple):
    """Parsed agruments."""

    package: str
    installed_only: bool


def parse_args(args: Optional[Sequence[str]] = None) -> ParsedArgs:
    """Parse an iterable of arguments, or the command line arguments."""
    parser = argparse.ArgumentParser(
        prog="python -m getversions.getversions",
        description=" ".join(
            (
                "Get versions of a package that are available in the repository,",
                "and installed for the current interpreter.",
            ),
        ),
    )
    parser.add_argument(
        "package", help="Name of the package for which to get version info"
    )
    parser.add_argument(
        "-i",
        "--installed-only",
        action="store_true",
        help="Print only the installed version",
    )
    parsed_args = parser.parse_args(args)
    return ParsedArgs(parsed_args.package, parsed_args.installed_only)


def print_avail_versions(package: str) -> None:
    """
    Print the available versions from the repository, and if the installed version
    is among them, mark it.
    """
    avail_versions, installed_version = get_avail_installed_versions(package)
    for version in avail_versions:
        if version != installed_version:
            print(version)
        else:
            print(f"*{version}")


def print_installed_version(package: str) -> None:
    """Print the installed version."""
    print(get_installed_version(package))


def main(args: Optional[Sequence[str]] = None) -> int:
    """
    Process command line arguments if they are present, and call the appropriate
    function with the relevant arguments.

    Args:
        args: Arguments to be processed by `parse_args`. Defaults to the command
        line arguments.

    Returns:
        0 to indicate success.
    """
    parsed_args = parse_args(args)
    if parsed_args.installed_only:
        print_installed_version(parsed_args.package)
    else:
        print_avail_versions(parsed_args.package)
    return 0


if __name__ == "__main__":
    raise (SystemExit(main()))
