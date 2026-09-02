## BI Data Quality Checker

A small Python CLI project for validating basic CSV data quality.

## Project Goal

The project is created as part of the course
"Programming with AI Assistants".

The goal is to demonstrate an AI-assisted feature delivery workflow:
requirements, implementation, testing, review, documentation, and Git workflow.

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