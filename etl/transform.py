# Imports
import re
from operator import itemgetter

from simplejson import load, dump


# Constants
EXTRACT_FILE = "../data/inspections.json"
TRANSFORM_FILE = "../data/restaurants.json"


# Initializations
def is_valid_phone(phone):
    return bool(phone) and len(phone) == 10 and phone[0] != "0"


def is_valid_date(date):
    return date and date != "1900-01-01T00:00:00.000"


def is_invalid_gos(insp):
    return insp.get("grade") is None or insp.get("score") is None


def phone_digits(phone):
    return "".join(re.findall(r"\d+", phone)) if phone else ""


def mod_digits(mod):
    return mod[1] if mod[0] == "0" else mod


def formatted_phone(phone):
    return phone[1:] if len(phone) == 11 and phone[0] == 1 else phone


def formatted_date(date):
    return mod_digits(date[5:7]) + "/" + mod_digits(date[8:10]) + "/" + date[:4]


def formatted_gos(gos):
    return gos if gos else None


def formatted_critical(critical):
    return True if critical == "Y" else False


def violation(datum):
    return {
        "description": datum.get("violation_description"),
        "critical": formatted_critical(datum.get("critical_flag"))
    }


def inspection(datum):
    return {
        "date": datum.get("inspection_date"),
        "grade": formatted_gos(datum.get("grade")),
        "score": formatted_gos(datum.get("score")),
        "violations": [violation(datum)] if datum.get("violation_description") else []
    }


def restaurant(datum, date):
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
        "inspections": {date: inspection(datum)}
    }


def transform(extract_file, transform_file):
    # Create extract_file before running this
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

                    if is_invalid_gos(insp):
                        grade = formatted_gos(datum.get("grade"))
                        score = formatted_gos(datum.get("score"))

                        if grade and score:
                            insp["grade"] = grade
                            insp["score"] = score

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
    print("total valid restaurants: ", len(rests_list))  # 24318

    with open(transform_file, "w") as tf:
        dump(rests_list, tf, indent=4)

    print("Transformation Process Completed Successfully")


if __name__ == "__main__":
    # Transform raw data
    transform(EXTRACT_FILE, TRANSFORM_FILE)
