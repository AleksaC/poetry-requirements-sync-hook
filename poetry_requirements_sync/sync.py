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

    return 0


if __name__ == "__main__":
    argv = None

    if len(sys.argv) == 1:
        files = subprocess.run(
            ["git", "diff", "--cached", "--name-only"], stdout=subprocess.PIPE
        )
        argv = files.stdout.decode().strip().split("\n")

    sys.exit(main(argv))
