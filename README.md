# AIGC5005 Lab 04 — Weather Summary

This project builds on my Lab 03 weather summary application.

For Lab 04, I improved the existing Python package by adding
configuration management, logging, custom exceptions, type annotations,
automated testing, and reproducible run information.

The application downloads hourly weather data from the Open-Meteo API
and generates a JSON summary of daily temperatures, precipitation,
and the warmest day.

## Data Source

Weather data comes from the Open-Meteo API.

The default configuration uses Toronto weather data, including
the past seven days and the current forecast period.

The API URL can be changed in `config/weathersummary.toml`.

## Setup

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate weathersummary
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the package in editable mode:

```bash
python -m pip install -e .
```

The project uses Python 3.11.

## Run

Run the application using the package CLI:

```bash
python -m weathersummary.main --config config/weathersummary.toml
```

The application creates two files:

- `data/processed/summary.json`
- `data/processed/run_info.json`

The first file contains the weather analysis results.

The second file records the application settings, Python version,
and installed versions of pytest, mypy, and Ruff.

## Check it

Run the automated tests:

```bash
python -m pytest
```

Check formatting:

```bash
python -m ruff format --check .
```

Check code quality:

```bash
python -m ruff check .
```

Check type annotations:

```bash
python -m mypy
```

The Ruff configuration enables the E, F, I, B, and UP rule groups.

All automated tests use local sample data or mocked API responses.
They do not require an internet connection.

## Settings

Application settings are stored in:

`config/weathersummary.toml`

The configuration includes:

| Setting | Purpose |
|---|---|
| `weather.source_url` | Weather API endpoint |
| `weather.timeout` | Request timeout in seconds |
| `output.directory` | Directory for generated JSON files |
| `processing.seed` | Reserved for reproducible sampling |
| `processing.sample_size` | Reserved for future sampling |
| `logging.level` | Application logging level |

The application loads these settings into an immutable
`Settings` dataclass.

The seed and sample size settings are recorded for reproducibility
but are not currently used to limit or sample weather records.

## Errors and exit codes

The application uses custom exception classes:

- `WeatherSummaryError` — Base application exception
- `WeatherSourceError` — Weather API or network errors
- `WeatherDataError` — Invalid or incomplete weather data
- `WeatherConfigError` — Configuration errors

The CLI returns:

| Exit code | Meaning |
|---|---|
| `0` | Application completed successfully |
| `1` | Application failed |

Application errors are displayed on stderr with an `Error:` prefix.

The application uses Python logging instead of print statements
for internal processing messages.

## Reproducing a run

To reproduce the application environment:

1. Clone the repository.
2. Create the Conda environment using `environment.yml`.
3. Install dependencies using `requirements.txt`.
4. Install the package with `pip install -e .`.
5. Run the application with the supplied TOML configuration.
6. Review `summary.json` and `run_info.json`.

The `run_info.json` file records the settings and tool versions
used during execution.

Because the Open-Meteo API provides changing weather data,
running the application on different dates may produce different
summary values.

## What the tests cover

The project uses pytest for automated testing.

The tests cover:

- Weather record creation and invalid numeric values
- Daily temperature calculations
- Daily precipitation calculations
- Warmest-day identification
- Missing temperature and precipitation values
- Empty datasets and aggregation errors
- Successful and failed API requests
- Invalid or incomplete API responses
- Valid and invalid TOML configuration
- Immutable configuration settings
- Successful CLI execution
- CLI failures and exit codes
- Run metadata generation and JSON output

Shared test fixtures are stored in `tests/conftest.py`.

Tests use pytest fixtures, parametrization, monkeypatching,
temporary directories, and exception assertions.

## Project Layout

```text
config/
    weathersummary.toml

data/
    raw/
    processed/
        summary.json
        run_info.json

src/weathersummary/
    __init__.py
    py.typed
    aggregations.py
    config.py
    exceptions.py
    logging_setup.py
    main.py
    models.py
    report.py
    run_info.py
    sources.py

tests/
    conftest.py
    test_aggregations.py
    test_config.py
    test_main.py
    test_models.py
    test_run_info.py
    test_sources.py

environment.yml
requirements.txt
pyproject.toml
README.md
```

## Design Choices

I kept the object-oriented structure developed in Lab 03.

`WeatherRecord` represents an hourly weather observation.

`WeatherSource` retrieves API data and creates weather records.

The aggregation classes calculate temperature statistics,
precipitation totals, and the warmest day.

`report.py` builds and writes the weather summary.

For Lab 04, I separated configuration loading, logging setup,
exception handling, and run metadata into dedicated modules.

This makes the application easier to test and maintain.

## Known Limitations

- An internet connection is required for live weather downloads.
- The default configuration uses Toronto weather data.
- The API data changes over time, so output values may differ between runs.
- Sampling settings are reserved for future development.
- The application generates JSON reports only.
- The application does not currently provide a graphical interface.