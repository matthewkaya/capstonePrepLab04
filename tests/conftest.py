import pytest

from weathersummary.models import WeatherRecord


@pytest.fixture
def sample_records() -> list[WeatherRecord]:
    """Provide sample weather records for offline tests."""
    return [
        WeatherRecord("2026-10-08T10:00", 10.0, 1.0),
        WeatherRecord("2026-10-08T14:00", 20.0, 2.0),
        WeatherRecord("2026-10-09T10:00", 25.0, 0.5),
        WeatherRecord("2026-10-09T14:00", 30.0, 1.5),
    ]
