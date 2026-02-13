# Handoff Prompt

Copy everything below the line into a fresh Claude Code conversation to begin implementation:

---

**Project: Restructure utilitiesWebGui into a pip-installable Python package**

I need to restructure the `utilitiesWebGui` project (at `c:\Users\Administrator\PycharmProjects\utilitiesWebGui`) from a monolithic Flask app into a pip-installable Python package called `utilities_web`.

**What exists now:** A Flask app with inline HTML templates (`utility-a.py`, `app.py`, `process_files.py`) that provides a web form for file uploads and runs scripts via subprocess. These files should be removed after the restructure.

**What I want:** A reusable package with a `create_app()` factory function. Consumer projects install this package via pip and create a web UI for their scripts in ~10 lines of code:

```python
from utilities_web import create_app, FileInput, TextInput

app = create_app(
    title="My Utility",
    inputs=[
        FileInput("config.json", required=True),
        TextInput("threshold", default="0.5"),
    ],
    process_command=["python", "my_script.py", "{config.json}", "{threshold}"]
)
app.run(debug=True)
```

**Target structure:**
```
utilitiesWebGui/
├── pyproject.toml                    # pip-installable package config
├── src/utilities_web/
│   ├── __init__.py                   # Exports create_app + input types
│   ├── app_factory.py               # create_app() — creates Flask app with routes
│   ├── input_types.py               # Dataclasses: FileInput, TextInput, NumberInput, SelectInput, CheckboxInput
│   ├── processor.py                 # Runs subprocess commands or Python callables
│   └── templates/                   # Jinja2: base.html, form.html, result.html (Bootstrap 5.3)
├── examples/
│   ├── profile_migration/main.py    # Current utility-a converted to new framework
│   └── simple_processor/main.py     # Minimal callable example
└── tests/
    ├── test_app_factory.py
    ├── test_input_types.py
    └── test_processor.py
```

**Key requirements:**
1. `create_app()` accepts: `title`, `inputs` (list of InputField types), `process_command` (subprocess with `{field_name}` placeholders) OR `process_handler` (Python callable), `upload_folder`, `example_folder`, `enable_examples`, `custom_css`, `success_message`, `error_handler`
2. Input types are dataclasses: `FileInput` (accept, max_size_mb), `TextInput` (default, placeholder, multiline), `NumberInput` (min/max/step), `SelectInput` (choices), `CheckboxInput`
3. Templates use Bootstrap 5.3 CDN, include progress indicator, flash messages, example download buttons
4. `processor.py` handles both subprocess execution (with placeholder substitution and stdout/stderr capture) and Python callable execution, returns standardized `{"status": "success"|"error", "output": ..., "data": ...}` dicts
5. `pyproject.toml` uses setuptools, includes `flask>=2.3.0` dependency, package-data for templates
6. Remove old files (`utility-a.py`, `app.py`, `process_files.py`) after creating the new structure
7. Move existing example files from `examples/` to `examples/profile_migration/example_files/`
8. Write tests and update README.md

**Please read the project's README.md and CLAUDE.md first, then implement this step by step. Use sub-agents for parallel work where possible.**
