import pytest
from src.utils import DataValidator

@pytest.mark.parametrize("email,expected", [
    ("john@example.com", True),
    ("wrong@", False)
])
def test_email_validator(email, expected):
    assert DataValidator.is_valid_email(email) == expected