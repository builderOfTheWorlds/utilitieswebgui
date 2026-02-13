# utilities-web

A reusable, pip-installable Flask framework for building web UIs around data-processing utilities. Define your inputs as dataclasses, point at a subprocess command or Python callable, and `utilities-web` generates a Bootstrap 5.3 form, handles file uploads, runs your processing logic, and displays the result -- all with a single `create_app()` call.

## Prerequisites

- Python 3.8 or later
- pip (Python package manager)

## Installation

### From source (editable / development)

```bash
git clone <repository-url>
cd utilitiesWebGui
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -e .
```

### As a dependency in another project

Add the package to your project's dependencies (path install or, eventually, from PyPI):

```
utilities-web
```

Or install directly:

```bash
pip install -e /path/to/utilitiesWebGui
```

## Usage

### Quick start

```python
from utilities_web import create_app, FileInput, TextInput

app = create_app(
    title="My Utility",
    inputs=[
        FileInput("config.json", required=True),
        TextInput("threshold", default="0.5"),
    ],
    process_command=["python", "my_script.py", "{config.json}", "{threshold}"],
)
app.run(debug=True)
```

Open `http://localhost:5000` in your browser. The framework renders a form with a file upload and a text field, substitutes the submitted values into the command placeholders, runs the subprocess, and shows the output on a result page.

### Using a Python callable instead of a subprocess

```python
from utilities_web import create_app, NumberInput, CheckboxInput

def process(value, verbose):
    result = float(value) * 2
    return {"status": "success", "output": f"Result: {result}", "data": {"result": result}}

app = create_app(
    title="Doubler",
    inputs=[
        NumberInput("value", min_val=0, max_val=100, step=1, default=10),
        CheckboxInput("verbose", default=False),
    ],
    process_handler=process,
)
app.run(debug=True)
```

The callable receives form data as keyword arguments and should return a dict with `status`, `output`, and optionally `data` keys. If a plain string or other value is returned, it is wrapped in the standard result format automatically.

### `create_app()` parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `str` | `"Utility"` | Page title shown in the browser tab and heading. |
| `inputs` | `list` | `[]` | List of input field definitions (see Input Types below). |
| `process_command` | `list[str]` | `None` | Subprocess command with `{field_name}` placeholders. |
| `process_handler` | `callable` | `None` | Python callable that receives form data as `**kwargs`. |
| `upload_folder` | `str` | `"uploaded_files"` | Directory where uploaded files are saved. |
| `example_folder` | `str` | `None` | Directory containing example files for download. |
| `enable_examples` | `bool` | `False` | Show example-file download buttons on the form. |
| `custom_css` | `str` | `None` | Extra CSS injected into the page `<style>` tag. |
| `success_message` | `str` | `"Processing complete!"` | Message shown on the result page after success. |
| `error_handler` | `callable` | `None` | Called with the exception when processing raises. |

Exactly one of `process_command` or `process_handler` must be provided.

## Input Types

All input types are dataclasses importable from `utilities_web`. Every input has a `name` (used as the form field key and placeholder token), an optional `label` (defaults to `name`), and a `required` flag.

### FileInput

File upload field.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | -- | Field name and placeholder key. |
| `label` | `str` | `name` | Display label. |
| `required` | `bool` | `True` | Whether the file is required. |
| `accept` | `str` | `None` | Allowed file types (e.g. `".csv,.json"`). |
| `max_size_mb` | `float` | `None` | Maximum file size in MB. |

### TextInput

Single-line text or multiline textarea.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | -- | Field name. |
| `label` | `str` | `name` | Display label. |
| `required` | `bool` | `False` | Whether the field is required. |
| `default` | `str` | `None` | Default value. |
| `placeholder` | `str` | `None` | Placeholder text. |
| `multiline` | `bool` | `False` | Render as a `<textarea>` instead of `<input>`. |

### NumberInput

Numeric input with optional range and step constraints.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | -- | Field name. |
| `label` | `str` | `name` | Display label. |
| `required` | `bool` | `False` | Whether the field is required. |
| `default` | `float` | `None` | Default value. |
| `min_val` | `float` | `None` | Minimum allowed value. |
| `max_val` | `float` | `None` | Maximum allowed value. |
| `step` | `float` | `None` | Step increment. |

### SelectInput

Dropdown select field.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | -- | Field name. |
| `choices` | `list` | `[]` | List of strings or `(value, label)` tuples. |
| `label` | `str` | `name` | Display label. |
| `required` | `bool` | `False` | Whether the field is required. |
| `default` | `str` | `None` | Default selected value. |

### CheckboxInput

Boolean checkbox field.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | -- | Field name. |
| `label` | `str` | `name` | Display label. |
| `default` | `bool` | `False` | Default checked state. |

## Configuration

- **Upload folder** -- Uploaded files are saved to the directory specified by `upload_folder` (default `uploaded_files/`). The directory is created automatically if it does not exist.
- **Example files** -- Set `enable_examples=True` and `example_folder="examples/"` to display download buttons for each file in that directory.
- **Debug mode** -- Pass `debug=True` to `app.run()` during development. Disable for production.
- **Custom styling** -- Inject additional CSS via the `custom_css` parameter. The base UI uses Bootstrap 5.3 loaded from CDN.

## Project Structure

```
utilitiesWebGui/
├── pyproject.toml                # Package metadata and dependencies
├── README.md                     # This file
├── CLAUDE.md                     # AI assistant project guidelines
├── src/
│   └── utilities_web/
│       ├── __init__.py           # Public API (create_app, input types)
│       ├── app_factory.py        # Flask application factory
│       ├── input_types.py        # Input field dataclasses
│       ├── processor.py          # Subprocess and callable execution
│       └── templates/
│           ├── base.html         # Base layout (Bootstrap 5.3 CDN)
│           ├── form.html         # Form rendering template
│           └── result.html       # Result display template
├── examples/
│   ├── profile_migration/        # Example: Advanced Profile Migration utility
│   └── simple_processor/         # Example: minimal usage demo
└── tests/                        # pytest test suite
```

## Testing

Install development dependencies and run the test suite:

```bash
pip install -e ".[dev]"
pytest
```

To run with coverage reporting:

```bash
pytest --cov=utilities_web --cov-report=term-missing
```

## License

MIT
