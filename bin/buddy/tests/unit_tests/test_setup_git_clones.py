import os

from buddy.setup_git_clones import parse_repository_details
from buddy.git_classes import ExternalRepository

from tests.unit_tests.data_for_git_tests import (
    repo_data1,
    repo_dict1,
    repo_data2,
    repo_dict2,
)


class TestParseRepositoryDetails(object):
    def test_empty_input(self):
        assert parse_repository_details({}) == {}

    def test_single_repository(self):
        repo_yaml = {"repo_name": repo_dict1()}
        assert parse_repository_details(repo_yaml) == {
            "repo_name": ExternalRepository(*repo_data1())
        }

    def test_multiple_repositories(self):
        repo_yaml = {"repo1": repo_dict1(), "repo2": repo_dict2()}
        assert parse_repository_details(repo_yaml) == {
            "repo1": ExternalRepository(*repo_data1()),
            "repo2": ExternalRepository(*repo_data2()),
        }

    def test_malformed_repository_data(self):
        pass


class TestLocalRepositoryExists(object):
    def test_when_local_repo_is_absent(self, monkeypatch):
        def mock_return(path):
            return True

        monkeypatch.setattr(os.path, "exists", mock_return)
        repo = ExternalRepository(*repo_data1())
        assert repo.local_exists()

    def test_when_local_repo_is_present(self, monkeypatch):
        def mock_return(path):
            return False

        monkeypatch.setattr(os.path, "exists", mock_return)
        repo = ExternalRepository(*repo_data1())
        assert not repo.local_exists()
