"""Formatting helpers for validation results."""


def format_report(results):
    """Return a readable terminal report for validation results.

    Args:
        results: dictionary returned by validate_data().

    Returns:
        A string containing the formatted validation summary.
    """
    total_rows = results.get("total_rows", 0)
    key_column = results.get("key_column", "N/A")
    key_missing_count = results.get("key_missing_count", 0)
    duplicate_key_values = results.get("duplicate_key_values", [])
    required_missing_counts = results.get("required_missing_counts", {})

    if duplicate_key_values:
        duplicates = ", ".join(str(value) for value in duplicate_key_values)
    else:
        duplicates = "None"

    lines = [
        "Data Quality Report",
        "===================",
        f"Total rows: {total_rows}",
        f"Key column: {key_column}",
        f"Missing key values: {key_missing_count}",
        f"Duplicate key values: {duplicates}",
        "Missing values by required column:",
    ]

    if required_missing_counts:
        for column_name, count in required_missing_counts.items():
            lines.append(f"- {column_name}: {count}")
    else:
        lines.append("- None")

    return "\n".join(lines)
