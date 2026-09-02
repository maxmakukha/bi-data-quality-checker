"""Tests for the data validator module."""
import pytest

from src.validator import validate_data


@pytest.fixture
def clean_dataset():
    """A clean dataset with no quality issues."""
    columns = ['customer_id', 'name', 'email']
    rows = [
        {'customer_id': '1', 'name': 'John Smith', 'email': 'john@example.com'},
        {'customer_id': '2', 'name': 'Jane Doe', 'email': 'jane@example.com'},
        {'customer_id': '3', 'name': 'Bob Wilson', 'email': 'bob@example.com'},
    ]
    return columns, rows


@pytest.fixture
def messy_dataset():
    """A dataset with various quality issues."""
    columns = ['customer_id', 'name', 'email']
    rows = [
        {'customer_id': '1', 'name': 'John Smith', 'email': 'john@example.com'},
        {'customer_id': '', 'name': 'Anna Brown', 'email': ''},  # missing key and email
        {'customer_id': '1', 'name': 'Michael', 'email': 'michael@example.com'},  # duplicate key
        {'customer_id': '  ', 'name': 'Sarah', 'email': 'sarah@example.com'},  # whitespace-only key
        {'customer_id': '5', 'name': '', 'email': 'paul@example.com'},  # missing name
    ]
    return columns, rows


def test_clean_dataset_returns_zero_issues(clean_dataset):
    """Verify a clean dataset returns zero missing and duplicate findings."""
    columns, rows = clean_dataset
    results = validate_data(columns, rows, 'customer_id', ['name', 'email'])
    
    assert results['key_missing_count'] == 0
    assert results['duplicate_key_values'] == []
    assert results['required_missing_counts'] == {'name': 0, 'email': 0}


def test_missing_key_values_counted(messy_dataset):
    """Verify missing key values are counted."""
    columns, rows = messy_dataset
    results = validate_data(columns, rows, 'customer_id', [])
    
    # Row 1 (empty string) and row 3 (whitespace) should be counted as missing
    assert results['key_missing_count'] == 2


def test_duplicate_key_values_detected(messy_dataset):
    """Verify duplicate non-empty key values are detected."""
    columns, rows = messy_dataset
    results = validate_data(columns, rows, 'customer_id', [])
    
    # customer_id '1' appears twice in non-missing rows
    assert '1' in results['duplicate_key_values']


def test_duplicate_values_are_sorted(messy_dataset):
    """Verify duplicate values are sorted in the result."""
    columns = ['id', 'name']
    rows = [
        {'id': '3', 'name': 'A'},
        {'id': '3', 'name': 'B'},
        {'id': '1', 'name': 'C'},
        {'id': '1', 'name': 'D'},
        {'id': '2', 'name': 'E'},
        {'id': '2', 'name': 'F'},
    ]
    
    results = validate_data(columns, rows, 'id', [])
    
    assert results['duplicate_key_values'] == ['1', '2', '3']


def test_required_column_missing_counts(messy_dataset):
    """Verify missing required values are counted separately by column."""
    columns, rows = messy_dataset
    results = validate_data(columns, rows, 'customer_id', ['name', 'email'])
    
    # name: one empty value = 1
    # email: one empty value = 1
    assert results['required_missing_counts']['name'] == 1
    assert results['required_missing_counts']['email'] == 1


def test_whitespace_treated_as_missing():
    """Verify whitespace-only values are treated as missing."""
    columns = ['id', 'name']
    rows = [
        {'id': '1', 'name': 'John'},
        {'id': '2', 'name': '   '},  # whitespace only
        {'id': '3', 'name': '\t'},   # tab
        {'id': '4', 'name': '\n'},   # newline
    ]
    
    results = validate_data(columns, rows, 'id', ['name'])
    
    assert results['required_missing_counts']['name'] == 3


def test_missing_key_column_raises_error(clean_dataset):
    """Verify a missing key column raises ValueError."""
    columns, rows = clean_dataset
    
    with pytest.raises(ValueError, match="Key column not found"):
        validate_data(columns, rows, 'nonexistent_column', [])


def test_missing_required_column_raises_error(clean_dataset):
    """Verify a missing required column raises ValueError."""
    columns, rows = clean_dataset
    
    with pytest.raises(ValueError, match="Required column not found"):
        validate_data(columns, rows, 'customer_id', ['nonexistent_column'])


def test_missing_multiple_required_columns(clean_dataset):
    """Verify error message lists all missing required columns."""
    columns, rows = clean_dataset
    
    with pytest.raises(ValueError) as exc_info:
        validate_data(columns, rows, 'customer_id', ['missing1', 'missing2'])
    
    assert 'missing1' in str(exc_info.value)
    assert 'missing2' in str(exc_info.value)


def test_total_rows_count(messy_dataset):
    """Verify total row count is returned correctly."""
    columns, rows = messy_dataset
    results = validate_data(columns, rows, 'customer_id', [])
    
    assert results['total_rows'] == 5


def test_key_column_in_results(clean_dataset):
    """Verify the key column name is included in results."""
    columns, rows = clean_dataset
    results = validate_data(columns, rows, 'customer_id', [])
    
    assert results['key_column'] == 'customer_id'


def test_required_columns_in_results(clean_dataset):
    """Verify required columns are included in results."""
    columns, rows = clean_dataset
    required = ['name', 'email']
    results = validate_data(columns, rows, 'customer_id', required)
    
    assert results['required_columns'] == required


def test_none_values_treated_as_missing():
    """Verify None values are treated as missing."""
    columns = ['id', 'name']
    rows = [
        {'id': '1', 'name': 'John'},
        {'id': None, 'name': 'Jane'},  # None key
        {'id': '3', 'name': None},     # None required value
    ]
    
    results = validate_data(columns, rows, 'id', ['name'])
    
    assert results['key_missing_count'] == 1
    assert results['required_missing_counts']['name'] == 1
