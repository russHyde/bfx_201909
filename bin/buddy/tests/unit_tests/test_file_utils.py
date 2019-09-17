from mock import patch, mock_open

from buddy.file_utils import read_yaml
from tests.unit_tests.data_for_git_tests import yaml_document, repo_dict1, repo_dict2


class TestReadYaml(object):
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_yaml(self, m):
        assert read_yaml("some_file") == {}

    @patch("builtins.open", new_callable=mock_open, read_data=yaml_document())
    def test_nonempty_yaml(self, m):
        assert read_yaml("some_file") == {"repo1": repo_dict1(), "repo2": repo_dict2()}
