import json
from pathlib import Path

from weathersummary.config import Settings
from weathersummary.run_info import (
    build_run_info,
    get_package_version,
    write_run_info,
)


def test_build_run_info():
    settings = Settings(
        source_url="https://example.com/weather",
        timeout=10,
        output_directory=Path("data/processed"),
        seed=42,
        sample_size=100,
        log_level="INFO",
    )

    result = build_run_info(settings)

    assert result["settings"]["source_url"] == "https://example.com/weather"
    assert result["settings"]["timeout"] == 10
    assert result["settings"]["output_directory"] == "data/processed"
    assert result["python_version"]
    assert "pytest" in result["tool_versions"]
    assert "mypy" in result["tool_versions"]
    assert "ruff" in result["tool_versions"]


def test_write_run_info(tmp_path):
    settings = Settings(
        source_url="https://example.com/weather",
        timeout=10,
        output_directory=tmp_path,
        seed=42,
        sample_size=100,
        log_level="INFO",
    )

    output_path = tmp_path / "reports" / "run_info.json"

    write_run_info(settings, output_path)

    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert data["settings"]["seed"] == 42
    assert data["settings"]["sample_size"] == 100


def test_missing_package_version():
    result = get_package_version("nonexistent-package-for-weather-tests-xyz")

    assert result == "not installed"
