"""Process execution module — runs subprocess commands or Python callables."""

import logging
import subprocess
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


def run_subprocess(
    command: List[str],
    form_data: Dict[str, Any],
    timeout: Optional[int] = None,
) -> Dict[str, Any]:
    """Execute a subprocess command with placeholder substitution.

    Placeholders in the command list (e.g. ``{field_name}``) are replaced
    with corresponding values from *form_data*.  File fields are replaced
    with the saved file path.

    Args:
        command: Command list with ``{field_name}`` placeholders.
        form_data: Mapping of field names to submitted values / file paths.
        timeout: Optional timeout in seconds.

    Returns:
        Standardized result dict with keys ``status``, ``output``, and ``data``.
    """
    resolved = []
    for part in command:
        for key, value in form_data.items():
            part = part.replace(f"{{{key}}}", str(value))
        resolved.append(part)

    logger.debug("Running subprocess", extra={"command": resolved})

    try:
        result = subprocess.run(
            resolved,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode == 0:
            logger.info("Subprocess completed successfully")
            return {
                "status": "success",
                "output": result.stdout,
                "data": {"returncode": result.returncode, "stderr": result.stderr},
            }
        else:
            logger.error(
                "Subprocess failed",
                extra={"returncode": result.returncode, "stderr": result.stderr},
            )
            return {
                "status": "error",
                "output": result.stderr or result.stdout,
                "data": {"returncode": result.returncode},
            }
    except subprocess.TimeoutExpired:
        logger.error("Subprocess timed out", extra={"timeout": timeout})
        return {
            "status": "error",
            "output": f"Process timed out after {timeout} seconds",
            "data": {},
        }
    except FileNotFoundError as exc:
        logger.error("Subprocess executable not found", extra={"error": str(exc)})
        return {
            "status": "error",
            "output": f"Command not found: {resolved[0]}",
            "data": {},
        }


def run_callable(
    handler: Callable[..., Any],
    form_data: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute a Python callable with submitted form data.

    The callable receives *form_data* as keyword arguments and should return
    a dict.  If it returns a plain string, it is wrapped in the standard
    result format.

    Args:
        handler: A callable that accepts ``**form_data``.
        form_data: Mapping of field names to submitted values / file paths.

    Returns:
        Standardized result dict with keys ``status``, ``output``, and ``data``.
    """
    logger.debug("Running callable", extra={"handler": getattr(handler, "__name__", repr(handler))})

    try:
        result = handler(**form_data)

        if isinstance(result, dict) and "status" in result:
            return result

        return {
            "status": "success",
            "output": str(result) if result is not None else "Processing complete.",
            "data": result if isinstance(result, dict) else {},
        }
    except Exception as exc:
        logger.error("Callable raised exception", extra={"error": str(exc)})
        return {
            "status": "error",
            "output": str(exc),
            "data": {},
        }
