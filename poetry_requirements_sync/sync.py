#!/usr/bin/env python

from __future__ import print_function

import argparse
import errno
import os
import subprocess
import sys


def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filenames", nargs="*", help="Filenames pre-commit believes are changed.",
    )

    return parser.parse_args(args)


def get_pyproject_files(filenames):
    files = []

    for filename in filenames:
        if "pyproject.toml" in filename:
            files.append(filename)

    return files


def get_updated_dependencies(base_dir):
    process = subprocess.Popen(
        ["poetry", "export", "--without-hashes", "-f", "requirements.txt"],
        stdout=subprocess.PIPE,
        cwd=base_dir or "."
    )

    stdout, _ = process.communicate()

    return stdout.decode()


def update_requirements(reqs_filename, updated):
    try:
        with open(reqs_filename, "r+") as f:
            if f.read().splitlines() == updated.splitlines():
                print("%s already synced with pyproject.toml" % reqs_filename)
                return 0
            else:
                f.seek(0)
                f.write(updated)
                f.truncate()
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise
        with open(reqs_filename, "w") as f:
            f.write(updated)

    os.system("git add %s" % reqs_filename)

    print("%s synced with pyproject.toml" % reqs_filename)


def main(argv=None):
    args = parse_arguments(argv)

    files = get_pyproject_files(args.filenames)

    if not files:
        return 0

    for file in files:
        base_dir = os.path.dirname(file)
        updated = get_updated_dependencies(base_dir)
        reqs_filename = os.path.join(base_dir, "requirements.txt")
        update_requirements(reqs_filename, updated)

    return 0


if __name__ == "__main__":
    argv = None

    if len(sys.argv) == 1:
        process = subprocess.Popen(
            ["git", "diff", "--cached", "--name-only"], stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()
        argv = stdout.decode().strip().split("\n")

    sys.exit(main(argv))
