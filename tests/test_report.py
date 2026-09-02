"""Tests for the report formatting module."""
import pytest

from src.report import format_report


@pytest.fixture
def clean_results():
    """Validation results for a clean dataset."""
    return {
        'total_rows': 100,
        'key_column': 'user_id',
        'key_missing_count': 0,
        'duplicate_key_values': [],
        'required_columns': ['email', 'name'],
        'required_missing_counts': {'email': 0, 'name': 0},
    }


@pytest.fixture
def messy_results():
    """Validation results for a dataset with issues."""
    return {
        'total_rows': 50,
        'key_column': 'customer_id',
        'key_missing_count': 5,
        'duplicate_key_values': ['123', '456'],
        'required_columns': ['email', 'phone'],
        'required_missing_counts': {'email': 3, 'phone': 8},
    }


def test_report_contains_total_rows(clean_results):
    """Verify the report contains total rows."""
    report = format_report(clean_results)
    
    assert 'Total rows: 100' in report


def test_report_contains_key_column(clean_results):
    """Verify the report contains the key column name."""
    report = format_report(clean_results)
    
    assert 'Key column: user_id' in report


def test_report_contains_missing_key_count(clean_results):
    """Verify the report contains missing key count."""
    report = format_report(clean_results)
    
    assert 'Missing key values: 0' in report


def test_report_duplicate_values_displayed(messy_results):
    """Verify duplicate values are displayed in the report."""
    report = format_report(messy_results)
    
    assert 'Duplicate key values: 123, 456' in report


def test_report_none_for_no_duplicates(clean_results):
    """Verify 'None' is displayed when there are no duplicate values."""
    report = format_report(clean_results)
    
    assert 'Duplicate key values: None' in report


def test_report_required_column_missing_counts(messy_results):
    """Verify required-column missing counts are included in report."""
    report = format_report(messy_results)
    
    assert '- email: 3' in report
    assert '- phone: 8' in report


def test_report_structure(clean_results):
    """Verify report has expected structure and sections."""
    report = format_report(clean_results)
    
    assert 'Data Quality Report' in report
    assert '===================' in report
    assert 'Missing values by required column:' in report


def test_report_with_no_required_columns():
    """Verify report handles case with no required columns."""
    results = {
        'total_rows': 10,
        'key_column': 'id',
        'key_missing_count': 0,
        'duplicate_key_values': [],
        'required_columns': [],
        'required_missing_counts': {},
    }
    
    report = format_report(results)
    
    assert '- None' in report


def test_report_preserves_duplicate_order():
    """Verify the report displays duplicate values in the provided order."""
    results = {
        'total_rows': 10,
        'key_column': 'id',
        'key_missing_count': 0,
        'duplicate_key_values': ['zebra', 'apple', 'monkey'],
        'required_columns': [],
        'required_missing_counts': {},
    }

    report = format_report(results)

    assert 'Duplicate key values: zebra, apple, monkey' in report


def test_report_single_duplicate():
    """Verify report correctly displays a single duplicate value."""
    results = {
        'total_rows': 10,
        'key_column': 'id',
        'key_missing_count': 1,
        'duplicate_key_values': ['42'],
        'required_columns': [],
        'required_missing_counts': {},
    }
    
    report = format_report(results)
    
    assert 'Duplicate key values: 42' in report


def test_report_multiple_required_columns_missing_counts():
    """Verify report shows missing counts for multiple required columns."""
    results = {
        'total_rows': 100,
        'key_column': 'id',
        'key_missing_count': 2,
        'duplicate_key_values': [],
        'required_columns': ['col_a', 'col_b', 'col_c'],
        'required_missing_counts': {'col_a': 5, 'col_b': 0, 'col_c': 12},
    }
    
    report = format_report(results)
    
    assert '- col_a: 5' in report
    assert '- col_b: 0' in report
    assert '- col_c: 12' in report


def test_report_is_string():
    """Verify the report is returned as a string."""
    results = {
        'total_rows': 1,
        'key_column': 'id',
        'key_missing_count': 0,
        'duplicate_key_values': [],
        'required_columns': [],
        'required_missing_counts': {},
    }
    
    report = format_report(results)
    
    assert isinstance(report, str)
