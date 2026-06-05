"""
Validation Test Suite
Verifies that the ItemValidator correctly enforces schema rules, data types, 
and length constraints independently of the HTTP routing layer.
"""
import pytest
from app.validators.item_validator import ItemValidator

def test_valid_item_creation_payload():
    """Test that a perfectly valid payload passes validation."""
    data = {"name": "Production Server", "description": "High-memory compute node."}
    is_valid, error = ItemValidator.validate_item_payload(data)
    
    assert is_valid is True
    assert error is None

def test_missing_required_name():
    """Test that missing the required 'name' field fails validation."""
    data = {"description": "Missing the name field entirely."}
    is_valid, error = ItemValidator.validate_item_payload(data)
    
    assert is_valid is False
    assert error["code"] == "VALIDATION_ERROR"
    assert "required" in error["message"]

def test_name_too_short():
    """Test length constraint on the 'name' field."""
    data = {"name": "DB"}  # Less than 3 characters
    is_valid, error = ItemValidator.validate_item_payload(data)
    
    assert is_valid is False
    assert error["code"] == "VALIDATION_ERROR"
    assert "least 3 characters" in error["message"]

def test_invalid_description_type():
    """Test type checking on the 'description' field."""
    data = {"name": "Valid Name", "description": {"nested": "dict"}}  # Should be string
    is_valid, error = ItemValidator.validate_item_payload(data)
    
    assert is_valid is False
    assert error["code"] == "VALIDATION_ERROR"
    assert "must be a string" in error["message"]

def test_valid_update_payload_no_name():
    """Test that an update payload is valid even without a name (partial update)."""
    data = {"description": "Only updating the description."}
    is_valid, error = ItemValidator.validate_item_payload(data, is_update=True)
    
    assert is_valid is True
    assert error is None