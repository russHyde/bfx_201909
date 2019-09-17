from mock import patch, mock_open


import buddy

from buddy.validation_workflow import ValidationWorkflow
from buddy.validation_classes import Md5sumValidator

# ---- test data


def single_md5sum_basics():
    basics = {
        "test_name": "my_test",
        "input_file": "some_file",
        "expected_md5sum": "a" * 32,
    }
    return basics


def single_md5sum_yaml_details():
    basics = single_md5sum_basics()
    details = {
        basics["test_name"]: {
            "input_file": basics["input_file"],
            "expected_md5sum": basics["expected_md5sum"],
        }
    }
    return details


def single_md5sum_yaml_file_contents():
    basics = single_md5sum_basics()
    contents = """
{}:
    input_file: {}
    expected_md5sum: {}
""".format(
        basics["test_name"], basics["input_file"], basics["expected_md5sum"]
    )
    return contents


def single_md5sum_validator():
    basics = single_md5sum_basics()
    validator_dict = {
        basics["test_name"]: Md5sumValidator(
            input_file=basics["input_file"],
            test_name=basics["test_name"],
            expected_md5sum=basics["expected_md5sum"],
        )
    }
    return validator_dict


# ---- tests


class TestValidationWorkflowConstruction(object):
    def test_trivial_workflow_constructor(self):
        validator_dict = {}
        workflow = ValidationWorkflow(validator_dict)
        assert isinstance(workflow, ValidationWorkflow)
        assert validator_dict == workflow.validators

    def test_validation_workflow_constructor(self):
        validator_dict = single_md5sum_validator()
        workflow = ValidationWorkflow(validator_dict)
        assert isinstance(workflow, ValidationWorkflow)
        assert validator_dict == workflow.validators

    def test_validation_workflow_equality(self):
        validator_dict = single_md5sum_validator()
        workflow1 = ValidationWorkflow(validator_dict)
        workflow2 = ValidationWorkflow(validator_dict)
        assert workflow1 == workflow2


class TestValidationWorkflowNonstandardConstruction(object):
    def test_validation_workflow_from_yaml_dictionary(self):
        yaml_dict = single_md5sum_yaml_details()
        validator_dict = single_md5sum_validator()
        workflow = ValidationWorkflow.from_yaml_dict(yaml_dict)
        assert validator_dict == workflow.validators

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=single_md5sum_yaml_file_contents(),
    )
    def test_validation_workflow_from_yaml_file(self, m):
        workflow = ValidationWorkflow.from_yaml_file("mock_file_name")
        validator_dict = single_md5sum_validator()
        assert validator_dict == workflow.validators


class TestGetFailingValidators(object):
    def test_no_validators_means_no_failures(self):
        validator_dict = {}
        workflow = ValidationWorkflow(validator_dict)
        assert {} == workflow.get_failing_validators()

    def test_all_passing_validators_means_no_failures(self, monkeypatch):
        def mock_md5sum(filepath, comment=None):
            return "a" * 32

        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", mock_md5sum)

        validator_dict = single_md5sum_validator()
        workflow = ValidationWorkflow(validator_dict)
        assert {} == workflow.get_failing_validators()

    def test_all_failing_validators(self, monkeypatch):
        def mock_md5sum(filepath, comment=None):
            return "b" * 32

        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", mock_md5sum)

        validator_dict = single_md5sum_validator()
        workflow = ValidationWorkflow(validator_dict)
        assert validator_dict == workflow.get_failing_validators()


class TestValidationReportFormatting(object):
    def test_all_passing_means_no_report(self, monkeypatch):
        # returns a string
        # lines are of form "test_name:XYZ\ttest_type:md5sum\tinput_file:ABC"
        def mock_md5sum(filepath, comment=None):
            return "a" * 32

        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", mock_md5sum)

        validator_dict = single_md5sum_validator()
        workflow = ValidationWorkflow(validator_dict)
        assert "" == workflow.format_failure_report()

    def test_all_failing_gives_report(self, monkeypatch):
        def mock_md5sum(filepath, comment=None):
            return "b" * 32

        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", mock_md5sum)

        validator_dict = single_md5sum_validator()
        workflow = ValidationWorkflow(validator_dict)
        report = "\t".join(
            [
                "[FAILURE]",
                "test_name:my_test",
                "test_type:md5sum",
                "input_file:some_file",
            ]
        )
        assert report == workflow.format_failure_report()


class TestParseValidatorDetails(object):
    def test_md5sum_validators_can_be_parsed(self):
        yaml_dict = {
            "test1": {"input_file": "some_file", "expected_md5sum": "a" * 32},
            "test2": {"input_file": "another_file", "expected_md5sum": "b" * 32},
            "test3": {
                "input_file": "file_x",
                "expected_md5sum": "c" * 32,
                "comment": "#",
            },
        }

        expected_validators = {
            "test1": Md5sumValidator(
                test_name="test1", input_file="some_file", expected_md5sum="a" * 32
            ),
            "test2": Md5sumValidator(
                test_name="test2", input_file="another_file", expected_md5sum="b" * 32
            ),
            "test3": Md5sumValidator(
                test_name="test3",
                input_file="file_x",
                expected_md5sum="c" * 32,
                comment="#",
            ),
        }
        validators = ValidationWorkflow.parse_validator_details(yaml_dict)

        assert all(map(lambda x: isinstance(x, Md5sumValidator), validators.values()))
        assert validators == expected_validators
