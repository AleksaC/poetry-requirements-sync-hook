#!/usr/bin/env python

from __future__ import print_function

import argparse
import subprocess
import sys


def main(argv=None):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filenames", nargs="*", help="Filenames pre-commit believes are changed.",
    )

    args = parser.parse_args(argv)

    # This makes an assumption that this code is run from root of the project, make sure
    # this holds. It also only covers the case where pyproject.toml is in root directory
    # allow arbitrarily nesting

    for filename in args.filenames:
        if "pyproject.toml" in filename:
            break  # TODO: Take path to pyproject.toml here
    else:
        return 0

    res = subprocess.run(
        ["poetry", "export", "--without-hashes", "-f", "requirements.txt"],
        stdout=subprocess.PIPE
    )

    updated = res.stdout.decode()

    reqs_filename = "requirements.txt"

    try:
        with open(reqs_filename, "r+") as f:
            if f.read().splitlines() == updated.splitlines():
                print("%s already synced with pyproject.toml" % reqs_filename)
                return 0
            else:
                f.seek(0)
                f.write(updated)
                f.truncate()
    except FileNotFoundError:
        with open(reqs_filename, "w") as f:
            f.write(updated)

    subprocess.run(["git", "add", reqs_filename])

    print("%s synced with pyproject.toml" % reqs_filename)

    return 0


if __name__ == "__main__":
    argv = None

    if len(sys.argv) == 1:
        files = subprocess.run(
            ["git", "diff", "--cached", "--name-only"], stdout=subprocess.PIPE
        )
        argv = files.stdout.decode().strip().split("\n")

    sys.exit(main(argv))
