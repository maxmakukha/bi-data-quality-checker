# AI Prompts and Decisions

This document contains the key prompts used during the development of the BI Data Quality Checker, the AI tools used, their suggestions, and the decisions made after human review.

---

## Prompt 1 — Requirements and Feature Planning

**AI Tool:** ChatGPT

**Goal:** Define the scope and requirements for the Data Quality Validation feature.

### Prompt

I am building a small Python CLI project called BI Data Quality Checker.

The target user is a BI Engineer who needs to validate CSV files before using them in analytics.

Help me define a small Data Quality Validation feature.

Requirements:

- accept a CSV file;
- allow the user to specify a key column;
- detect missing key values;
- detect duplicate key values;
- check missing values in required columns;
- print a readable report.

Keep the feature intentionally small and easy to test.

Do not include automatic data cleaning, databases, web APIs, GUI, anomaly detection, or complex Python frameworks.

Provide:

1. User Story
2. Acceptance Criteria
3. Out-of-scope items
4. Suggested implementation plan
5. Important edge cases

### AI Response Summary

ChatGPT proposed:

- a User Story focused on CSV validation before analytical use;
- 11 acceptance criteria;
- separation of the implementation into loader, validator, and report components;
- explicit handling of missing files and missing columns;
- several edge cases for testing.

One useful suggestion that was not explicitly included in the original requirements was validation of missing required columns.

### Human Review and Decisions

**Accepted:**

- simple separation into `loader.py`, `validator.py`, and `report.py`;
- validation of missing key columns;
- validation of missing required columns;
- empty dataset handling;
- duplicate key detection;
- missing value detection.

**Modified:**

- the scope was kept intentionally small;
- only basic CSV validation will be implemented;
- duplicate detection applies only to non-empty key values.

**Rejected / postponed:**

- automatic data cleaning;
- data type inference;
- malformed CSV recovery;
- encoding detection;
- statistical anomaly detection;
- database integration;
- web API or GUI;
- optimization for very large files.

**Reason:**

These features are not required for the main User Story and would increase implementation and testing complexity without adding value to the course demonstration.

---

## Prompt 2 — CSV Loader Implementation

**AI Tool:** GitHub Copilot in VS Code

**Goal:** Implement the CSV loading component using the repository context.

### Prompt

Review the README.md and the current project structure before making changes.

Implement only the CSV loading component for the Data Quality Validation feature.

Create `src/loader.py`.

Requirements:

- use only the Python standard library;
- use the `csv` module;
- create a function `load_csv(file_path)`;
- read the CSV using `csv.DictReader`;
- return the column names and data rows;
- do not perform data quality validation in this module;
- do not modify the source file;
- keep the implementation simple and easy to explain;
- raise a clear error if the file does not exist.

Do not implement validator.py, report.py, CLI arguments, or tests yet.

Before making changes, briefly explain your implementation plan.

### AI Response Summary

GitHub Copilot reviewed the project context and created `src/loader.py`.

The proposed implementation:

- uses Python's standard `csv` module;
- uses `csv.DictReader`;
- returns column names and rows;
- keeps validation logic outside the loader;
- checks whether the input file exists;
- raises a descriptive `FileNotFoundError`;
- does not modify the source CSV.

### Human Review and Decision

**Accepted with no code changes.**

The implementation follows the requested scope and keeps the loader focused on a single responsibility: reading CSV data.

The explicit file existence check was reviewed. Although `open()` can raise `FileNotFoundError` directly, the proposed implementation was kept because it provides a clear project-specific error message and remains easy to understand.

The use of `utf-8-sig` encoding was also accepted because it supports regular UTF-8 CSV files while handling files that contain a UTF-8 BOM.

No validation logic was added to the loader, preserving separation of responsibilities.

### Manual Verification

The AI-generated loader was manually verified before committing the code.

**Happy path:**

`load_csv("data/customers_good.csv")` successfully returned:

- 3 column names;
- 4 data rows;
- rows represented as Python dictionaries.

**Negative path:**

`load_csv("data/not_exists.csv")` raised the expected:

`FileNotFoundError: CSV file not found: data/not_exists.csv`

During the first manual run, the sample CSV files were accidentally placed inside
the `src/data` directory instead of the project-level `data` directory.

The clear `FileNotFoundError` helped identify the incorrect file location.
After moving the files to the correct directory, the loader worked as expected.

---

## Prompt 3 — Data Quality Validator Implementation

**AI Tool:** GitHub Copilot in VS Code

**Goal:** Implement the core data quality validation logic.

### Prompt

Review `README.md`, `src/loader.py`, and the current project structure before making changes.

Implement only the data validation component.

Create `src/validator.py`.

Requirements:

- create a function `validate_data(columns, rows, key_column, required_columns)`;
- verify that `key_column` exists in `columns`;
- verify that every column in `required_columns` exists in `columns`;
- count total rows;
- count missing values in the key column;
- detect duplicate non-empty key values;
- count missing values separately for each required column;
- treat empty strings and whitespace-only strings as missing values;
- do not modify the input rows;
- do not print output inside the validator;
- return validation results as a simple Python dictionary;
- keep the implementation small and easy to explain;
- use only the Python standard library.

If the key column does not exist, raise a clear `ValueError`.

If a required column does not exist, raise a clear `ValueError`.

Do not implement report formatting, CLI arguments, or tests yet.

Before making changes, briefly explain your implementation plan.

### AI Response Summary

GitHub Copilot created `src/validator.py` with a focused validation function.

The implementation:

- validates that the key column exists;
- validates that all required columns exist;
- counts total rows;
- treats `None`, empty strings, and whitespace-only strings as missing;
- counts missing key values;
- detects duplicate non-empty key values;
- counts missing values separately for each required column;
- returns results as a plain Python dictionary;
- does not print output or modify input rows.

### Human Review and Decision

**Accepted with no code changes.**

The duplicate detection logic was reviewed carefully.

The implementation ignores missing key values before duplicate detection, which
matches the project requirement that only non-empty key values are checked for
duplicates.

Duplicate values are stored in a set, so a duplicated key is reported once even
if it appears more than two times.

The returned dictionary is simple, readable, and suitable for both testing and
future report formatting.

No unnecessary dependencies or validation responsibilities were added.

### Manual Verification

The AI-generated validator was manually verified before committing the code.

**Good dataset:**

`validate_data(...)` returned:

- `total_rows = 4`
- `key_missing_count = 0`
- no duplicate key values
- `name` missing count = 0
- `email` missing count = 0

**Bad dataset:**

`validate_data(...)` returned:

- `total_rows = 5`
- `key_missing_count = 1`
- duplicate key value = `2`
- `name` missing count = 1
- `email` missing count = 1

**Missing key column:**

Using `wrong_id` as the key column raised:

`ValueError: Key column not found: wrong_id`

**Missing required column:**

Using `phone` as a required column raised:

`ValueError: Required column not found: phone`

The observed results matched the expected validation behavior.