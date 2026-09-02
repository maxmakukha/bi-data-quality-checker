def _is_missing(value):
    return value is None or str(value).strip() == ""


def validate_data(columns, rows, key_column, required_columns):
    """Validate a dataset using a key column and required columns.

    Args:
        columns: list of column names
        rows: list of dictionaries from the CSV
        key_column: name of the key column
        required_columns: list of required column names

    Returns:
        Dictionary containing row counts and validation findings.

    Raises:
        ValueError: If the key column or any required column is missing.
    """
    if key_column not in columns:
        raise ValueError(f"Key column not found: {key_column}")

    missing_required = [column for column in required_columns if column not in columns]
    if missing_required:
        missing = ", ".join(missing_required)
        raise ValueError(f"Required column not found: {missing}")

    total_rows = len(rows)

    key_missing_count = 0
    seen_key_values = set()
    duplicate_key_values = set()

    for row in rows:
        key_value = row.get(key_column)
        if _is_missing(key_value):
            key_missing_count += 1
            continue

        normalized_value = str(key_value).strip()
        if normalized_value in seen_key_values:
            duplicate_key_values.add(normalized_value)
        else:
            seen_key_values.add(normalized_value)

    required_missing_counts = {}
    for column in required_columns:
        count = 0
        for row in rows:
            value = row.get(column)
            if _is_missing(value):
                count += 1
        required_missing_counts[column] = count

    return {
        "total_rows": total_rows,
        "key_column": key_column,
        "key_missing_count": key_missing_count,
        "duplicate_key_values": sorted(duplicate_key_values),
        "required_columns": required_columns,
        "required_missing_counts": required_missing_counts,
    }
