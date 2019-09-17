import buddy.validate_file_contents

from buddy.validation_classes import Md5sumValidator

# user
# .. can ensure the md5sum for a file matches a given value
#


class TestMd5sumValidatorConstruction(object):
    def test_can_construct_md5sum_validator(self):
        validator = Md5sumValidator(
            test_name="test1", input_file="some_file", expected_md5sum="a" * 32
        )
        assert isinstance(validator, Md5sumValidator)


class TestEqualityOfMd5sumValidators(object):
    def test_equal_if_all_fields_are_equal(self):
        validator1 = Md5sumValidator(
            test_name="test1", input_file="some_file", expected_md5sum="a" * 32
        )
        validator2 = Md5sumValidator(
            test_name="test1", input_file="some_file", expected_md5sum="a" * 32
        )
        assert validator1 == validator2

    def test_not_equal_if_comment_char_differs(self):
        validator1 = Md5sumValidator(
            test_name="test1", input_file="some_file", expected_md5sum="a" * 32
        )
        validator2 = Md5sumValidator(
            test_name="test1",
            input_file="some_file",
            expected_md5sum="a" * 32,
            comment="#",
        )
        assert validator1 != validator2


class TestMd5sumValidatorMethods(object):
    @staticmethod
    def mock_return(filepath, comment=None):
        if comment is None:
            return "a" * 32
        else:
            return "b" * 32

    def test_is_valid_detects_matching_md5sum(self, monkeypatch):
        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", self.mock_return)

        validator = Md5sumValidator(
            test_name="test1", input_file="some_file", expected_md5sum="a" * 32
        )

        assert validator.is_valid()

    def test_is_valid_detects_nonmatching_md5sum(self, monkeypatch):
        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", self.mock_return)

        validator = Md5sumValidator(
            test_name="test1", input_file="some_file", expected_md5sum="c" * 32
        )

        assert not validator.is_valid()

    def test_stripping_comment_character_affects_md5sum(self, monkeypatch):
        monkeypatch.setattr(buddy.validation_classes, "get_md5sum", self.mock_return)

        validator = Md5sumValidator(
            test_name="test1",
            input_file="some_file",
            expected_md5sum="b" * 32,
            comment="#",
        )

        assert validator.is_valid()
