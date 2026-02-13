"""Tests for utilities_web.processor — run_subprocess and run_callable."""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from utilities_web.processor import run_callable, run_subprocess


# ---------------------------------------------------------------------------
# run_subprocess
# ---------------------------------------------------------------------------

class TestRunSubprocess:
    def test_placeholder_substitution(self):
        """Placeholders like {field} are replaced with form_data values."""
        with patch("utilities_web.processor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="ok", stderr=""
            )
            run_subprocess(
                ["echo", "{greeting}", "{name}"],
                {"greeting": "hello", "name": "world"},
            )
            mock_run.assert_called_once_with(
                ["echo", "hello", "world"],
                capture_output=True,
                text=True,
                timeout=None,
            )

    def test_success_when_returncode_zero(self):
        with patch("utilities_web.processor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0, stdout="output text", stderr=""
            )
            result = run_subprocess(["cmd"], {})
            assert result["status"] == "success"
            assert result["output"] == "output text"
            assert result["data"]["returncode"] == 0

    def test_error_when_returncode_nonzero(self):
        with patch("utilities_web.processor.subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=1, stdout="", stderr="something failed"
            )
            result = run_subprocess(["cmd"], {})
            assert result["status"] == "error"
            assert result["output"] == "something failed"
            assert result["data"]["returncode"] == 1

    def test_timeout_expired(self):
        with patch("utilities_web.processor.subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="cmd", timeout=5)
            result = run_subprocess(["cmd"], {}, timeout=5)
            assert result["status"] == "error"
            assert "timed out" in result["output"]

    def test_file_not_found(self):
        with patch("utilities_web.processor.subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("No such file")
            result = run_subprocess(["nonexistent_binary"], {})
            assert result["status"] == "error"
            assert "Command not found" in result["output"]
            assert "nonexistent_binary" in result["output"]


# ---------------------------------------------------------------------------
# run_callable
# ---------------------------------------------------------------------------

class TestRunCallable:
    def test_handler_returning_dict_with_status(self):
        """If the handler returns a dict containing 'status', it is returned as-is."""
        handler = MagicMock(return_value={"status": "success", "output": "done", "data": {}})
        result = run_callable(handler, {"x": "1"})
        handler.assert_called_once_with(x="1")
        assert result == {"status": "success", "output": "done", "data": {}}

    def test_handler_returning_plain_string(self):
        """A plain string is wrapped in the standard result format."""
        handler = MagicMock(return_value="hello world")
        result = run_callable(handler, {})
        assert result["status"] == "success"
        assert result["output"] == "hello world"
        assert result["data"] == {}

    def test_handler_raising_exception(self):
        """Exceptions are caught and returned as error results."""
        handler = MagicMock(side_effect=RuntimeError("boom"))
        result = run_callable(handler, {})
        assert result["status"] == "error"
        assert "boom" in result["output"]
        assert result["data"] == {}
