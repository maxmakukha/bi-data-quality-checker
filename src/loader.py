import csv
import os


def load_csv(file_path):
    """Load a CSV file and return its column names and row dictionaries.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A tuple: (column_names, data_rows)

    Raises:
        FileNotFoundError: If the CSV file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    with open(file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = reader.fieldnames or []
        rows = list(reader)

    return columns, rows
