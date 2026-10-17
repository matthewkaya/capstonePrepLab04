import tomllib
from dataclasses import dataclass
from pathlib import Path

from .exceptions import WeatherConfigError


@dataclass(frozen=True)
class Settings:
    """Application configuration settings."""

    source_url: str
    timeout: int
    output_directory: Path
    seed: int
    sample_size: int
    log_level: str


def load_settings(config_path: Path) -> Settings:
    """Load and validate application settings from TOML."""

    try:
        with config_path.open("rb") as file:
            config = tomllib.load(file)

    except (OSError, tomllib.TOMLDecodeError) as error:
        raise WeatherConfigError(
            f"Unable to load configuration: {config_path}"
        ) from error

    try:
        weather = config["weather"]
        output = config["output"]
        processing = config["processing"]
        logging_config = config["logging"]

        settings = Settings(
            source_url=weather["source_url"],
            timeout=weather["timeout"],
            output_directory=Path(output["directory"]),
            seed=processing["seed"],
            sample_size=processing["sample_size"],
            log_level=logging_config["level"],
        )

    except (KeyError, TypeError, ValueError) as error:
        raise WeatherConfigError(
            "Configuration contains missing or invalid settings."
        ) from error

    if not isinstance(settings.source_url, str) or not settings.source_url:
        raise WeatherConfigError("source_url must be a non-empty string.")

    if type(settings.timeout) is not int or settings.timeout <= 0:
        raise WeatherConfigError("timeout must be a positive integer.")

    if type(settings.seed) is not int:
        raise WeatherConfigError("seed must be an integer.")

    if type(settings.sample_size) is not int or settings.sample_size <= 0:
        raise WeatherConfigError("sample_size must be a positive integer.")

    if not isinstance(settings.log_level, str) or settings.log_level.upper() not in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }:
        raise WeatherConfigError("Invalid logging level.")

    return settings
