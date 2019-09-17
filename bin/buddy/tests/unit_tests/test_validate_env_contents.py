import os, sys, subprocess

from buddy.validate_env_contents import (
    python_matches_conda,
    conda_env_matches_expected,
    rscript_matches_conda,
)


class TestCondaEnvIsActivated(object):
    def test_with_no_conda_env(self, mocker):
        mocker.patch.dict("os.environ", values={}, clear=True)
        assert not conda_env_matches_expected("/my/conda/env")

    def test_with_matching_conda_env(self, mocker):
        mocker.patch.dict(
            "os.environ", values={"CONDA_PREFIX": "/my/conda/env"}, clear=True
        )
        assert conda_env_matches_expected("/my/conda/env")

    def test_with_mismatching_conda_env(self, mocker):
        mocker.patch.dict(
            "os.environ", values={"CONDA_PREFIX": "/some/other/env"}, clear=True
        )
        assert not conda_env_matches_expected("/my/conda/env")


# System python should match conda-env python


class TestPythonInCondaEnv(object):
    def test_with_no_conda_env(self, mocker):
        mocker.patch.dict("os.environ", values={}, clear=True)
        mocker.patch.object(sys, "executable", "/global/bin/python")
        assert not python_matches_conda()

    def test_with_matching_conda_env(self, mocker):
        mocker.patch.dict("os.environ", {"CONDA_PREFIX": "/my/conda/env"}, clear=True)
        mocker.patch.object(sys, "executable", "/my/conda/env/bin/python")
        assert python_matches_conda()

    def test_with_mismatching_conda_env(self, mocker):
        mocker.patch.dict("os.environ", {"CONDA_PREFIX": "/my/conda/env"}, clear=True)
        mocker.patch.object(sys, "executable", "/some/other/env/bin/python")
        assert not python_matches_conda()


# If r is required, system Rscript should match conda-env Rscript


class TestRscriptInCondaEnv(object):
    def mock_which(*args, **kwargs):
        """Mocks a subprocess call to `which Rscript`"""
        return subprocess.CompletedProcess(
            args=None, returncode=0, stdout=b"/my/conda/env/bin/Rscript\n"
        )

    def test_with_no_conda_env(self, mocker, monkeypatch):
        mocker.patch.dict("os.environ", values={}, clear=True)
        monkeypatch.setattr(subprocess, "run", self.mock_which)
        assert not rscript_matches_conda()

    def test_with_matching_conda_env(self, mocker, monkeypatch):
        mocker.patch.dict(
            "os.environ", values={"CONDA_PREFIX": "/my/conda/env"}, clear=True
        )
        monkeypatch.setattr(subprocess, "run", self.mock_which)
        assert rscript_matches_conda()

    def test_with_mismatching_conda_env(self, mocker, monkeypatch):
        mocker.patch.dict(
            "os.environ", values={"CONDA_PREFIX": "/some/other/env"}, clear=True
        )
        monkeypatch.setattr(subprocess, "run", self.mock_which)
        assert not rscript_matches_conda()

    def test_without_rscript(self, mocker, monkeypatch):
        mocker.patch.dict(
            "os.environ", values={"CONDA_PREFIX": "/my/conda/env"}, clear=True
        )

        def local_mock_which(*args, **kwargs):
            return subprocess.CompletedProcess(args=None, returncode=1, stdout=b"")

        monkeypatch.setattr(subprocess, "run", local_mock_which)
        assert not rscript_matches_conda()


# If r is required, and Rscript is not available, an informative error should
# be thrown
