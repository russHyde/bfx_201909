"""
Checks whether a conda environment has been activated. Verifies the path to that
environment and verifies that the environment contains an appropriate python and
(optionally) Rscript interpreter.
"""

import os
import sys
import subprocess


def conda_env_is_activated():
    """
    The environment variable "CONDA_PREFIX" is defined when a conda environment
    is activated. This checks if that variable has been set.

    :return: bool
    """
    return "CONDA_PREFIX" in os.environ


def conda_env_matches_expected(conda_prefix):
    """
    Does the activated conda environment agree with the conda environment that
    the user expected to have activated for this project?

    :param conda_prefix: The expected path of the project-specific `conda`
    environment
    :return: bool
    """
    return conda_env_is_activated() and os.environ["CONDA_PREFIX"] == conda_prefix


def python_matches_conda():
    """
    Is the path to the active `python` consistent with the current `conda`
    environment? There should be a python in <my_conda_env>/bin/python

    :return: bool
    """
    return (
        conda_env_is_activated()
        and os.path.join(os.environ["CONDA_PREFIX"], "bin", "python") == sys.executable
    )


def rscript_matches_conda():
    """
    Is the path to the active `Rscript` consistent with the current `conda`
    environment? If R is used in the current project, there should be an
    Rscript in <my_conda_env>/bin/Rscript

    :return: bool
    """
    if not conda_env_is_activated():
        return False

    expected_rscript = os.path.join(os.environ["CONDA_PREFIX"], "bin", "Rscript")
    which_rscript = subprocess.run(args=["which", "Rscript"], stdout=subprocess.PIPE)
    observed_rscript = which_rscript.stdout.decode("utf-8").strip()
    return expected_rscript == observed_rscript


def run_workflow(conda_prefix, is_r_required):
    """
    Check that a conda-environment is activated, that it has the expected path
    and that it contains the active `python` and (optionally) `Rscript`
    interpreters.
    :param conda_prefix: The expected path to the conda environment
    :type conda_prefix: str
    :param is_r_required: Should the conda environment contain R?
    :type is_r_required: bool
    """
    assert (
        conda_env_is_activated()
    ), "project should be running in a `conda` environment"
    assert conda_env_matches_expected(
        conda_prefix
    ), "path to the `conda` environment should be `{}`".format(conda_prefix)
    assert (
        python_matches_conda()
    ), "`python` should be present in the `conda` environment"
    if is_r_required:
        assert (
            rscript_matches_conda()
        ), "`Rscript` should be present in the `conda` environment"


if __name__ == "__main__":
    # TODO: add argparse command parser for:
    # - conda-prefix [String]
    # - is-r-required [0/1]
    CONDA_PREFIX = sys.argv[1]
    IS_R_REQUIRED = bool(int(sys.argv[2]))
    run_workflow(CONDA_PREFIX, IS_R_REQUIRED)
