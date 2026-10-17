# AIGC5005 Lab 04 — Harden Your Package

## Project Overview

This project is an improved version of my Lab 03 Weather Summary application.

In Lab 03, I converted my original weather analysis program into an
object-oriented Python package. For Lab 04, I focused on improving the
reliability, maintainability, testability, and reproducibility of that package.

The application retrieves hourly weather data from the Open-Meteo API
and generates a JSON report containing daily weather statistics.

The main improvements introduced in Lab 04 include:

- TOML-based configuration management
- Custom exception handling
- Structured application logging
- Command-line interface (CLI)
- Offline automated testing with pytest
- Python type annotations and Mypy validation
- Ruff formatting and linting
- Reproducible dependency management
- Execution metadata stored in run_info.json
- Improved project documentation

The project follows a modular design in which each component has
a clearly defined responsibility.

---

## Data Source

The application uses the Open-Meteo API to retrieve weather data
for Toronto, Ontario, Canada.

Default location:

- City: Toronto
- Latitude: 43.65
- Longitude: -79.38

The default API request includes:

- Seven days of historical weather data
- One day of forecast data
- Hourly temperature measurements
- Hourly precipitation measurements

### What One Record Represents

Each WeatherRecord object represents one hourly weather observation.

A record contains three main attributes:

| Attribute | Description | Example |
|---|---|---|
| time | Date and time of the observation | 2026-10-08T10:00 |
| temperature | Temperature in degrees Celsius | 15.4 |
| precipitation | Precipitation in millimetres | 0.5 |

Temperature and precipitation values may be missing.
The application handles missing numeric values during processing.

### Expected Number of Records

The default configuration requests eight days of hourly weather data.

Therefore, the expected number of records is approximately:

8 days × 24 hours = 192 hourly records

The actual number may vary depending on the API response.

### Weather Calculations

The application processes the hourly observations to calculate:

1. Daily minimum temperature
2. Daily maximum temperature
3. Daily average temperature
4. Daily total precipitation
5. The warmest day in the dataset

The results are written to:

data/processed/summary.json

---

## Setup

The project uses Python 3.11 and Conda for environment management.

### 1. Clone the Repository

```bash
git clone https://github.com/matthewkaya/capstonePrepLab04.git
cd capstonePrepLab04
```

### 2. Create the Conda Environment

```bash
conda env create -f environment.yml
```

### 3. Activate the Environment

```bash
conda activate weathersummary
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install the Package

```bash
python -m pip install -e .
```

The editable installation allows the package to be imported
directly from the source directory during development.

---

## Run

The application is executed through its Python package entry point.

```bash
python -m weathersummary.main --config config/weathersummary.toml
```

The command performs the following operations:

1. Reads the TOML configuration file.
2. Validates the application settings.
3. Configures application logging.
4. Requests weather data from Open-Meteo.
5. Converts the API response into WeatherRecord objects.
6. Calculates daily weather statistics.
7. Generates the weather summary.
8. Writes execution metadata.
9. Saves the JSON output files.

### Generated Files

The application generates two output files.

**1. summary.json**

Location:

```text
data/processed/summary.json
```

Contains the calculated weather statistics.

**2. run_info.json**

Location:

```text
data/processed/run_info.json
```

Contains information about the environment and settings
used during the execution.

---

## Check It

The project uses automated quality checks to verify
correctness, formatting, and type safety.

### Run Automated Tests

```bash
python -m pytest
```

Final verification result:

```text
33 passed
```

### Check Code Formatting

```bash
python -m ruff format --check .
```

Final verification result:

```text
20 files already formatted
```

### Check Code Quality

```bash
python -m ruff check .
```

Final verification result:

```text
All checks passed!
```

### Check Type Annotations

```bash
python -m mypy
```

Final verification result:

```text
Success: no issues found in 10 source files
```

Ruff is configured to check the following rule groups:

| Rule Group | Purpose |
|---|---|
| E | Python style errors |
| F | Common Python programming errors |
| I | Import ordering |
| B | Potential bugs identified by flake8-bugbear |
| UP | Modern Python syntax recommendations |

These checks help maintain consistent and reliable source code.

---

## Settings

Application settings are stored in:

```text
config/weathersummary.toml
```

Example configuration:

```toml
[weather]
source_url = "https://api.open-meteo.com/v1/forecast?latitude=43.65&longitude=-79.38&hourly=temperature_2m,precipitation&past_days=7&forecast_days=1"
timeout = 10

