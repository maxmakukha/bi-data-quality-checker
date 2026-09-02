## BI Data Quality Checker

A small Python CLI for basic CSV data quality validation.

## Project Goal

The project is created as part of the course
"Programming with AI Assistants".

The goal is to demonstrate an AI-assisted feature delivery workflow:
requirements, implementation, testing, review, documentation, and Git workflow.

## Overview

This project is a lightweight command-line tool for checking basic data quality in CSV files before they are used in analytics or reporting workflows. It is intentionally small and focused: it validates row counts, missing values, duplicate key values, and missing fields in required columns.

## Features

- Validates a CSV file supplied as a command-line argument.
- Requires a key column using the `--key` option.
- Optionally checks one or more required columns using `--required`.
- Counts the total number of rows in the file.
- Identifies missing values in the key column.
- Detects duplicate non-empty values in the key column.
- Reports missing values separately for each required column.
- Prints a readable summary report to the terminal.
- Raises clear errors for missing files or missing columns.

## Project Structure

- `main.py` - command-line entry point.
- `src/loader.py` - loads CSV files and returns rows.
- `src/validator.py` - checks key and required-column quality rules.
- `src/report.py` - formats the validation summary.
- `data/customers_good.csv` - example valid dataset.
- `data/customers_bad.csv` - example dataset with quality issues.
- `tests/` - automated test suite.
- `prompts.md` - record of the AI-assisted workflow.

## Requirements

- Python 3
- `pytest` from the project requirements file

This project uses only the Python standard library plus the test dependency listed in `requirements.txt`.

## Installation

From the project root, install the required Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Usage

Run the validator from the project root:

```bash
python3 main.py <csv_path> --key <key_column> --required <required_column> [<required_column> ...]
```

### Arguments

- `csv_path`: path to the CSV file to validate.
- `--key`: required column used to check for missing or duplicate values. This is the main identifier column for the dataset.
- `--required`: optional list of one or more columns that must not contain missing values. If omitted, the tool checks only the key column.

### Example using a good dataset

```bash
python3 main.py data/customers_good.csv --key customer_id --required name email
```

### Example using a bad dataset

```bash
python3 main.py data/customers_bad.csv --key customer_id --required name email
```

## Example output

Using the valid dataset:

```text
Data Quality Report
===================
Total rows: 4
Key column: customer_id
Missing key values: 0
Duplicate key values: None
Missing values by required column:
- name: 0
- email: 0
```

Using the dataset with quality issues:

```text
Data Quality Report
===================
Total rows: 5
Key column: customer_id
Missing key values: 1
Duplicate key values: 2
Missing values by required column:
- name: 1
- email: 1
```

## Running tests

```bash
python3 -m pytest -v
```

The current automated test suite contains 31 passing tests.

## AI-Assisted Development

This project was developed using an AI-assisted workflow:

- ChatGPT was used for requirements gathering and planning.
- GitHub Copilot was used for implementation, tests, documentation, and code review.
- The workflow history and prompt decisions are recorded in `prompts.md`.

## Future Improvements

Potential future improvements include:

- handling malformed CSV parsing errors with clearer user-facing messages;
- adding CLI integration tests for exit codes and error output;
- adding optional key normalization rules;
- optimizing validation for very large CSV files;
- adding type hints to public functions.

These improvements were identified during code review but intentionally
deferred to keep the current feature small and within its original scope.

## Feature: Data Quality Validation

The Data Quality Validation feature helps BI Engineers identify basic data quality issues in CSV files before the data is used for analytics.

### User Story

As a BI Engineer, I want to validate a CSV dataset before using it in analytics, so that I can detect basic data quality problems before loading the data into an analytical system.

### Acceptance Criteria

- The application accepts a path to a CSV file.
- The user can specify a key column.
- The application reports the total number of data rows.
- The application detects missing values in the key column.
- The application detects duplicate non-empty values in the key column.
- The user can specify one or more required columns.
- The application reports missing values for each required column.
- A clear error is returned if the CSV file does not exist.
- A clear error is returned if the key column does not exist.
- A clear error is returned if a required column does not exist.
- The application prints a readable data quality report.

### Out of Scope

The feature does not:

- modify or clean the source data;
- infer data types;
- detect statistical anomalies;
- load data into databases;
- provide a web API or GUI;
- perform advanced data profiling.