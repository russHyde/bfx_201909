import sh

from textwrap import dedent
from pytest_mock import mocker

from buddy.validate_file_contents import run_workflow
from tests.integration_tests.data_for_md5sum_tests import empty_md5


# The program
# .. should not print anything if all validation tests pass


class TestMd5sumWorkflow(object):
    def test_nothing_printed_when_all_tests_pass(self, tmpdir, mocker):
        yaml = dedent(
            """
            test1:
                input_file: empty_file
                expected_md5sum: {}
            """
        ).format(empty_md5())

        with sh.pushd(tmpdir):
            sh.touch("empty_file")
            with open("config.yaml", "w") as f:
                print(yaml, file=f)

            mocker.patch("builtins.print")
            run_workflow("config.yaml")
            print.assert_not_called()
