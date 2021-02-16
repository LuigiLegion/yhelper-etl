# Imports
from etl.transform import is_valid_phone, is_valid_date


# Tests
class TestIsValidPhone:
    def test_none(self):
        # Arrange
        phone = None
        # Act
        result = is_valid_phone(phone)
        # Assert
        assert result is False

    def test_empty_string(self):
        # Arrange
        phone = ""
        # Act
        result = is_valid_phone(phone)
        # Assert
        assert result is False

    def test_nine_digit_phone(self):
        # Arrange
        phone = "999999999"
        # Act
        result = is_valid_phone(phone)
        # Assert
        assert result is False

    def test_eleven_digit_phone(self):
        # Arrange
        phone = "11111111111"
        # Act
        result = is_valid_phone(phone)
        # Assert
        assert result is False

    def test_invalid_ten_digit_phone(self):
        # Arrange
        phone = "0000000000"
        # Act
        result = is_valid_phone(phone)
        # Assert
        assert result is False

    def test_valid_ten_digit_phone(self):
        # Arrange
        phone = "1234567890"
        # Act
        result = is_valid_phone(phone)
        # Assert
        assert result is True


class TestIsValidDate:
    def test_none(self):
        # Arrange
        date = None
        # Act
        result = is_valid_date(date)
        # Assert
        assert result is False

    def test_empty_string(self):
        # Arrange
        date = ""
        # Act
        result = is_valid_date(date)
        # Assert
        assert result is False

    def test_invalid_default_date(self):
        # Arrange
        date = "1900-01-01T00:00:00.000"
        # Act
        result = is_valid_date(date)
        # Assert
        assert result is False

    def test_partial_date(self):
        # Arrange
        date = "2020-01-31"
        # Act
        result = is_valid_date(date)
        # Assert
        assert result is True

    def test_full_date(self):
        # Arrange
        date = "2020-01-31T00:00:00.000"
        # Act
        result = is_valid_date(date)
        # Assert
        assert result is True
