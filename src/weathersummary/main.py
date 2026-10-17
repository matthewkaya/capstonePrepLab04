import argparse
import logging
import sys
from pathlib import Path

from .config import load_settings
from .exceptions import WeatherSummaryError
from .logging_setup import setup_logging
from .report import build_summary, write_summary
from .run_info import write_run_info
from .sources import WeatherSource

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """Run the weather summary application."""

    parser = argparse.ArgumentParser(description="Generate a weather summary report.")

    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/weathersummary.toml"),
        help="Path to the TOML configuration file.",
    )

    args = parser.parse_args(argv)

    try:
        settings = load_settings(args.config)
        setup_logging(settings.log_level)

        logger.info("Starting weather summary application")

        source = WeatherSource(
            url=settings.source_url,
            timeout=settings.timeout,
        )

        records = source.fetch_records()

        summary = build_summary(
            records=records,
            source_url=settings.source_url,
        )

        output_path = settings.output_directory / "summary.json"
        write_summary(summary, output_path)

        run_info_path = settings.output_directory / "run_info.json"
        write_run_info(settings, run_info_path)

        logger.info("Weather summary completed successfully")

        print(f"Summary saved to {output_path}")
        print(f"Run information saved to {run_info_path}")

        return 0

    except (WeatherSummaryError, OSError) as error:
        logger.error("Application failed: %s", error)
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
