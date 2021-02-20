# Imports
from etl.transform import is_valid_phone, is_valid_date, is_invalid_gos, phone_digits, mod_digits


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


class TestIsInvalidGos:
    def test_both_not_none(self):
        # Arrange
        insp = {
            "grade": "A",
            "score": "0",
        }
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is False

    def test_grade_none(self):
        # Arrange
        insp = {
            "grade": None,
            "score": "0",
        }
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_score_none(self):
        # Arrange
        insp = {
            "grade": "A",
            "score": None,
        }
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_both_none(self):
        # Arrange
        insp = {
            "grade": None,
            "score": None,
        }
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_grade_missing_score_not_none(self):
        # Arrange
        insp = {"score": "0"}
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_grade_missing_score_none(self):
        # Arrange
        insp = {"score": None}
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_score_missing_grade_not_none(self):
        # Arrange
        insp = {"grade": "A"}
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_score_missing_grade_none(self):
        # Arrange
        insp = {"grade": None}
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True

    def test_both_missing(self):
        # Arrange
        insp = {}
        # Act
        result = is_invalid_gos(insp)
        # Assert
        assert result is True


class TestPhoneDigits:
    def test_none(self):
        # Arrange
        phone = None
        expected = ""
        # Act
        result = phone_digits(phone)
        # Assert
        assert result == expected

    def test_empty_string(self):
        # Arrange
        phone = ""
        expected = ""
        # Act
        result = phone_digits(phone)
        # Assert
        assert result == expected

    def test_symbols(self):
        # Arrange
        phone = "#: (123) 456-7890"
        expected = "1234567890"
        # Act
        result = phone_digits(phone)
        # Assert
        assert result == expected

    def test_alphanumeric(self):
        # Arrange
        phone = "My phone number is 123 456 7890"
        expected = "1234567890"
        # Act
        result = phone_digits(phone)
        # Assert
        assert result == expected

    def test_numeric(self):
        # Arrange
        phone = "1234567890"
        expected = "1234567890"
        # Act
        result = phone_digits(phone)
        # Assert
        assert result == expected


class TestModDigits:
    def test_single_digit_mod(self):
        # Arrange
        mod = "01"
        expected = "1"
        # Act
        result = mod_digits(mod)
        # Assert
        assert result == expected

    def test_double_digit_mod(self):
        # Arrange
        mod = "11"
        expected = "11"
        # Act
        result = mod_digits(mod)
        # Assert
        assert result == expected
