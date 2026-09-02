"""Tests for the CSV loader module."""
import os
import tempfile
import pytest

from src.loader import load_csv


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    content = "id,name,email\n1,John,john@example.com\n2,Jane,jane@example.com\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(content)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


def test_load_valid_csv(temp_csv_file):
    """Verify that a valid CSV file is loaded correctly."""
    columns, rows = load_csv(temp_csv_file)
    
    assert len(rows) == 2
    assert len(columns) == 3
    assert columns == ['id', 'name', 'email']


def test_column_names_returned(temp_csv_file):
    """Verify that column names are returned correctly."""
    columns, rows = load_csv(temp_csv_file)
    
    assert columns == ['id', 'name', 'email']
    assert isinstance(columns, list)


def test_rows_as_dictionaries(temp_csv_file):
    """Verify that rows are returned as dictionaries."""
    columns, rows = load_csv(temp_csv_file)
    
    assert isinstance(rows, list)
    assert len(rows) == 2
    
    assert isinstance(rows[0], dict)
    assert rows[0] == {'id': '1', 'name': 'John', 'email': 'john@example.com'}
    
    assert isinstance(rows[1], dict)
    assert rows[1] == {'id': '2', 'name': 'Jane', 'email': 'jane@example.com'}


def test_missing_file_raises_error():
    """Verify that a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_csv('/nonexistent/path/file.csv')


def test_directory_path_raises_value_error():
    """Verify passing a directory path raises ValueError."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError, match="not a file"):
            load_csv(tmpdir)


def test_empty_csv():
    """Verify that an empty CSV file (headers only) returns empty rows."""
    content = "id,name,email\n"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write(content)
        temp_path = f.name
    
    try:
        columns, rows = load_csv(temp_path)
        
        assert columns == ['id', 'name', 'email']
        assert len(rows) == 0
    finally:
        os.unlink(temp_path)
