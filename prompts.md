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

These features are not required for the main User Story and would increase
implementation and testing complexity without adding value to the course
demonstration.