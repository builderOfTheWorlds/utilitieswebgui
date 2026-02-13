"""Tests for utilities_web.app_factory — create_app and Flask routes."""

from unittest.mock import MagicMock, patch

import pytest

from utilities_web import create_app, TextInput


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TestCreateAppValidation:
    def test_raises_when_neither_command_nor_handler_provided(self):
        with pytest.raises(ValueError, match="Either process_command or process_handler"):
            create_app(title="Test")

    def test_raises_when_both_command_and_handler_provided(self):
        with pytest.raises(ValueError, match="Only one of"):
            create_app(
                title="Test",
                process_command=["echo"],
                process_handler=lambda: None,
            )


# ---------------------------------------------------------------------------
# Route tests using Flask test client
# ---------------------------------------------------------------------------

class TestGetIndex:
    def test_get_returns_200_with_title(self):
        app = create_app(
            title="My Test Utility",
            process_handler=lambda: None,
        )
        app.config["TESTING"] = True
        with app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200
            html = response.data.decode()
            assert "My Test Utility" in html


class TestPostWithHandler:
    def test_post_with_callable_returns_result_page(self):
        def handler(**kwargs):
            return {"status": "success", "output": "All good!", "data": {}}

        app = create_app(
            title="Handler Test",
            inputs=[TextInput(name="greeting", required=False)],
            process_handler=handler,
        )
        app.config["TESTING"] = True
        with app.test_client() as client:
            response = client.post("/", data={"greeting": "hi"})
            assert response.status_code == 200
            html = response.data.decode()
            assert "All good!" in html

    def test_post_missing_required_field_redirects(self):
        app = create_app(
            title="Required Test",
            inputs=[TextInput(name="username", label="Username", required=True)],
            process_handler=lambda **kw: {"status": "success", "output": "", "data": {}},
        )
        app.config["TESTING"] = True
        with app.test_client() as client:
            response = client.post("/", data={})
            # Missing required field triggers a redirect back to the form
            assert response.status_code == 302
            assert "/" in response.headers["Location"]
