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

---

## Prompt 4 — Validation Report Implementation

**AI Tool:** GitHub Copilot in VS Code

**Goal:** Convert validation results into a readable terminal report.

### Prompt

Review `README.md`, `src/validator.py`, and the current project structure before making changes.

Implement only the report formatting component.

Create `src/report.py`.

Requirements:

- create a function `format_report(results)`;
- accept the dictionary returned by `validate_data()`;
- return the report as a string;
- do not print directly inside `format_report()`;
- show the total number of rows;
- show the key column name;
- show the number of missing key values;
- show duplicate key values;
- show missing value counts for each required column;
- if there are no duplicate key values, display `None`;
- keep the output simple and readable in a terminal;
- use only the Python standard library;
- do not modify the validation results.

Do not implement CLI arguments or tests yet.

Before making changes, briefly explain your implementation plan.

### AI Response Summary

GitHub Copilot created `src/report.py` with a `format_report(results)` function.

The implementation:

- accepts the dictionary returned by `validate_data()`;
- returns a formatted string instead of printing directly;
- shows total row count;
- shows the key column;
- shows missing key values;
- shows duplicate key values;
- shows missing counts for required columns;
- displays `None` when duplicate key values are absent.

### Human Review and Decision

**Accepted with a small simplification.**

The report structure and separation of responsibilities were accepted.

The original duplicate formatting logic used an intermediate value that could be
either a list or a string and then checked its type with `isinstance()`.

This worked correctly, but it was simplified to a direct conditional:

- if duplicate values exist, join them into a readable string;
- otherwise display `None`.

The change reduces unnecessary branching and makes the code easier to explain and maintain.

### Manual Verification

The report formatter was manually verified with both sample datasets.

**Good dataset:**

The generated report showed:

- 4 total rows;
- 0 missing key values;
- no duplicate key values;
- 0 missing values for `name`;
- 0 missing values for `email`.

**Bad dataset:**

The generated report showed:

- 5 total rows;
- 1 missing key value;
- duplicate key value `2`;
- 1 missing value for `name`;
- 1 missing value for `email`.

The output was readable and matched the validation results.

This verification also confirmed that the complete internal flow
`loader → validator → report` works correctly.

---

## Prompt 5 — CLI Integration

**AI Tool:** GitHub Copilot in VS Code

**Goal:** Connect the loader, validator, and report components into a simple command-line interface.

### Prompt

Review `README.md`, `src/loader.py`, `src/validator.py`, `src/report.py`, and the current `main.py`.

Update only `main.py`.

Requirements:

- use Python standard library only;
- use `argparse`;
- accept the CSV file path as a positional argument;
- add `--key` as a required argument for the key column;
- add `--required` as an optional argument accepting zero or more required column names;
- call `load_csv()`;
- call `validate_data()`;
- call `format_report()`;
- print the final formatted report;
- catch `FileNotFoundError` and `ValueError`;
- print a clear error message for expected user input errors;
- keep the implementation small and easy to explain;
- do not add new modules;
- do not modify loader.py, validator.py, or report.py.

Before making changes, briefly explain your implementation plan.

### AI Response Summary

GitHub Copilot updated `main.py` and connected the existing project components into a command-line interface.

The implementation:

- uses `argparse` for command-line arguments;
- accepts the CSV path as a positional argument;
- requires the `--key` argument;
- supports zero or more columns through `--required`;
- connects `load_csv()`, `validate_data()`, and `format_report()`;
- prints the final validation report;
- handles expected `FileNotFoundError` and `ValueError` exceptions;
- writes error messages to `stderr`;
- exits with a non-zero status code when validation cannot be performed.

### Human Review and Decision

**Accepted with no code changes.**

The CLI implementation follows the requested scope and correctly connects the
three existing components.

The use of `sys.stderr` for error messages and a non-zero exit code was accepted
because it clearly separates successful output from expected user errors.

No unnecessary dependencies or additional modules were introduced.

