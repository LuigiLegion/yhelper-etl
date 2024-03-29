# Imports
import re
from operator import itemgetter
from datetime import datetime
from decimal import Decimal, ROUND_HALF_EVEN
from typing import List, Optional, Union

from simplejson import load, dump


# Constants
EXTRACT_FILE = "../data/inspections.json"
TRANSFORM_FILE = "../data/restaurants.json"


# Initializations
def is_valid_phone(phone: Optional[str]) -> bool:
    return isinstance(phone, str) and len(phone) == 10 and phone[0] != "0"


def is_valid_date(date: Optional[str]) -> bool:
    return isinstance(date, str) and bool(date) and date != "1900-01-01T00:00:00.000"


def is_valid_score(score: Optional[str]) -> bool:
    return isinstance(score, str) and str.isnumeric(score)


def is_valid_grade(grade: Optional[str]) -> bool:
    return grade == "A" or grade == "B" or grade == "C"


def phone_digits(phone: Optional[str]) -> str:
    return "".join(re.findall(r"\d+", phone)) if isinstance(phone, str) else ""


def mod_digits(mod: str) -> str:
    return mod[1] if mod[0] == "0" else mod


def grade_by_score(score: int) -> str:
    if 0 <= score <= 13:
        return "A"

    elif 14 <= score <= 27:
        return "B"

    else:
        return "C"


def formatted_phone(phone: str) -> str:
    return phone[1:] if len(phone) == 11 and phone[0] == "1" else phone


def formatted_date(date: str) -> str:
    return f"{mod_digits(date[5:7])}/{mod_digits(date[8:10])}/{date[:4]}"


def formatted_score(score: Optional[str]) -> Optional[int]:
    return int(score) if is_valid_score(score) else None


def formatted_grade(
    grade: Optional[str],
    score: Optional[int],
) -> Optional[str]:
    if is_valid_grade(grade):
        return grade

    elif score is not None:
        return grade_by_score(score)

    else:
        return None


def formatted_critical(critical: Optional[str]) -> bool:
    return True if critical == "Y" else False


def grades() -> dict:
    return {
        "A": 0,
        "B": 0,
        "C": 0,
    }


def unix_time(utc_time_obj) -> float:
    return (utc_time_obj - datetime(1970, 1, 1)).total_seconds()


def utc_time_object(utc_timestamp: str):
    return datetime.strptime(utc_timestamp, "%Y-%m-%dT%H:%M:%S.%f")


def truncated_decimal(decimal: Union[float, int], scale: int) -> Decimal:
    dec = Decimal(decimal)
    exp = Decimal("0." + ("0" * (scale - 1)) + "1")

    return dec.quantize(exp, rounding=ROUND_HALF_EVEN)


def ratio(grade_duration: float, total_duration: float) -> Decimal:
    return truncated_decimal((grade_duration / total_duration) * 100, scale=2)


def statistics(
    sorted_insps: List[dict],
    unix_time_now: float = unix_time(datetime.utcnow()),
) -> dict:
    durations = grades()

    insps_count = len(sorted_insps) - 1
    prev_grade = None

    for i, insp in enumerate(sorted_insps):
        grade = insp.get("grade")

        if grade:
            if prev_grade is None:
                prev_grade = grade

            if i == insps_count:
                insp_unix_time = unix_time_now
                prev_insp_unix_time = unix_time(utc_time_object(insp.get("date")))

            else:
                insp_unix_time = unix_time(utc_time_object(insp.get("date")))
                prev_insp_unix_time = unix_time(
                    utc_time_object(sorted_insps[i + 1].get("date"))
                )

            unix_time_diff = insp_unix_time - prev_insp_unix_time
            durations[grade] += unix_time_diff

    total_duration = durations.get("A") + durations.get("B") + durations.get("C")

    ratios = grades()

    if total_duration:
        for grade, duration in durations.items():
            ratios[grade] = ratio(duration, total_duration)

    return ratios


def violation(datum: dict) -> dict:
    return {
        "description": datum.get("violation_description"),
        "critical": formatted_critical(datum.get("critical_flag")),
    }


def inspection(datum: dict) -> dict:
    score = formatted_score(datum.get("score"))

    return {
        "date": datum.get("inspection_date"),
        "score": score,
        "grade": formatted_grade(datum.get("grade"), score),
        "violations": [violation(datum)] if datum.get("violation_description") else [],
    }


def restaurant(datum: dict, date: str) -> dict:
    return {
        "name": datum.get("dba"),
        "phone": datum.get("phone"),
        "building": datum.get("building"),
        "street": datum.get("street"),
        "borough": datum.get("boro"),
        "state": "NY",
        "zip": datum.get("zipcode"),
        "latitude": datum.get("latitude"),
        "longitude": datum.get("longitude"),
        "inspections": {date: inspection(datum)},
    }


def transform(
    extract_file: str,
    transform_file: str,
    is_test: bool = False,
) -> List[dict]:
    # Load inspections data from file
    with open(extract_file, "r") as ef:
        data = load(ef)

    # Initialize restaurants dict
    restaurants = {}

    for datum in data:
        phone = formatted_phone(phone_digits(datum.get("phone")))
        date = datum.get("inspection_date")

        if is_valid_phone(phone) and is_valid_date(date):
            if phone in restaurants:
                inspections = restaurants.get(phone).get("inspections")

                if date in inspections:
                    insp = inspections.get(date)

                    if datum.get("violation_description"):
                        viol = violation(datum)
                        insp.get("violations").append(viol)

                    if insp.get("score") is None:
                        score = formatted_score(datum.get("score"))
                        grade = formatted_grade(datum.get("grade"), score)

                        if score and grade:
                            insp["score"] = score
                            insp["grade"] = grade

                else:
                    inspections[date] = inspection(datum)

            else:
                restaurants[phone] = restaurant(datum, date)

    # Initialize restaurants list
    restaurant_list = []

    for phone, rest in restaurants.items():
        inspection_list = [i for i in rest.get("inspections").values()]
        sorted_inspections = sorted(inspection_list, key=itemgetter("date"), reverse=True)

        rest["statistics"] = (
            statistics(sorted_inspections, unix_time_now=1621798200.121685)
            if is_test
            else statistics(sorted_inspections)
        )

        for sorted_inspection in sorted_inspections:
            sorted_inspection["date"] = formatted_date(sorted_inspection.get("date"))

        rest["inspections"] = sorted_inspections
        restaurant_list.append({phone: rest})

    # Print number of restaurants with valid inspections in dataset
    print(f"total restaurants count: {len(restaurant_list)}")  # 24258

    # Dump restaurants data to file
    with open(transform_file, "w") as tf:
        dump(restaurant_list, tf, indent=4)

    print("Data Transformation Process Completed Successfully")

    return restaurant_list


if __name__ == "__main__":
    transform(EXTRACT_FILE, TRANSFORM_FILE)
