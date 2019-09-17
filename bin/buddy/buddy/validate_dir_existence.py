"""
Given a file-path to a .yaml file, this script will check
whether every string in the .yaml file corresponds to a
directory that exists (with respect to the current working
directory)
"""

import argparse
import errno
import os
import os.path
import sys

from buddy.file_utils import read_yaml


def run_workflow(yaml_path):
    """
    Checks that every directory mentioned in the yaml file is really a
    directory

    :param yaml_path: a file-path
    :return:
    """
    dirs = read_yaml(yaml_path)

    for current_dir in dirs:
        if not os.path.expanduser(current_dir) == current_dir:
            print(
                "Don't use tilde `~` in dirnames in `validate_dir_existence.py`",
                file=sys.stderr,
            )
            raise Exception()

        if not os.path.isdir(current_dir):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), current_dir
            )


def define_command_arg_parser():
    """
    Get a parser that extracts the command args used when calling this
    program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("required_dirs_yaml", nargs=1)
    return parser


# ---- run as a script

if __name__ == "__main__":
    ARGS = define_command_arg_parser().parse_args()
    run_workflow(ARGS.required_dirs_yaml[0])
