import logging
from collections.abc import Sequence
from typing import Any

from .exceptions import WeatherDataError
from .models import WeatherRecord

logger = logging.getLogger(__name__)


class Aggregation:
    """Base class for weather aggregations."""

    def compute(self, records: Sequence[WeatherRecord]) -> Any:
        raise NotImplementedError


class TemperatureAggregation(Aggregation):
    """Calculates daily temperature statistics."""

    def compute(self, records: Sequence[WeatherRecord]) -> dict[str, dict[str, float]]:
        daily_temperatures: dict[str, list[float]] = {}

        for record in records:
            date = record.time.split("T")[0]
            temperature = record.temperature

            if temperature is None:
                logger.debug("Skipping missing temperature for %s", date)
                continue

            daily_temperatures.setdefault(date, []).append(temperature)

        summary = {}

        for date, temperatures in daily_temperatures.items():
            summary[date] = {
                "min_temperature": min(temperatures),
                "max_temperature": max(temperatures),
                "mean_temperature": round(sum(temperatures) / len(temperatures), 2),
            }

        logger.info("Calculated temperature statistics for %d days", len(summary))
        return summary


class PrecipitationAggregation(Aggregation):
    """Calculates total precipitation for each day."""

    def compute(self, records: Sequence[WeatherRecord]) -> dict[str, float]:
        daily_precipitation: dict[str, float] = {}

        for record in records:
            date = record.time.split("T")[0]
            precipitation = record.precipitation

            if precipitation is None:
                logger.debug("Skipping missing precipitation for %s", date)
                continue

            daily_precipitation[date] = (
                daily_precipitation.get(date, 0.0) + precipitation
            )

        logger.info(
            "Calculated precipitation totals for %d days",
            len(daily_precipitation),
        )
        return daily_precipitation


class WarmestDayAggregation(Aggregation):
    """Finds the day with the highest maximum temperature."""

    def compute(self, records: Sequence[WeatherRecord]) -> dict[str, Any]:
        daily_max_temperatures: dict[str, float] = {}

        for record in records:
            date = record.time.split("T")[0]
            temperature = record.temperature

            if temperature is None:
                continue

            if (
                date not in daily_max_temperatures
                or temperature > daily_max_temperatures[date]
            ):
                daily_max_temperatures[date] = temperature

        if not daily_max_temperatures:
            logger.error("No valid temperature records available")
            raise WeatherDataError("No valid temperature records available.")

        warmest_day = max(
            daily_max_temperatures,
            key=lambda date: daily_max_temperatures[date],
        )

        logger.info("Warmest day identified: %s", warmest_day)

        return {
            "date": warmest_day,
            "temperature": daily_max_temperatures[warmest_day],
        }
