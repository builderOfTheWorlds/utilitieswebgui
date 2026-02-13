"""Minimal example using a Python callable instead of a subprocess."""

from utilities_web import TextInput, NumberInput, CheckboxInput, create_app


def process_data(name: str = "", count: str = "", uppercase: bool = False, **_):
    """Simple handler that repeats a greeting."""
    count = int(count) if count else 1
    greeting = f"Hello, {name}!"
    if uppercase:
        greeting = greeting.upper()
    lines = [greeting] * count
    return {"status": "success", "output": "\n".join(lines), "data": {}}


app = create_app(
    title="Simple Greeting Processor",
    inputs=[
        TextInput("name", label="Your Name", required=True, placeholder="Enter your name"),
        NumberInput("count", label="Repeat Count", default=1, min_val=1, max_val=100, step=1),
        CheckboxInput("uppercase", label="Uppercase output"),
    ],
    process_handler=process_data,
    success_message="Done!",
)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
