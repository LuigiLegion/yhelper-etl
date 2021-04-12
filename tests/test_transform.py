# Imports
from datetime import datetime
from decimal import Decimal

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
    grades,
    unix_time,
    utc_time_object,
    truncated_decimal,
    ratio,
    statistics,
    violation,
    inspection,
    restaurant,
    transform,
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


class TestGrades:
    def test_grades(self):
        # Arrange
        expected = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        # Act
        result = grades()
        # Assert
        assert result == expected


class TestUnixTime:
    def test_unix_time(self):
        # Arrange
        utc_time_obj = datetime.strptime(
            "2015-10-21T00:00:00.000", "%Y-%m-%dT%H:%M:%S.%f"
        )
        expected = 1445385600.0
        # Act
        result = unix_time(utc_time_obj)
        # Assert
        assert result == expected


class TestUtcTimeObject:
    def test_utc_time_object(self):
        # Arrange
        utc_timestamp = "2015-10-21T00:00:00.000"
        expected = datetime(2015, 10, 21, 0, 0)
        # Act
        result = utc_time_object(utc_timestamp)
        # Assert
        assert result == expected


class TestTruncatedDecimal:
    def test_int(self):
        # Arrange
        decimal = 42
        expected = Decimal("42.00")
        # Act
        result = truncated_decimal(decimal, scale=2)
        # Assert
        assert result == expected

    def test_float_round_down_below_half_point(self):
        # Arrange
        decimal = 3.1415926535
        expected = Decimal("3.14")
        # Act
        result = truncated_decimal(decimal, scale=2)
        # Assert
        assert result == expected

    def test_float_round_up_on_half_point(self):
        # Arrange
        decimal = 3.1415926535
        expected = Decimal("3.142")
        # Act
        result = truncated_decimal(decimal, scale=3)
        # Assert
        assert result == expected

    def test_float_round_up_above_half_point(self):
        # Arrange
        decimal = 3.1415926535
        expected = Decimal("3.1416")
        # Act
        result = truncated_decimal(decimal, scale=4)
        # Assert
        assert result == expected


class TestRatio:
    def test_ratio(self):
        # Arrange
        grade_duration = 55.5
        total_duration = 100.0
        expected = Decimal("55.50")
        # Act
        result = ratio(grade_duration, total_duration)
        # Assert
        assert result == expected


class TestStatistics:
    def test_statistics(self):
        # Arrange
        sorted_insps = [
            {
                "date": "2020-02-08T00:00:00.000",
                "grade": "B",
                "score": 19,
            },
            {
                "date": "2020-01-31T00:00:00.000",
                "grade": "C",
                "score": 60,
            },
            {
                "date": "2019-08-07T00:00:00.000",
                "grade": "A",
                "score": 13,
            },
            {
                "date": "2019-06-06T00:00:00.000",
                "grade": "B",
                "score": 19,
            },
            {
                "date": "2018-10-24T00:00:00.000",
                "grade": "C",
                "score": 38,
            },
            {
                "date": "2018-03-13T00:00:00.000",
                "grade": "C",
                "score": 62,
            },
            {
                "date": "2017-10-06T00:00:00.000",
                "grade": "A",
                "score": 5,
            },
            {
                "date": "2017-07-17T00:00:00.000",
                "grade": "A",
                "score": 0,
            },
        ]
        expected = {
            "A": Decimal("65.54"),
            "B": Decimal("10.12"),
            "C": Decimal("24.33"),
        }
        # Act
        result = statistics(sorted_insps)
        # Assert
        assert result == expected


