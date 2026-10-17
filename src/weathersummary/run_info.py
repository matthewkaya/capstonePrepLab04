import json
import logging
import platform
from dataclasses import asdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from .config import Settings

logger = logging.getLogger(__name__)


def get_package_version(package: str) -> str:
    """Return an installed package version."""

    try:
        return version(package)
    except PackageNotFoundError:
        return "not installed"


def build_run_info(settings: Settings) -> dict[str, Any]:
    """Collect configuration and environment information."""

    configuration = asdict(settings)
    configuration["output_directory"] = str(settings.output_directory)

    return {
        "settings": configuration,
        "python_version": platform.python_version(),
        "tool_versions": {
            "pytest": get_package_version("pytest"),
            "mypy": get_package_version("mypy"),
            "ruff": get_package_version("ruff"),
        },
    }


def write_run_info(settings: Settings, path: Path) -> None:
    """Write reproducibility information to a JSON file."""

    logger.info("Writing run information to %s", path)

    run_info = build_run_info(settings)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(run_info, file, indent=2)

    logger.info("Run information saved successfully")
