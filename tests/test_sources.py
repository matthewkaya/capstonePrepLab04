import pytest
import requests

from weathersummary.exceptions import WeatherDataError, WeatherSourceError
from weathersummary.sources import WeatherSource


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self.data


def test_successful_weather_response(monkeypatch):
    data = {
        "hourly": {
            "time": ["2026-10-08T10:00"],
            "temperature_2m": [20.5],
            "precipitation": [0.2],
        }
    }

    monkeypatch.setattr(
        requests,
        "get",
        lambda url, timeout: FakeResponse(data),
    )

    records = WeatherSource("https://example.com").fetch_records()

    assert len(records) == 1
    assert records[0].temperature == 20.5


def test_connection_error(monkeypatch):
    def fake_get(url, timeout):
        raise requests.ConnectionError("Connection failed")

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(WeatherSourceError, match="Unable to download"):
        WeatherSource("https://example.com").fetch_records()


def test_missing_hourly_fields(monkeypatch):
    monkeypatch.setattr(
        requests,
        "get",
        lambda url, timeout: FakeResponse({"hourly": {}}),
    )

    with pytest.raises(WeatherDataError, match="missing required hourly"):
        WeatherSource("https://example.com").fetch_records()


def test_different_list_lengths(monkeypatch):
    data = {
        "hourly": {
            "time": ["2026-10-08T10:00"],
            "temperature_2m": [20.5, 21.0],
            "precipitation": [0.2],
        }
    }

    monkeypatch.setattr(
        requests,
        "get",
        lambda url, timeout: FakeResponse(data),
    )

    with pytest.raises(WeatherDataError, match="different lengths"):
        WeatherSource("https://example.com").fetch_records()
