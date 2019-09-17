from buddy.validation_classes import Md5sumValidator
from buddy.file_utils import read_yaml


class ValidationWorkflow:
    def __init__(self, validators):
        self.validators = validators

    def __eq__(self, other):
        return self.validators == other.validators

    @classmethod
    def from_yaml_dict(cls, yaml_dictionary):
        """
        User can make a ValidationWorkflow from a dictionary that defines the
        validation tests to be applied within that Workflow.

        :param yaml_dictionary: A dictionary that defines the validation tests.
        This should be of the form: {test1: {input_file: ..., expected_md5sum:
        ...}, test2: {...}, ...}.
        :return: A ValidationWorkflow object.
        """
        return cls(cls.parse_validator_details(yaml_dictionary))

    @classmethod
    def from_yaml_file(cls, yaml_file):
        """
        User can make a ValidationWorkflow from a yaml-file that defines the
        validation tests to be applied within that Workflow.

        :param yaml_file A file that defines the validation tests.
        The file should be of the form:
            test1:
                input_file: some_file
                expected_md5sum: some_hash_code

        :return: A ValidationWorkflow object.
        """
        return cls.from_yaml_dict(read_yaml(yaml_file))

    def get_failing_validators(self):
        return {k: v for k, v in self.validators.items() if not v.is_valid()}

    def format_failure_report(self):
        def format_single_failure(validator):
            return "\t".join(
                [
                    "[FAILURE]",
                    "test_name:{}".format(validator.test_name),
                    "test_type:{}".format(validator.test_type),
                    "input_file:{}".format(validator.input_file),
                ]
            )

        failures = self.get_failing_validators()
        return "\n".join(map(format_single_failure, failures.values()))

    @staticmethod
    def parse_validator_details(yaml_dictionary):
        """
        Convert a set of validation-test definitions into a set of Validator
        objects that can be used to apply those tests.
        - To compare md5sum between a file and a string, one of the keys must
        be `expected_md5sum` and another must be `input_file`.

        :param yaml_dictionary: A dictionary that defines a set of validation
        tests. This should be of the form: {test1: {input_file: ...,
        expected_md5sum: ...}, test2: {...}, ...}.
        :return: A dictionary containing, for each validation test in the
        dictionary, a Validator object.
        """

        validators = {
            k: Md5sumValidator(test_name=k, **v) for k, v in yaml_dictionary.items()
        }

        return validators
