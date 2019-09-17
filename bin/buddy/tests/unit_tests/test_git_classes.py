import os
import sh

from pytest_mock import mocker
from buddy.git_classes import ExternalRepository, LocalRepository
from tests.unit_tests.data_for_git_tests import repo_data1, repo_data2


class TestExternalRepositoryClass(object):
    def test_init(self):
        path, commit, output = repo_data1()
        repo = ExternalRepository(path, commit, output)
        assert isinstance(repo, ExternalRepository)
        assert repo.input_path == path
        assert repo.commit == commit
        assert repo.output_path == output

    def test_object_equality(self):
        repo1 = ExternalRepository(*repo_data1())
        repo2 = ExternalRepository(*repo_data1())
        assert repo1 == repo1
        assert repo1 == repo2

    def test_object_inequality(self):
        repo1 = ExternalRepository(*repo_data1())
        repo2 = ExternalRepository(*repo_data2())
        assert repo1 != repo2


class TestLocalRepositoryClass(object):
    def test_init(self):
        path, commit, _ = repo_data1()
        repo = LocalRepository(path, commit)
        assert isinstance(repo, LocalRepository)
        assert repo.path == path
        assert repo.commit == commit


class TestGitClone(object):
    def test_clone_when_no_local_copy(self, mocker):
        # note that we can't patch the function `sh.git.clone`
        mocker.patch("sh.git")
        mocker.patch("os.path.exists", return_value=False)
        repo = ExternalRepository(*repo_data1())
        repo.clone()
        sh.git.assert_called_once_with("clone", repo.input_path, repo.output_path)

    def test_no_clone_when_local_copy_exists(self, mocker):
        mocker.patch("sh.git")
        mocker.patch("os.path.exists", return_value=True)
        repo = ExternalRepository(*repo_data1())
        repo.clone()
        sh.git.assert_not_called()


class TestGitCommit(object):
    def test_git_checkout_is_called(self, mocker):
        mocker.patch("sh.git")
        repo = ExternalRepository(*repo_data1())
        repo.checkout()
        sh.git.assert_called_once_with("-C", repo.output_path, "checkout", repo.commit)


# How do we test that a specific commit of a git repo can be checked out?
# - Unit tests with mocking:
#   - patch sh.git; patch os.path.exists
#   - check that sh.git("checkout", "-C", output_dir, commit) is called
# - But the unit test just replicates the implementation, so really...
# - Require integration tests for this:
#    - Test1:
#      - open temp dir
#      - git init within the temp dir
#      - git commit within the initialised dir
#      - assert that an exception is thrown when trying to checkout a commit
#    other than the hash for the only commit
#    - Test2:
#      - open temp dir
#      - git init within the temp dir
#      - git commit within the initialised dir
#        - first commit adds file1
#        - second commit adds file2
#      - assert that both file1 and file2 exist
#      - obtain the hash for the first commit
#      - checkout the first commit
#      - assert that file1 exists and file2 doesn't