class TestViolation:
    def test_empty_dict(self):
        # Arrange
        datum = {}
        expected = {
            "description": None,
            "critical": False,
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
            "critical": False,
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
            "critical": False,
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected

    def test_non_critical_violation(self):
        # Arrange
        datum = {
            "violation_description": "Current letter grade card not posted.",
            "critical_flag": "N",
        }
        expected = {
            "description": "Current letter grade card not posted.",
            "critical": False,
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected

    def test_critical_violation(self):
        # Arrange
        datum = {
            "violation_description": "Raw, cooked or prepared food is adulterated, contaminated, cross-contaminated, or not discarded in accordance with HACCP plan.",
            "critical_flag": "Y",
        }
        expected = {
            "description": "Raw, cooked or prepared food is adulterated, contaminated, cross-contaminated, or not discarded in accordance with HACCP plan.",
            "critical": True,
        }
        # Act
        result = violation(datum)
        # Assert
        assert result == expected


class TestInspection:
    def test_empty_dict(self):
        # Arrange
        datum = {}
        expected = {
            "date": None,
            "score": None,
            "grade": None,
            "violations": [],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_no_inspection_date(self):
        # Arrange
        datum = {
            "score": "38",
            "grade": "C",
            "violation_description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
            "critical_flag": "Y",
        }
        expected = {
            "date": None,
            "score": 38,
            "grade": "C",
            "violations": [
                {
                    "description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
                    "critical": True,
                },
            ],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_no_score(self):
        # Arrange
        datum = {
            "inspection_date": "2018-10-24T00:00:00.000",
            "grade": "C",
            "violation_description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
            "critical_flag": "Y",
        }
        expected = {
            "date": "2018-10-24T00:00:00.000",
            "score": None,
            "grade": "C",
            "violations": [
                {
                    "description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
                    "critical": True,
                },
            ],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_no_grade(self):
        # Arrange
        datum = {
            "inspection_date": "2018-10-24T00:00:00.000",
            "score": "38",
            "violation_description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
            "critical_flag": "Y",
        }
        expected = {
            "date": "2018-10-24T00:00:00.000",
            "score": 38,
            "grade": "C",
            "violations": [
                {
                    "description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
                    "critical": True,
                },
            ],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_no_violation_description(self):
        # Arrange
        datum = {
            "inspection_date": "2018-10-24T00:00:00.000",
            "score": "38",
            "grade": "C",
            "critical_flag": "Y",
        }
        expected = {
            "date": "2018-10-24T00:00:00.000",
            "score": 38,
            "grade": "C",
            "violations": [],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_no_critical_flag(self):
        # Arrange
        datum = {
            "inspection_date": "2018-10-24T00:00:00.000",
            "score": "38",
            "grade": "C",
            "violation_description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
        }
        expected = {
            "date": "2018-10-24T00:00:00.000",
            "score": 38,
            "grade": "C",
            "violations": [
                {
                    "description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
                    "critical": False,
                },
            ],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_inspection_with_grade_and_critical_violation(self):
        # Arrange
        datum = {
            "inspection_date": "2018-10-24T00:00:00.000",
            "score": "38",
            "grade": "C",
            "violation_description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
            "critical_flag": "Y",
        }
        expected = {
            "date": "2018-10-24T00:00:00.000",
            "score": 38,
            "grade": "C",
            "violations": [
                {
                    "description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
                    "critical": True,
                },
            ],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected

    def test_inspection_with_no_grade_and_non_critical_violation(self):
        # Arrange
        datum = {
            "inspection_date": "2020-01-31T00:00:00.000",
            "score": "60",
            "violation_description": "Plumbing not properly installed or maintained; anti-siphonage or backflow prevention device not provided where required; equipment or floor not properly drained; sewage disposal system in disrepair or not functioning properly.",
            "critical_flag": "N",
        }
        expected = {
            "date": "2020-01-31T00:00:00.000",
            "score": 60,
            "grade": "C",
            "violations": [
                {
                    "description": "Plumbing not properly installed or maintained; anti-siphonage or backflow prevention device not provided where required; equipment or floor not properly drained; sewage disposal system in disrepair or not functioning properly.",
                    "critical": False,
                },
            ],
        }
        # Act
        result = inspection(datum)
        # Assert
        assert result == expected


class TestRestaurant:
    def test_empty_dict(self):
        # Arrange
        datum = {}
        date = "2015-10-21T00:00:00.000"
        expected = {
            "name": None,
            "phone": None,
            "building": None,
            "street": None,
            "borough": None,
            "state": "NY",
            "zip": None,
            "latitude": None,
            "longitude": None,
            "inspections": {
                "2015-10-21T00:00:00.000": {
                    "date": None,
                    "score": None,
                    "grade": None,
                    "violations": [],
                },
            },
        }
        # Act
        result = restaurant(datum, date)
        # Assert
        assert result == expected

    def test_inspection_with_grade_and_critical_violation(self):
        # Arrange
        datum = {
            "dba": "THE STRAND SMOKE HOUSE",
            "boro": "Queens",
            "building": "25-27",
            "street": "BROADWAY",
            "zipcode": "11106",
            "phone": "7184403231",
            "inspection_date": "2018-10-24T00:00:00.000",
            "violation_description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
            "critical_flag": "Y",
            "score": "38",
            "grade": "C",
            "latitude": "40.7633079547",
            "longitude": "-73.92819546732",
        }
        date = "2018-10-24T00:00:00.000"
        expected = {
            "name": "THE STRAND SMOKE HOUSE",
            "phone": "7184403231",
            "building": "25-27",
            "street": "BROADWAY",
            "borough": "Queens",
            "state": "NY",
            "zip": "11106",
            "latitude": "40.7633079547",
            "longitude": "-73.92819546732",
            "inspections": {
                "2018-10-24T00:00:00.000": {
                    "date": "2018-10-24T00:00:00.000",
                    "score": 38,
                    "grade": "C",
                    "violations": [
                        {
                            "description": "Food from unapproved or unknown source or home canned. Reduced oxygen packaged (ROP) fish not frozen before processing; or ROP foods prepared on premises transported to another site.",
                            "critical": True,
                        },
                    ],
                },
            },
        }
        # Act
        result = restaurant(datum, date)
        # Assert
        assert result == expected

    def test_inspection_with_no_grade_and_non_critical_violation(self):
        # Arrange
        datum = {
            "dba": "THE STRAND SMOKE HOUSE",
            "boro": "Queens",
            "building": "25-27",
            "street": "BROADWAY",
            "zipcode": "11106",
            "phone": "7184403231",
            "inspection_date": "2020-01-31T00:00:00.000",
            "violation_description": "Plumbing not properly installed or maintained; anti-siphonage or backflow prevention device not provided where required; equipment or floor not properly drained; sewage disposal system in disrepair or not functioning properly.",
            "critical_flag": "N",
            "score": "60",
            "latitude": "40.7633079547",
            "longitude": "-73.92819546732",
        }
        date = "2020-01-31T00:00:00.000"
        expected = {
            "name": "THE STRAND SMOKE HOUSE",
            "phone": "7184403231",
            "building": "25-27",
            "street": "BROADWAY",
            "borough": "Queens",
            "state": "NY",
            "zip": "11106",
            "latitude": "40.7633079547",
            "longitude": "-73.92819546732",
            "inspections": {
                "2020-01-31T00:00:00.000": {
                    "date": "2020-01-31T00:00:00.000",
                    "score": 60,
                    "grade": "C",
                    "violations": [
                        {
                            "description": "Plumbing not properly installed or maintained; anti-siphonage or backflow prevention device not provided where required; equipment or floor not properly drained; sewage disposal system in disrepair or not functioning properly.",
                            "critical": False,
                        },
                    ],
                },
            },
        }
        # Act
        result = restaurant(datum, date)
        # Assert
        assert result == expected


class TestTransform:
    def test_data_sample(self):
        # Arrange
        expected_file = "tests/data/expected/sample.json"
        extract_file = "tests/data/raw/sample.json"
        transform_file = "tests/data/result/sample.json"

        with open(expected_file, "r") as ef:
            expected = load(ef)

        # Act
        transform(extract_file, transform_file)

        with open(transform_file, "r") as tf:
            result = load(tf)

        # Assert
        assert result == expected
