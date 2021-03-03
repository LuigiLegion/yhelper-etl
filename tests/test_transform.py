# Imports
from simplejson import load

from etl.transform import (
    is_valid_phone,
    is_valid_date,
    is_valid_score,
    is_valid_grade,
    phone_digits,
    mod_digits,
    grade_by_score,
    formatted_phone,
    formatted_date,
    formatted_score,
    formatted_grade,
    formatted_critical,
    violation,
    transform
)


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


class TestIsValidScore:
    def test_none(self):
        # Arrange
        score = None
        # Act
        result = is_valid_score(score)
        # Assert
        assert result is False

    def test_empty_string(self):
        # Arrange
        score = ""
        # Act
        result = is_valid_score(score)
        # Assert
        assert result is False

    def test_negative_score(self):
        # Arrange
        score = "-1"
        # Act
        result = is_valid_score(score)
        # Assert
        assert result is False

    def test_zero_score(self):
        # Arrange
        score = "0"
        # Act
        result = is_valid_score(score)
        # Assert
        assert result is True

    def test_positive_score(self):
        # Arrange
        score = "42"
        # Act
        result = is_valid_score(score)
        # Assert
        assert result is True


class TestIsValidGrade:
    def test_none(self):
        # Arrange
        grade = None
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is False

    def test_empty_string(self):
        # Arrange
        grade = ""
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is False

    def test_g_grade(self):
        # Arrange
        grade = "G"
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is False

    def test_n_grade(self):
        # Arrange
        grade = "N"
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is False

    def test_p_grade(self):
        # Arrange
        grade = "P"
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is False

    def test_z_grade(self):
        # Arrange
        grade = "Z"
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is False

    def test_a_grade(self):
        # Arrange
        grade = "A"
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is True

    def test_b_grade(self):
        # Arrange
        grade = "B"
        # Act
        result = is_valid_grade(grade)
        # Assert
        assert result is True

    def test_c_grade(self):
        # Arrange
        grade = "C"
        # Act
        result = is_valid_grade(grade)
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


class TestGradeByScore:
    def test_a_grade_highest_score(self):
        # Arrange
        score = 0
        expected = "A"
        # Act
        result = grade_by_score(score)
        # Assert
        assert result == expected

    def test_a_grade_lowest_score(self):
        # Arrange
        score = 13
        expected = "A"
        # Act
        result = grade_by_score(score)
        # Assert
        assert result == expected

    def test_b_grade_highest_score(self):
        # Arrange
        score = 14
        expected = "B"
        # Act
        result = grade_by_score(score)
        # Assert
        assert result == expected

    def test_b_grade_lowest_score(self):
        # Arrange
        score = 27
        expected = "B"
        # Act
        result = grade_by_score(score)
        # Assert
        assert result == expected

    def test_c_grade_highest_score(self):
        # Arrange
        score = 28
        expected = "C"
        # Act
        result = grade_by_score(score)
        # Assert
        assert result == expected

    def test_c_grade_score(self):
        # Arrange
        score = 42
        expected = "C"
        # Act
        result = grade_by_score(score)
        # Assert
        assert result == expected


class TestFormattedPhone:
    def test_empty_string(self):
        # Arrange
        phone = ""
        expected = ""
        # Act
        result = formatted_phone(phone)
        # Assert
        assert result == expected

    def test_ten_digit_phone(self):
        # Arrange
        phone = "2345678900"
        expected = "2345678900"
        # Act
        result = formatted_phone(phone)
        # Assert
        assert result == expected

    def test_eleven_digit_phone(self):
        # Arrange
        phone = "12345678900"
        expected = "2345678900"
        # Act
        result = formatted_phone(phone)
        # Assert
        assert result == expected


class TestFormattedDate:
    def test_both_double_digit(self):
        # Arrange
        date = "2011-11-11T00:00:00.000"
        expected = "11/11/2011"
        # Act
        result = formatted_date(date)
        # Assert
        assert result == expected

    def test_single_digit_day(self):
        # Arrange
        date = "2011-11-01T00:00:00.000"
        expected = "11/1/2011"
        # Act
        result = formatted_date(date)
        # Assert
        assert result == expected

    def test_single_digit_month(self):
        # Arrange
        date = "2011-01-11T00:00:00.000"
        expected = "1/11/2011"
        # Act
        result = formatted_date(date)
        # Assert
        assert result == expected

    def test_both_single_digit(self):
        # Arrange
        date = "2011-01-01T00:00:00.000"
        expected = "1/1/2011"
        # Act
        result = formatted_date(date)
        # Assert
        assert result == expected


