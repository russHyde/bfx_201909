"""
Functions to make links from one file location (link) to another (target)
"""

import argparse
import errno
import os
import os.path
import sys


def add_relative_symlink(target, link):
    """
    Create a symbolic link from `link` to `target`.

    Pass-through if the link exists and already points to target.
    Ensure the target is referred to relative to the link location
    and make any intervening directories.

    Throw errors if:
    - target does not exist
    - link already exists and is not a link
    - link exists but does not point to target

    :param target: An existing file/dir/link on the filesystem
    :param link: A filepath; a softlink from this location to
      `target` will be made.
    :return: Null
    """

    if not os.path.exists(target):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), target)

    try:
        dname = os.path.dirname(link)
        if dname and not os.path.isdir(dname):
            os.makedirs(dname, exist_ok=True)
        relative_target_path = os.path.relpath(target, start=dname)
        os.symlink(relative_target_path, link)
    except FileExistsError as err:
        if not os.path.islink(link):
            print("Attempt to convert a file to a link", file=sys.stderr)
            raise err
        if os.readlink(link) != relative_target_path:
            print("Attempt to rewrite a link", file=sys.stderr)
            raise err


def define_command_arg_parser():
    """
    Get a parser that extracts the command args used when calling this
    program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs=1)
    parser.add_argument("link", nargs=1)
    return parser


if __name__ == "__main__":
    ARGS = define_command_arg_parser().parse_args()
    add_relative_symlink(ARGS.target[0], ARGS.link[0])
