import sh
import os
import pytest

from buddy.git_classes import ExternalRepository


def commit_file_and_get_hash(repo_path, file_name):
    with sh.pushd(repo_path):
        sh.touch(file_name)
        sh.git("add", file_name)
        sh.git("commit", "-m", "'adding {}'".format(file_name))
        commit_hash = str(sh.git("rev-parse", "HEAD")).strip()
        return commit_hash


class TestGitInit(object):
    def test_initial_commit(self, tmpdir):
        with sh.pushd(tmpdir):
            repo_name = "my_repo"
            assert not os.path.isdir(repo_name)
            sh.git("init", repo_name)
            assert os.path.isdir(repo_name)


class TestCheckoutHead(object):
    def test_clone_git_repo(self, tmpdir):
        with sh.pushd(tmpdir):
            repo_name = "my_repo"
            sh.git("init", repo_name)

            _ = commit_file_and_get_hash(repo_name, "file1")
            commit_hash_2 = commit_file_and_get_hash(repo_name, "file2")

            copied_repo_name = "my_copy"
            copied_repo = ExternalRepository(repo_name, commit_hash_2, copied_repo_name)
            assert not os.path.isdir(copied_repo_name)
            copied_repo.clone()
            copied_repo.checkout()
            assert os.path.isdir(copied_repo_name)
            with sh.pushd(copied_repo_name):
                assert os.path.isfile("file1")
                assert os.path.isfile("file2")


class TestCheckoutEarlyCommit(object):
    def test_clone_and_checkout(self, tmpdir):
        with sh.pushd(tmpdir):
            repo_name = "my_repo"
            sh.git("init", repo_name)

            commit_hash_1 = commit_file_and_get_hash(repo_name, "file1")
            _ = commit_file_and_get_hash(repo_name, "file2")

            copied_repo_name = "my_copy"
            copied_repo = ExternalRepository(repo_name, commit_hash_1, copied_repo_name)
            copied_repo.clone()
            copied_repo.checkout()

            with sh.pushd(copied_repo_name):
                assert os.path.isfile("file1")
                assert not os.path.isfile("file2")


class TestCheckoutInvalidHash(object):
    def test_checkout_invalid_hash(self, tmpdir):
        with sh.pushd(tmpdir):
            repo_name = "my_repo"
            sh.git("init", repo_name)

            _ = commit_file_and_get_hash(repo_name, "file1")
            _ = commit_file_and_get_hash(repo_name, "file2")

            copied_repo_name = "my_copy"
            copied_repo = ExternalRepository(
                repo_name, "NOTAHASHCODE", copied_repo_name
            )
            copied_repo.clone()
            assert os.path.isdir(copied_repo_name)

            with pytest.raises(sh.ErrorReturnCode):
                copied_repo.checkout()
