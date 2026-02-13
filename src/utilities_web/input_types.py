"""Input field type definitions for utilities_web forms."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class FileInput:
    """A file upload input field.

    Args:
        name: The field name (used as form key and placeholder substitution).
        label: Display label. Defaults to name if not provided.
        required: Whether the field is required.
        accept: Comma-separated file type filter (e.g. ".csv,.json").
        max_size_mb: Maximum file size in megabytes.
    """
    name: str
    label: Optional[str] = None
    required: bool = True
    accept: Optional[str] = None
    max_size_mb: Optional[float] = None

    def __post_init__(self):
        if self.label is None:
            self.label = self.name

    @property
    def input_type(self) -> str:
        return "file"


@dataclass
class TextInput:
    """A text input field.

    Args:
        name: The field name.
        label: Display label. Defaults to name if not provided.
        required: Whether the field is required.
        default: Default value.
        placeholder: Placeholder text.
        multiline: If True, renders as a textarea.
    """
    name: str
    label: Optional[str] = None
    required: bool = False
    default: Optional[str] = None
    placeholder: Optional[str] = None
    multiline: bool = False

    def __post_init__(self):
        if self.label is None:
            self.label = self.name

    @property
    def input_type(self) -> str:
        return "text"


@dataclass
class NumberInput:
    """A numeric input field.

    Args:
        name: The field name.
        label: Display label. Defaults to name if not provided.
        required: Whether the field is required.
        default: Default value.
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.
        step: Step increment.
    """
    name: str
    label: Optional[str] = None
    required: bool = False
    default: Optional[float] = None
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    step: Optional[float] = None

    def __post_init__(self):
        if self.label is None:
            self.label = self.name

    @property
    def input_type(self) -> str:
        return "number"


@dataclass
class SelectInput:
    """A dropdown select input field.

    Args:
        name: The field name.
        choices: List of (value, label) tuples or plain strings.
        label: Display label. Defaults to name if not provided.
        required: Whether the field is required.
        default: Default selected value.
    """
    name: str
    choices: List = field(default_factory=list)
    label: Optional[str] = None
    required: bool = False
    default: Optional[str] = None

    def __post_init__(self):
        if self.label is None:
            self.label = self.name
        normalized = []
        for choice in self.choices:
            if isinstance(choice, str):
                normalized.append((choice, choice))
            else:
                normalized.append(tuple(choice))
        self.choices = normalized

    @property
    def input_type(self) -> str:
        return "select"


@dataclass
class CheckboxInput:
    """A checkbox input field.

    Args:
        name: The field name.
        label: Display label. Defaults to name if not provided.
        default: Default checked state.
    """
    name: str
    label: Optional[str] = None
    default: bool = False

    def __post_init__(self):
        if self.label is None:
            self.label = self.name

    @property
    def input_type(self) -> str:
        return "checkbox"
