import argparse
import sys

from src.loader import load_csv
from src.validator import validate_data
from src.report import format_report


def main():
    parser = argparse.ArgumentParser(description="BI Data Quality Checker")
    parser.add_argument("csv_path", help="Path to the CSV file")
    parser.add_argument("--key", required=True, help="Name of the key column")
    parser.add_argument(
        "--required",
        nargs="*",
        default=[],
        help="Zero or more required column names",
    )

    args = parser.parse_args()

    try:
        columns, rows = load_csv(args.csv_path)
        results = validate_data(columns, rows, args.key, args.required)
        report = format_report(results)
        print(report)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()