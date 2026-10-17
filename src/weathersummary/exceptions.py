class WeatherSummaryError(Exception):
    """Base exception for the weather summary application."""


class WeatherSourceError(WeatherSummaryError):
    """Raised when weather data cannot be retrieved."""


class WeatherDataError(WeatherSummaryError):
    """Raised when weather data is invalid or incomplete."""


class WeatherConfigError(WeatherSummaryError):
    """Raised when application configuration is invalid."""