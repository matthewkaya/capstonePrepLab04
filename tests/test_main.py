from pathlib import Path

import pytest

from weathersummary.exceptions import WeatherSourceError
from weathersummary.main import main
from weathersummary.models import WeatherRecord


@pytest.fixture
def cli_config(tmp_path: Path) -> Path:
    """Create a temporary configuration for CLI tests."""

    config_path = tmp_path / "weathersummary.toml"
    output_directory = tmp_path / "output"

    config_path.write_text(
        f"""
[weather]
source_url = "https://example.com/weather"
timeout = 10

[output]
directory = "{output_directory}"

[processing]
seed = 42
sample_size = 100

[logging]
level = "INFO"
""",
        encoding="utf-8",
    )

    return config_path


def test_main_success(cli_config, monkeypatch, capsys):
    """Successful execution should create a report and return zero."""

    records = [
        WeatherRecord("2026-10-08T10:00", 15.0, 1.0),
        WeatherRecord("2026-10-08T14:00", 20.0, 2.0),
    ]

    def fake_fetch_records(self):
        return records

    monkeypatch.setattr(
        "weathersummary.main.WeatherSource.fetch_records",
        fake_fetch_records,
    )

    result = main(["--config", str(cli_config)])

    captured = capsys.readouterr()

    assert result == 0
    assert "Summary saved to" in captured.out

    output_path = cli_config.parent / "output" / "summary.json"
    assert output_path.exists()


def test_main_source_failure(cli_config, monkeypatch, capsys):
    """API failures should return one and print an error."""

    def fake_fetch_records(self):
        raise WeatherSourceError("API unavailable")

    monkeypatch.setattr(
        "weathersummary.main.WeatherSource.fetch_records",
        fake_fetch_records,
    )

    result = main(["--config", str(cli_config)])

    captured = capsys.readouterr()

    assert result == 1
    assert "Error: API unavailable" in captured.err


def test_main_missing_config(tmp_path, capsys):
    """Missing configuration should return one."""

    missing_config = tmp_path / "missing.toml"

    result = main(["--config", str(missing_config)])

    captured = capsys.readouterr()

    assert result == 1
    assert "Error:" in captured.err