### Manual Verification

The command-line interface was manually verified end-to-end.

**Bad dataset:**

The CLI correctly produced a report with:

- 5 total rows;
- 1 missing key value;
- duplicate key value `2`;
- 1 missing value for `name`;
- 1 missing value for `email`.

**Good dataset:**

The CLI correctly produced a report with:

- 4 total rows;
- 0 missing key values;
- no duplicate key values;
- 0 missing values for `name`;
- 0 missing values for `email`.

**Missing file:**

Using a non-existent CSV path produced:

`Error: CSV file not found: data/not_exists.csv`

**Missing key column:**

Using `wrong_id` as the key column produced:

`Error: Key column not found: wrong_id`

The complete workflow
`CLI → loader → validator → report`
worked as expected.

---

## Prompt 6 — Automated Tests

**AI Tool:** GitHub Copilot in VS Code

**Goal:** Add automated tests for the implemented data quality feature.

### Prompt

Review `README.md`, `src/loader.py`, `src/validator.py`, `src/report.py`, and `main.py`.

Create automated tests using `pytest`.

Create the following files:

- `tests/test_loader.py`
- `tests/test_validator.py`
- `tests/test_report.py`

Requirements:

### Loader tests
- verify that a valid CSV file is loaded correctly;
- verify that column names are returned;
- verify that rows are returned as dictionaries;
- verify that a missing file raises `FileNotFoundError`.

### Validator tests
- verify a clean dataset returns zero missing and duplicate findings;
- verify missing key values are counted;
- verify duplicate non-empty key values are detected;
- verify missing required values are counted separately by column;
- verify whitespace-only values are treated as missing;
- verify a missing key column raises `ValueError`;
- verify a missing required column raises `ValueError`.

### Report tests
- verify the report contains total rows;
- verify duplicate values are displayed;
- verify `None` is displayed when there are no duplicate values;
- verify required-column missing counts are included.

Constraints:
- use `pytest`;
- keep tests small and readable;
- do not test implementation details that are not part of the feature behavior;
- do not modify production code;
- do not add external dependencies other than pytest;
- do not add CLI tests yet.

Before making changes, briefly explain the test plan.

### AI Response Summary

GitHub Copilot generated automated pytest tests for the loader,
validator, and report components.

The generated test suite contained 30 tests covering:

- CSV loading;
- missing files;
- validation of clean and problematic datasets;
- missing and duplicate key values;
- required-column validation;
- whitespace and None values;
- report formatting.

### Test Execution and Human Review

The initial AI-generated test suite was executed with:

`python3 -m pytest -v`

Initial result:

- 30 tests collected;
- 28 tests passed;
- 2 tests failed.

The failures were reviewed manually and both were caused by incorrect
expectations in the AI-generated tests rather than defects in the
production code.

**Issue 1 — Report duplicate ordering**

Copilot created a report test with unsorted duplicate values but expected
the report formatter to sort them.

This contradicted the component design: `validator.py` is responsible for
sorting duplicate values, while `report.py` only formats the provided
validation results.

The test was changed to verify that the report preserves the provided order.

**Issue 2 — Required-column missing count**

Copilot incorrectly expected two missing values in the `name` column of
the test fixture.

Manual inspection showed that only one row had a missing `name`.

The expected count was corrected from `2` to `1`.

### Human Review and Decision

**Accepted with corrections to two AI-generated tests.**

No production code was changed because the failures were caused by
incorrect test expectations.

This demonstrated that AI-generated tests must also be reviewed and
validated rather than accepted automatically.

### Final Test Result

After correcting the two AI-generated test expectations, the full test suite
was executed again with:

`python3 -m pytest -v`

Final result:

- 30 tests collected;
- 30 tests passed;
- 0 tests failed.

The production code did not require changes during this correction cycle.

The final green test run confirmed the behavior of the loader, validator,
and report components across happy paths, negative paths, and edge cases.