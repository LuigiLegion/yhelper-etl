# Imports
import re
from operator import itemgetter
from typing import List, Optional

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
    return mod_digits(date[5:7]) + "/" + mod_digits(date[8:10]) + "/" + date[:4]


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


def transform(extract_file: str, transform_file: str) -> List[dict]:
    # Load inspections data from file
    with open(extract_file, "r") as ef:
        data = load(ef)

    # Initialize restaurants dict
    rests = {}

    for datum in data:
        phone = formatted_phone(phone_digits(datum.get("phone")))
        date = datum.get("inspection_date")

        if is_valid_phone(phone) and is_valid_date(date):
            if phone in rests:
                insps = rests.get(phone).get("inspections")

                if date in insps:
                    insp = insps.get(date)

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
                    insps[date] = inspection(datum)

            else:
                rests[phone] = restaurant(datum, date)

    # Initialize restaurants list
    rests_list = []

    for phone, rest in rests.items():
        insps_list = [i for i in rest.get("inspections").values()]
        sorted_insps = sorted(insps_list, key=itemgetter("date"), reverse=True)

        for sorted_insp in sorted_insps:
            sorted_insp["date"] = formatted_date(sorted_insp.get("date"))

        rest["inspections"] = sorted_insps
        rests_list.append({phone: rest})

    # Print number of restaurants with valid inspections in dataset
    print("total valid restaurants: ", len(rests_list))  # 24252

    # Dump restaurants data to file
    with open(transform_file, "w") as tf:
        dump(rests_list, tf, indent=4)

    print("Transformation Process Completed Successfully")

    return rests_list


if __name__ == "__main__":
    # Transform raw data
    transform(EXTRACT_FILE, TRANSFORM_FILE)
