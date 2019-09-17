"""
Simple file manipulation functions

- `yaml` files must be read using `yaml.safe_load` for security purposes
"""

import yaml


def read_yaml(yaml_file):
    """
    Reads all data stored in a yaml file; returns a dictionary storing the
    key-value pairs within the file
    """
    yaml_dict = yaml.safe_load(open(yaml_file, "r"))
    if yaml_dict is None:
        return {}
    return yaml_dict
