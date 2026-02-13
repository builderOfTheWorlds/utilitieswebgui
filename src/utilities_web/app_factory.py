"""Flask application factory for utilities_web."""

import logging
import os
from typing import Any, Callable, Dict, List, Optional

from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for

from .input_types import CheckboxInput, FileInput
from .processor import run_callable, run_subprocess

logger = logging.getLogger(__name__)


def create_app(
    title: str = "Utility",
    inputs: Optional[List] = None,
    process_command: Optional[List[str]] = None,
    process_handler: Optional[Callable[..., Any]] = None,
    upload_folder: str = "uploaded_files",
    example_folder: Optional[str] = None,
    enable_examples: bool = False,
    custom_css: Optional[str] = None,
    success_message: str = "Processing complete!",
    error_handler: Optional[Callable[[Exception], Dict[str, Any]]] = None,
) -> Flask:
    """Create a Flask app that renders a form and processes submissions.

    Exactly one of *process_command* or *process_handler* must be provided.

    Args:
        title: Page title shown in the browser and heading.
        inputs: List of input field definitions (FileInput, TextInput, etc.).
        process_command: Subprocess command list with ``{field}`` placeholders.
        process_handler: Python callable that receives form data as kwargs.
        upload_folder: Directory where uploaded files are saved.
        example_folder: Directory containing example files for download.
        enable_examples: Whether to show example download buttons.
        custom_css: Extra CSS injected into the page ``<style>`` tag.
        success_message: Message shown on the result page after success.
        error_handler: Optional callable invoked when processing raises.

    Returns:
        A configured Flask application instance.
    """
    if process_command is None and process_handler is None:
        raise ValueError("Either process_command or process_handler must be provided")
    if process_command is not None and process_handler is not None:
        raise ValueError("Only one of process_command or process_handler may be provided")

    if inputs is None:
        inputs = []

    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    os.makedirs(upload_folder, exist_ok=True)

    # Resolve example files list
    example_files: List[str] = []
    if enable_examples and example_folder and os.path.isdir(example_folder):
        example_files = sorted(os.listdir(example_folder))

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            form_data: Dict[str, Any] = {}

            for inp in inputs:
                if isinstance(inp, FileInput):
                    file = request.files.get(inp.name)
                    if file and file.filename:
                        path = os.path.join(upload_folder, file.filename)
                        file.save(path)
                        form_data[inp.name] = path
                    elif inp.required:
                        flash(f"Missing required file: {inp.label}", "error")
                        return redirect(url_for("index"))
                elif isinstance(inp, CheckboxInput):
                    form_data[inp.name] = inp.name in request.form
                else:
                    value = request.form.get(inp.name, "")
                    if inp.required and not value:
                        flash(f"Missing required field: {inp.label}", "error")
                        return redirect(url_for("index"))
                    form_data[inp.name] = value

            logger.info("Processing form submission", extra={"title": title})

            try:
                if process_command is not None:
                    result = run_subprocess(process_command, form_data)
                else:
                    result = run_callable(process_handler, form_data)
            except Exception as exc:
                if error_handler:
                    result = error_handler(exc)
                else:
                    logger.error("Unhandled processing error", extra={"error": str(exc)})
                    result = {"status": "error", "output": str(exc), "data": {}}

            return render_template(
                "result.html",
                title=title,
                result=result,
                success_message=success_message,
                custom_css=custom_css,
            )

        return render_template(
            "form.html",
            title=title,
            inputs=inputs,
            enable_examples=enable_examples,
            example_files=example_files,
            custom_css=custom_css,
        )

    if enable_examples and example_folder:
        @app.route("/download-example/<filename>")
        def download_example(filename):
            if os.path.exists(os.path.join(example_folder, filename)):
                return send_from_directory(example_folder, filename, as_attachment=True)
            flash(f"Example file '{filename}' not found.", "error")
            return redirect(url_for("index"))

    return app
