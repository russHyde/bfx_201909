import hashlib


class Md5sumValidator:
    def __init__(self, test_name, input_file, expected_md5sum, comment=None):
        self.test_name = test_name
        self.input_file = input_file
        self.expected_md5sum = expected_md5sum
        self.test_type = "md5sum"
        self.comment = comment

    def is_valid(self):
        return get_md5sum(self.input_file, self.comment) == self.expected_md5sum

    def __eq__(self, other):
        return (
            self.test_name == other.test_name
            and self.input_file == other.input_file
            and self.expected_md5sum == other.expected_md5sum
            and self.comment == other.comment
        )


def get_md5sum(filepath, comment=None):
    """
    Compute the md5 sum for a file.
    If `comment` is specified, ignore all lines of the file that start with
    this comment-character.

    :param filepath: a path to a file, a string.
    :param comment: the comment character for the file; all lines that start
    with this character will be disregarded.

    :return: the md5sum for the file, as a string
    """
    my_predicate = lambda x: True
    if comment is not None:
        my_predicate = lambda x: not x.startswith(comment)

    try:
        my_hash = hashlib.md5()
        with open(filepath, "r") as f:
            for line in filter(my_predicate, f):
                my_hash.update(line.encode("utf-8"))
    except:
        raise

    return my_hash.hexdigest()
