from pathlib import Path

import pytest

from weathersummary.config import load_settings
from weathersummary.exceptions import WeatherConfigError


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """Create a valid temporary TOML configuration."""

    path = tmp_path / "weathersummary.toml"

    path.write_text(
        """
[weather]
source_url = "https://example.com/weather"
timeout = 10

[output]
directory = "data/processed"

[processing]
seed = 42
sample_size = 100

[logging]
level = "INFO"
""",
        encoding="utf-8",
    )

    return path


def test_load_valid_settings(config_file: Path) -> None:
    settings = load_settings(config_file)

    assert settings.source_url == "https://example.com/weather"
    assert settings.timeout == 10
    assert settings.output_directory == Path("data/processed")
    assert settings.seed == 42
    assert settings.sample_size == 100
    assert settings.log_level == "INFO"


def test_settings_are_immutable(config_file: Path) -> None:
    from dataclasses import FrozenInstanceError

    settings = load_settings(config_file)

    with pytest.raises(FrozenInstanceError):
        settings.timeout = 20


def test_missing_config_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.toml"

    with pytest.raises(
        WeatherConfigError,
        match="Unable to load configuration",
    ):
        load_settings(path)


def test_invalid_toml(tmp_path: Path) -> None:
    path = tmp_path / "invalid.toml"
    path.write_text("[weather\n", encoding="utf-8")

    with pytest.raises(
        WeatherConfigError,
        match="Unable to load configuration",
    ):
        load_settings(path)


@pytest.mark.parametrize(
    ("setting", "value", "message"),
    [
        ("timeout", "0", "timeout must be a positive integer"),
        ("timeout", "-5", "timeout must be a positive integer"),
        ("timeout", '"invalid"', "timeout must be a positive integer"),
    ],
)
def test_invalid_timeout(
    config_file: Path,
    setting: str,
    value: str,
    message: str,
) -> None:
    content = config_file.read_text(encoding="utf-8")
    content = content.replace(f"{setting} = 10", f"{setting} = {value}")
    config_file.write_text(content, encoding="utf-8")

    with pytest.raises(WeatherConfigError, match=message):
        load_settings(config_file)


def test_missing_required_section(config_file: Path) -> None:
    content = config_file.read_text(encoding="utf-8")
    content = content.replace("[processing]", "[missing_processing]")
    config_file.write_text(content, encoding="utf-8")

    with pytest.raises(
        WeatherConfigError,
        match="Configuration contains missing or invalid settings",
    ):
        load_settings(config_file)
