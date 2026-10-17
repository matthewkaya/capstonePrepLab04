import logging

import requests

from .exceptions import WeatherDataError, WeatherSourceError
from .models import WeatherRecord

logger = logging.getLogger(__name__)


class WeatherSource:
    """Downloads weather data and creates weather records."""

    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout

    def fetch_records(self):
        logger.info("Fetching weather data from API")

        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

        except requests.RequestException as error:
            logger.error("Unable to download weather data: %s", error)
            raise WeatherSourceError("Unable to download weather data.") from error

        except ValueError as error:
            logger.error("Weather API returned invalid JSON: %s", error)
            raise WeatherDataError("Weather API returned invalid JSON.") from error

        try:
            times = data["hourly"]["time"]
            temperatures = data["hourly"]["temperature_2m"]
            precipitation = data["hourly"]["precipitation"]

        except (KeyError, TypeError) as error:
            logger.error("Weather data is missing required hourly fields")
            raise WeatherDataError(
                "Weather data is missing required hourly fields."
            ) from error

        if not all(
            isinstance(values, list) for values in (times, temperatures, precipitation)
        ):
            logger.error("Weather hourly fields must be lists")
            raise WeatherDataError("Weather hourly fields must be lists.")

        if len(times) != len(temperatures) or len(times) != len(precipitation):
            logger.error("Weather data lists have different lengths")
            raise WeatherDataError("Weather data lists have different lengths.")

        records = []

        for time, temperature, rain in zip(times, temperatures, precipitation):
            if not isinstance(time, str):
                logger.warning("Skipping record with invalid timestamp")
                continue

            record = WeatherRecord(time, temperature, rain)
            records.append(record)

        logger.info("Successfully loaded %d weather records", len(records))

        return records
