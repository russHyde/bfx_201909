"""
Functions for identifying which git repos need to be cloned for the current
project, and for cloning them
"""

import argparse

from buddy.file_utils import read_yaml
from buddy.git_classes import ExternalRepository


def parse_repository_details(yaml_dictionary):
    """
    Extracts details of git repositories: where are they stored, where are they
    to be copied, which commit should be checked out?
    """
    repositories = {
        k: ExternalRepository(v["url"], v["commit"], v["output"])
        for k, v in yaml_dictionary.items()
    }
    return repositories


def import_repository_details(yaml_file):
    """
    Reads and extracts repository information from a yaml file
    """
    yaml_dict = read_yaml(yaml_file)
    repositories = parse_repository_details(yaml_dict)
    return repositories


def run_workflow(yaml_file):
    """
    For each git repository mentioned in the yaml file, clone it and checkout
    the required commit.
    """
    repositories = import_repository_details(yaml_file)
    for _, repo in repositories.items():
        repo.clone()
        repo.checkout()


def define_command_arg_parser():
    """
    Get a parser that extracts the command args used when calling this program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("git_yaml", nargs=1)
    return parser


if __name__ == "__main__":
    ARGS = define_command_arg_parser().parse_args()
    run_workflow(ARGS.git_yaml[0])
