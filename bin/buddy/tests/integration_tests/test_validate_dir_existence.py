import os
import sh
import pytest

from textwrap import dedent
from pytest_mock import mocker

from buddy.validate_dir_existence import run_workflow


class TestDirExistence(object):
    def test_with_existing_dir(self, tmpdir, mocker):
        yaml = dedent(
            """
            - ./existing_dir/
            - an_existing_dir
            - a_dir/with_a_subdir
            """
        )
        # move into tmpdir
        # write the yaml file
        # make the yaml-stated directories exist
        # ensure the workflow exits with no error and prints nothing
        with sh.pushd(tmpdir):
            with open("valid.yaml", "w") as f:
                print(yaml, file=f)

            for d in ["existing_dir", "an_existing_dir", "a_dir/with_a_subdir"]:
                os.makedirs(d, exist_ok=True)
                assert os.path.isdir(d)

            mocker.patch("builtins.print")
            run_workflow("valid.yaml")
            print.assert_not_called()

    def test_with_nonexisting_dir(self, tmpdir):
        yaml = dedent(
            """
            - this_doesnt_exist/
            """
        )
        # move into tmpdir
        # make some dirs that aren't stated in the yaml
        # ensure the workflow exits 1 and prints a message re the missing
        #   directory
        with sh.pushd(tmpdir):
            with open("invalid.yaml", "w") as f:
                print(yaml, file=f)

            for d in ["some_other_dir"]:
                os.makedirs(d, exist_ok=True)
                assert os.path.isdir(d)

            with pytest.raises(FileNotFoundError) as e:
                run_workflow("invalid.yaml")

    def test_with_no_stated_dirs(self, tmpdir, mocker):
        yaml = dedent(
            """
            # some_comment
            
            
            """
        )
        # pass an empty yaml
        # move into tmpdir
        # ensure the workflow exits 0 and prints nothing
        with sh.pushd(tmpdir):
            with open("empty.yaml", "w") as f:
                print(yaml, file=f)

            for d in ["existing_dir", "an_existing_dir", "a_dir/with_a_subdir"]:
                os.makedirs(d, exist_ok=True)
                assert os.path.isdir(d)

            mocker.patch("builtins.print")
            run_workflow("empty.yaml")
            print.assert_not_called()

    def test_with_tilde_prefixed_dirs(self, tmpdir, mocker):
        yaml = dedent(
            """
            # some_comment
            ~/in_my_home_dir/
            
            """
        )
        # pass an empty yaml
        # move into tmpdir
        # ensure the workflow exits 0 and prints nothing

        yaml_path = "empty.yaml"
        with sh.pushd(tmpdir):
            with open(yaml_path, "w") as f:
                print(yaml, file=f)

            for d in ["existing_dir", "an_existing_dir", "a_dir/with_a_subdir"]:
                os.makedirs(d, exist_ok=True)
                assert os.path.isdir(d)

            with pytest.raises(Exception) as e:
                mocker.patch("builtins.print")
                run_workflow(yaml_path)
                print.assert_called_with(
                    "Don't use tilde `~` in dirnames in `validate_dir_existence.py`"
                )
