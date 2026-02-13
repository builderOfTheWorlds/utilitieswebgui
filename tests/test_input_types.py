"""Tests for utilities_web input type dataclasses."""

import pytest

from utilities_web import FileInput, TextInput, NumberInput, SelectInput, CheckboxInput


# ---------------------------------------------------------------------------
# FileInput
# ---------------------------------------------------------------------------

class TestFileInput:
    def test_default_label_from_name(self):
        inp = FileInput(name="config_file")
        assert inp.label == "config_file"

    def test_custom_label(self):
        inp = FileInput(name="config_file", label="Configuration File")
        assert inp.label == "Configuration File"

    def test_input_type(self):
        inp = FileInput(name="f")
        assert inp.input_type == "file"

    def test_required_defaults_to_true(self):
        inp = FileInput(name="f")
        assert inp.required is True

    def test_required_can_be_false(self):
        inp = FileInput(name="f", required=False)
        assert inp.required is False

    def test_accept_and_max_size(self):
        inp = FileInput(name="f", accept=".csv,.json", max_size_mb=10.0)
        assert inp.accept == ".csv,.json"
        assert inp.max_size_mb == 10.0


# ---------------------------------------------------------------------------
# TextInput
# ---------------------------------------------------------------------------

class TestTextInput:
    def test_default_label_from_name(self):
        inp = TextInput(name="username")
        assert inp.label == "username"

    def test_custom_label(self):
        inp = TextInput(name="username", label="User Name")
        assert inp.label == "User Name"

    def test_input_type(self):
        inp = TextInput(name="t")
        assert inp.input_type == "text"

    def test_required_defaults_to_false(self):
        inp = TextInput(name="t")
        assert inp.required is False

    def test_default_value(self):
        inp = TextInput(name="t", default="hello")
        assert inp.default == "hello"


# ---------------------------------------------------------------------------
# NumberInput
# ---------------------------------------------------------------------------

class TestNumberInput:
    def test_default_label_from_name(self):
        inp = NumberInput(name="count")
        assert inp.label == "count"

    def test_custom_label(self):
        inp = NumberInput(name="count", label="Item Count")
        assert inp.label == "Item Count"

    def test_input_type(self):
        inp = NumberInput(name="n")
        assert inp.input_type == "number"

    def test_required_defaults_to_false(self):
        inp = NumberInput(name="n")
        assert inp.required is False

    def test_default_and_bounds(self):
        inp = NumberInput(name="n", default=5.0, min_val=0.0, max_val=100.0, step=1.0)
        assert inp.default == 5.0
        assert inp.min_val == 0.0
        assert inp.max_val == 100.0
        assert inp.step == 1.0


# ---------------------------------------------------------------------------
# SelectInput
# ---------------------------------------------------------------------------

class TestSelectInput:
    def test_default_label_from_name(self):
        inp = SelectInput(name="mode")
        assert inp.label == "mode"

    def test_custom_label(self):
        inp = SelectInput(name="mode", label="Processing Mode")
        assert inp.label == "Processing Mode"

    def test_input_type(self):
        inp = SelectInput(name="s")
        assert inp.input_type == "select"

    def test_string_choices_normalized_to_tuples(self):
        inp = SelectInput(name="color", choices=["red", "green", "blue"])
        assert inp.choices == [("red", "red"), ("green", "green"), ("blue", "blue")]

    def test_tuple_choices_preserved(self):
        inp = SelectInput(name="color", choices=[("r", "Red"), ("g", "Green")])
        assert inp.choices == [("r", "Red"), ("g", "Green")]

    def test_mixed_choices(self):
        inp = SelectInput(name="color", choices=["plain", ("v", "Value")])
        assert inp.choices == [("plain", "plain"), ("v", "Value")]

    def test_required_defaults_to_false(self):
        inp = SelectInput(name="s")
        assert inp.required is False

    def test_default_value(self):
        inp = SelectInput(name="s", choices=["a", "b"], default="b")
        assert inp.default == "b"


# ---------------------------------------------------------------------------
# CheckboxInput
# ---------------------------------------------------------------------------

class TestCheckboxInput:
    def test_default_label_from_name(self):
        inp = CheckboxInput(name="agree")
        assert inp.label == "agree"

    def test_custom_label(self):
        inp = CheckboxInput(name="agree", label="I Agree")
        assert inp.label == "I Agree"

    def test_input_type(self):
        inp = CheckboxInput(name="c")
        assert inp.input_type == "checkbox"

    def test_default_is_false(self):
        inp = CheckboxInput(name="c")
        assert inp.default is False

    def test_default_true(self):
        inp = CheckboxInput(name="c", default=True)
        assert inp.default is True
