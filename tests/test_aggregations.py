import pytest

from weathersummary.aggregations import (
    Aggregation,
    PrecipitationAggregation,
    TemperatureAggregation,
    WarmestDayAggregation,
)
from weathersummary.models import WeatherRecord


@pytest.fixture
def sample_records():
    return [
        WeatherRecord("2026-10-08T10:00", 10.0, 1.0),
        WeatherRecord("2026-10-08T14:00", 20.0, 2.0),
        WeatherRecord("2026-10-09T10:00", 25.0, 0.5),
        WeatherRecord("2026-10-09T14:00", 30.0, 1.5),
    ]


def test_temperature_aggregation(sample_records):
    result = TemperatureAggregation().compute(sample_records)

    assert result["2026-10-08"]["min_temperature"] == 10.0
    assert result["2026-10-08"]["max_temperature"] == 20.0
    assert result["2026-10-08"]["mean_temperature"] == 15.0


def test_temperature_multiple_days(sample_records):
    result = TemperatureAggregation().compute(sample_records)

    assert len(result) == 2
    assert result["2026-10-09"]["mean_temperature"] == 27.5


def test_precipitation_aggregation(sample_records):
    result = PrecipitationAggregation().compute(sample_records)

    assert result["2026-10-08"] == 3.0
    assert result["2026-10-09"] == 2.0


def test_warmest_day(sample_records):
    result = WarmestDayAggregation().compute(sample_records)

    assert result == {"date": "2026-10-09", "temperature": 30.0}


def test_missing_temperature():
    records = [
        WeatherRecord("2026-10-08T10:00", None, 1.0),
        WeatherRecord("2026-10-08T14:00", 20.0, 2.0),
    ]

    result = TemperatureAggregation().compute(records)

    assert result["2026-10-08"]["mean_temperature"] == 20.0


def test_missing_precipitation():
    records = [
        WeatherRecord("2026-10-08T10:00", 10.0, None),
        WeatherRecord("2026-10-08T14:00", 20.0, 2.0),
    ]

    result = PrecipitationAggregation().compute(records)

    assert result["2026-10-08"] == 2.0


def test_empty_temperature_records():
    result = TemperatureAggregation().compute([])

    assert result == {}


def test_base_aggregation_not_implemented():
    with pytest.raises(NotImplementedError):
        Aggregation().compute([])