[output]
directory = "data/processed"

[processing]
seed = 42
sample_size = 100

[logging]
level = "INFO"
```

### Configuration Parameters

| Setting | Description |
|---|---|
| weather.source_url | URL of the weather data API |
| weather.timeout | Maximum request timeout in seconds |
| output.directory | Directory for generated reports |
| processing.seed | Reserved for reproducible sampling |
| processing.sample_size | Reserved for future sampling |
| logging.level | Application logging level |

Configuration settings are loaded into a frozen Settings dataclass.

I chose a frozen dataclass to prevent accidental modification
of configuration values after they have been loaded.

The seed and sample_size parameters are included in the configuration
and run metadata, but they are not currently used to sample weather data.

---

## Errors and Exit Codes

Lab 04 introduces application-specific exception classes.

### Exception Hierarchy

```text
WeatherSummaryError
    |
    +-- WeatherSourceError
    |
    +-- WeatherDataError
    |
    +-- WeatherConfigError
```

### Exception Responsibilities

| Exception | Purpose |
|---|---|
| WeatherSummaryError | Base exception for application errors |
| WeatherSourceError | Network and weather API failures |
| WeatherDataError | Invalid or incomplete weather data |
| WeatherConfigError | Missing or invalid configuration settings |

Using custom exceptions makes errors easier to identify
and handle consistently.

The application also uses exception chaining where appropriate
to preserve information about the original error.

### CLI Exit Codes

| Exit Code | Meaning |
|---|---|
| 0 | Application completed successfully |
| 1 | Application failed during execution |

When an application error occurs, the CLI displays an error message
on stderr using the following format:

```text
Error: <description>
```

Internal processing messages use Python's logging module.

---

## Reproducing a Run

Reproducibility is an important part of Lab 04.

I added configuration files, dependency information,
and execution metadata to make it easier to reproduce
the application environment.

### Steps to Reproduce

1. Clone the GitHub repository.
2. Create the Conda environment.
3. Activate the environment.
4. Install the dependencies.
5. Install the Python package.
6. Run the application using the supplied TOML configuration.
7. Review the generated JSON files.

### Environment Information

The repository includes:

**environment.yml**

Defines the Conda environment and Python version.

**requirements.txt**

Records the Python package dependencies.

**pyproject.toml**

Defines package metadata and development tool configuration.

**run_info.json**

Records:

- Application configuration settings
- Python version
- Pytest version
- Mypy version
- Ruff version

### Reproducibility Limitation

The Open-Meteo API provides time-dependent weather data.

Therefore, running the application on different dates
may produce different weather summaries.

The environment and configuration can be reproduced,
but identical weather results require the same source data.

---

## What the Tests Cover

The project contains 33 automated pytest tests.

All tests run offline.

External API calls are replaced with mocked responses
so that testing does not depend on network availability.

### Test Organization

| Test File | Main Responsibility |
|---|---|
| test_models.py | WeatherRecord creation and data validation |
| test_sources.py | API response handling and source errors |
| test_aggregations.py | Weather calculations and missing values |
| test_config.py | TOML configuration loading and validation |
| test_main.py | CLI execution and error handling |
| test_run_info.py | Execution metadata generation |
| conftest.py | Shared test fixtures |

### Testing Techniques

I used several pytest features:

**Fixtures**

Reusable test data is defined in tests/conftest.py.

This avoids repeating the same sample records in multiple tests.

**Parametrization**

Parametrized tests verify multiple inputs and expected results
without duplicating test functions.

**Exception Assertions**

pytest.raises() is used to verify that invalid inputs
produce the expected exceptions.

**Mocking**

monkeypatch is used to replace external API behavior
with controlled test responses.

**Temporary Directories**

tmp_path is used to test file creation without modifying
the project's actual output files.

### Main Testing Scenarios

The tests verify:

- Valid weather records
- Missing or invalid numeric values
- Temperature aggregation
- Precipitation aggregation
- Warmest-day calculations
- Multiple-day datasets
- Empty datasets
- Invalid API responses
- API request failures
- Configuration validation
- Immutable settings
- Successful CLI execution
- Failed CLI execution
- Exit codes and error messages
- Run metadata generation
- JSON output creation

The final test suite contains 33 passing tests.

---

## Project Layout

```text
capstonePrepLab04/
|
|-- config/
|   |-- weathersummary.toml
|
|-- data/
|   |-- raw/
|   |-- processed/
|       |-- summary.json
|       |-- run_info.json
|
|-- src/
|   |-- weathersummary/
|       |-- __init__.py
|       |-- py.typed
|       |-- models.py
|       |-- sources.py
|       |-- aggregations.py
|       |-- report.py
|       |-- config.py
|       |-- exceptions.py
|       |-- logging_setup.py
|       |-- run_info.py
|       |-- main.py
|
|-- tests/
|   |-- conftest.py
|   |-- test_models.py
|   |-- test_sources.py
|   |-- test_aggregations.py
|   |-- test_config.py
|   |-- test_main.py
|   |-- test_run_info.py
|
|-- .gitignore
|-- environment.yml
|-- requirements.txt
|-- pyproject.toml
|-- README.md
```

### Module Responsibilities

Each module has a specific responsibility.

| Module | What It Contains | Why It Is Separate |
|---|---|---|
| models.py | WeatherRecord data model | Keeps weather data representation independent of processing |
| sources.py | WeatherSource class and API handling | Separates external communication from calculations |
| aggregations.py | Temperature, precipitation, and warmest-day aggregation classes | Allows calculations to be tested and extended independently |
| report.py | Summary generation and JSON output | Separates reporting from retrieval and calculations |
| config.py | Settings dataclass and TOML loading | Centralizes configuration and avoids hard-coded settings |
| exceptions.py | Custom application exceptions | Provides consistent error handling |
| logging_setup.py | Logging configuration | Centralizes logging behavior |
| run_info.py | Execution metadata generation | Keeps reproducibility information separate from weather results |
| main.py | CLI entry point and workflow coordination | Keeps application orchestration in one place |
| __init__.py | Package interface | Organizes public package components |
| py.typed | Type information marker | Indicates support for static type checking |

### Why This Structure Was Chosen

I organized the application using the separation of concerns principle.

Each module focuses on one main responsibility.

For example, sources.py does not calculate daily temperatures.
It only retrieves and prepares the weather data.

Similarly, aggregations.py does not communicate with the API.
It receives weather records and performs calculations.

This separation provides several benefits:

- Individual components are easier to understand.
- Tests can focus on one responsibility at a time.
- Changes to the API do not necessarily require changes to calculations.
- New aggregation classes can be added without redesigning the package.
- Errors are easier to locate and debug.
- The application is easier to maintain.

---

## What Moved Where

Lab 04 builds on the package architecture created in Lab 03.

Most of the existing weather-processing functionality
remained in the same modules.

The main changes involved adding reliability,
configuration, testing, and development tools.

| Lab 03 | Lab 04 | Reason for Change |
|---|---|---|
| Existing WeatherRecord model | models.py with improved type checking | Improve type safety |
| Existing WeatherSource class | sources.py with custom errors and logging | Improve API error handling |
| Existing aggregation classes | aggregations.py with validation and logging | Improve reliability |
| Existing report functions | report.py with typed interfaces and logging | Improve maintainability |
| Configuration constants | config.py with TOML-based Settings | Support external configuration |
| Basic application entry point | main.py with CLI and exit codes | Improve command-line execution |
| Basic exception handling | exceptions.py | Introduce consistent custom exceptions |
| No centralized logging setup | logging_setup.py | Standardize logging |
| No execution metadata | run_info.py | Support reproducibility |
| Basic unit tests | Expanded pytest suite | Improve automated test coverage |
| No shared pytest fixtures | tests/conftest.py | Reuse sample test data |
| Limited type checking | Mypy configuration and py.typed | Improve type safety |

This table focuses on the actual changes made between
Lab 03 and Lab 04 rather than repeating the Lab 02
refactoring history.

---

## Design Choices

### 1. Object-Oriented Architecture

I kept the object-oriented structure introduced in Lab 03.

The WeatherRecord class represents one hourly weather observation.

The WeatherSource class handles communication with the API
and prepares the records for processing.

This separates the data model from the data source.

I chose this approach because it makes the code easier
to organize, understand, and test.

### 2. Inheritance and Polymorphism

I used an Aggregation base class to define a common interface
for weather calculations.

Three classes inherit from it:

- TemperatureAggregation
- PrecipitationAggregation
- WarmestDayAggregation

Each class implements its own compute() method.

This allows different calculations to use a consistent interface.

For example, a future HumidityAggregation class could be
added without changing the existing aggregation classes.

### 3. Separation of Concerns

I separated data retrieval, calculations, reporting,
configuration, and application execution into dedicated modules.

This prevents one module from becoming responsible
for too many unrelated operations.

It also makes testing easier because individual components
can be tested without running the entire application.

### 4. Configuration Management

I chose TOML because it is readable and works well
for structured application settings.

The configuration is stored outside the source code,
so settings can be changed without editing Python modules.

I used a frozen dataclass to make configuration values
immutable after loading.

### 5. Custom Exceptions

I introduced custom exceptions to distinguish between
different types of application failures.

For example, a network problem is different from
an invalid configuration value.

Using separate exception classes makes it easier
to identify the source of a failure.

The CLI handles application errors and returns
an appropriate exit code.

### 6. Structured Logging

I used Python's logging module instead of print statements
for internal application messages.

Logging supports different severity levels:

- DEBUG
- INFO
- WARNING
- ERROR

This allows the application to provide useful diagnostic
information without mixing logging with the final CLI output.

### 7. Offline Automated Testing

I chose pytest because it provides useful testing tools,
including fixtures, parametrization, and exception assertions.

I designed the tests to work offline by mocking API responses.

This makes the tests faster and more reliable because
they do not depend on an external service.

### 8. Type Safety

I added type annotations and configured Mypy to check
the Python package.

Type annotations document the expected inputs and outputs
of functions and methods.

They also help detect potential mistakes before runtime.

The py.typed marker indicates that the package includes
type information.

### 9. Reproducibility

I included environment.yml and requirements.txt
to document the required development environment.

I also added run_info.json to record configuration settings
and software versions.

This helps explain how a particular weather report
was generated.

### 10. Incremental Git Development

I used Git commits throughout development rather than
making all changes in one large commit.

I started with the Lab 03 baseline and then committed
formatting, testing, exception handling, configuration,
CLI improvements, reproducibility, and documentation
as separate development stages.

This makes the project history easier to follow
and helps identify when specific changes were introduced.

---

## Known Limitations

The application has the following limitations:

1. **Internet dependency**

   A network connection is required to download live weather data.

2. **Default location**

   The supplied configuration uses Toronto.
   Other locations require changing the API URL.

3. **Time-dependent data**

   Weather results may change between runs because
   the API returns data for a moving date range.

4. **Sampling settings**

   The seed and sample_size settings are stored
   but are not currently used to sample weather records.

5. **JSON output only**

   The application currently generates JSON reports.
   CSV and other export formats are not implemented.

6. **No graphical interface**

   The application is designed to run from the command line.

7. **Limited weather variables**

   The current calculations focus on temperature
   and precipitation.

Future improvements could include additional weather variables,
historical data caching, and alternative report formats.

---

## Repository

GitHub Repository:

https://github.com/matthewkaya/capstonePrepLab04

---

## Final Verification

The final development checks completed successfully.

| Check | Result |
|---|---|
| Ruff Format | 20 files already formatted |
| Ruff Lint | All checks passed |
| Mypy | No issues found in 10 source files |
| Pytest | 33 tests passed |

The project was developed using incremental Git commits,
with the Lab 03 application preserved as the starting baseline.

The final version includes configuration management,
custom exceptions, logging, automated testing,
type checking, and reproducibility metadata.

This completes the Lab 04 package hardening improvements.