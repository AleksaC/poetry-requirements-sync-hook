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
    parser.add_argument("--dev", action="store_true")
    parser.add_argument("--without-hashes", action="store_true")

    return parser.parse_args(args)


def get_pyproject_files(filenames):
    files = []

    for filename in filenames:
        if "pyproject.toml" in filename:
            files.append(filename)

    return files


def get_updated_dependencies(base_dir, dev, without_hashes):
    poetry_lock = os.path.join(base_dir, "poetry.lock")
    if not os.path.exists(poetry_lock):
        status = subprocess.call(["poetry", "lock"], cwd=base_dir or ".")

        if status != 0:
            return

        os.system("git add %s" % poetry_lock)

    command = ["poetry", "export"]
    if dev:
        command.append("--dev")
    if without_hashes:
        command.append("--without-hashes")
    command.extend(["-f", "requirements.txt"])

    process = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=base_dir or ".")
    stdout, _ = process.communicate()

    return stdout.decode()


def write_requirements(reqs_filename, updated):
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


def update_requirements(base_dir, dev, without_hashes):
    updated = get_updated_dependencies(base_dir, dev, without_hashes)

    if not updated:
        return

    reqs_filename = "requirements-dev.txt" if dev else "requirements.txt"
    reqs_filename = os.path.join(base_dir, reqs_filename)

    write_requirements(reqs_filename, updated)


def main(argv=None):
    args = parse_arguments(argv)

    files = get_pyproject_files(args.filenames)
    files = filter(lambda file: os.path.exists(file), files)

    for file in files:
        base_dir = os.path.dirname(file)

        try:
            update_requirements(base_dir, False, args.without_hashes)
            if args.dev:
                update_requirements(base_dir, True, args.without_hashes)
        except Exception as e:
            print("Something went wrong...", e, sep="\n")
            return 1

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
