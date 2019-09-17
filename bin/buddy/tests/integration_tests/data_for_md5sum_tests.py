import hashlib


def empty_md5():
    return hashlib.md5("".encode("utf-8")).hexdigest()
