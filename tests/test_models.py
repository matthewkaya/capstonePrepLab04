import pytest

from weathersummary.models import WeatherRecord


def test_valid_weather_record():
    record = WeatherRecord("2026-10-08T12:00", 20.5, 0.2)

    assert record.time == "2026-10-08T12:00"
    assert record.temperature == 20.5
    assert record.precipitation == 0.2


def test_invalid_weather_values():
    record = WeatherRecord("2026-10-08T12:00", "invalid", "invalid")

    assert record.temperature is None
    assert record.precipitation is None


@pytest.mark.parametrize(
    "temperature, expected",
    [
        (25.0, 25.0),
        (-5.0, -5.0),
        (0.0, 0.0),
    ],
)
def test_temperature_values(temperature, expected):
    record = WeatherRecord("2026-10-08T12:00", temperature, 0.0)

    assert record.temperature == expected


def test_missing_temperature():
    record = WeatherRecord("2026-10-08T12:00", None, 0.2)

    assert record.temperature is None