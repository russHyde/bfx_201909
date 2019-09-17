"""
Classes for holding details about any git repositories that should be cloned /
copied into a given file-path.
"""

import os
import sys

import sh


class LocalRepository:
    """
    `LocalRepository` defines a local git repo from which a given commit should
    be checked out
    """

    def __init__(self, path, commit):
        self.path = path
        self.commit = commit

    def __eq__(self, other):
        return self.path == other.path and self.commit == other.commit


class ExternalRepository:
    """
    `ExternalRepository` defines an external git repo that is to be downloaded
    and a commit that is to be checked-out.
    """

    # input_path (ie, url or file-path), commit, output_path (local file-path)

    # check that len(commit) >= 7

    def __init__(self, input_path, commit, output_path):
        self.input_path = input_path
        self.commit = commit
        self.output_path = output_path

    def __eq__(self, other):
        return (
            self.input_path == other.input_path
            and self.commit == other.commit
            and self.output_path == other.output_path
        )

    def local_exists(self):
        """
        Does a local-copy of this repository exist?
        """
        return os.path.exists(self.output_path)

    def sha1_matches(self):
        """
        Is the sha1 code for the requested commit a valid sha1 code for the
        requested repository?
        """
        pass

    def clone_into(self, directory):
        """
        Clone the external repository into the stated (possibly temporary)
        directory.
        """
        # TODO:
        # git clone from url to directory
        #
        # try:
        #   sh.git.clone(self.url, directory)
        # except sh.ErrorReturnCode as e:
        #   print(e)
        #   sys.exit(1)
        #
        pass

    def clone(self):
        """
        Clone the requested repository into the directory `output_path` and
        ensure that the requested `commit` is checked out
        """
        if not self.local_exists():
            sh.git("clone", self.input_path, self.output_path)
        # TODO:
        # if output dir is occupied:
        # - check that the sha-1 hash matches the wanted commit
        #   and throw an exception if it doesn't
        # otherwise:
        # - try to clone from the URL to a temp directory
        # - checkout the requested commit (throw exception if it
        #   doesn't exist)
        # - move from the temp directory to output

    def checkout(self):
        try:
            sh.git("-C", self.output_path, "checkout", self.commit)
        except Exception:
            raise
            sys.exit(1)