class TestFormattedScore:
    def test_none(self):
        # Arrange
        score = None
        # Act
        result = formatted_score(score)
        # Assert
        assert result is None

    def test_empty_string(self):
        # Arrange
        score = ""
        # Act
        result = formatted_score(score)
        # Assert
        assert result is None

    def test_negative_score(self):
        # Arrange
        score = "-1"
        # Act
        result = formatted_score(score)
        # Assert
        assert result is None

    def test_zero_score(self):
        # Arrange
        score = "0"
        expected = 0
        # Act
        result = formatted_score(score)
        # Assert
        assert result == expected

    def test_positive_score(self):
        # Arrange
        score = "42"
        expected = 42
        # Act
        result = formatted_score(score)
        # Assert
        assert result == expected


class TestFormattedGrade:
    def test_both_none(self):
        # Arrange
        grade = None
        score = None
        # Act
        result = formatted_grade(grade, score)
        # Assert
        assert result is None

    def test_both_not_none(self):
        # Arrange
        grade = "C"
        score = 42
        expected = "C"
        # Act
        result = formatted_grade(grade, score)
        # Assert
        assert result == expected

    def test_score_none(self):
        # Arrange
        grade = "C"
        score = None
        expected = "C"
        # Act
        result = formatted_grade(grade, score)
        # Assert
        assert result == expected

    def test_grade_none(self):
        # Arrange
        grade = None
        score = 42
        expected = "C"
        # Act
        result = formatted_grade(grade, score)
        # Assert
        assert result == expected


class TestFormattedCritical:
    def test_none(self):
        # Arrange
        critical = None
        expected = False
        # Act
        result = formatted_critical(critical)
        # Assert
        assert result == expected

    def test_empty_string(self):
        # Arrange
        critical = ""
        expected = False
        # Act
        result = formatted_critical(critical)
        # Assert
        assert result == expected

    def test_not_critical(self):
        # Arrange
        critical = "N"
        expected = False
        # Act
        result = formatted_critical(critical)
        # Assert
        assert result == expected

    def test_critical(self):
        # Arrange
        critical = "Y"
        expected = True
        # Act
        result = formatted_critical(critical)
        # Assert
        assert result == expected


class TestViolation:
    def test_empty_dict(self):
        # Arrange
        datum = {}
        expected = {
            "description": None,
            "critical": False
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected

    def test_no_description(self):
        # Arrange
        datum = {"critical_flag": "N"}
        expected = {
            "description": None,
            "critical": False
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected

    def test_no_critical(self):
        # Arrange
        datum = {"violation_description": "Current letter grade card not posted."}
        expected = {
            "description": "Current letter grade card not posted.",
            "critical": False
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected

    def test_non_critical_violation(self):
        # Arrange
        datum = {
            "violation_description": "Current letter grade card not posted.",
            "critical_flag": "N"
        }
        expected = {
            "description": "Current letter grade card not posted.",
            "critical": False
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected

    def test_critical_violation(self):
        # Arrange
        datum = {
            "violation_description": "Raw, cooked or prepared food is adulterated, contaminated, cross-contaminated, or not discarded in accordance with HACCP plan.",
            "critical_flag": "Y"
        }
        expected = {
            "description": "Raw, cooked or prepared food is adulterated, contaminated, cross-contaminated, or not discarded in accordance with HACCP plan.",
            "critical": True
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected


class TestTransform:
    def test_data_sample(self):
        # Arrange
        expected_file = "tests/data/expected/sample.json"
        extract_file = "tests/data/raw/sample.json"
        transform_file = "tests/data/result/sample.json"

        with open(expected_file, "r") as f:
            expected = load(f)

        # Act
        result = transform(extract_file, transform_file)
        # Assert
        assert result == expected
