def repo_data1():
    return "https://some_url.org", "a1b2c3d", "./store/me/here/repo_name"


def repo_dict1():
    return dict(zip(["url", "commit", "output"], repo_data1()))


def repo_data2():
    return "git@github.com:user/my_package.git", "zyx9876", "my_local_package"


def repo_dict2():
    return dict(zip(["url", "commit", "output"], repo_data2()))


def yaml_document():
    return """
    repo1:
        url: https://some_url.org
        commit: a1b2c3d
        output: ./store/me/here/repo_name
    repo2:
        url: git@github.com:user/my_package.git
        commit: zyx9876
        output: my_local_package
    """
