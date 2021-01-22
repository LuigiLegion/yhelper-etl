# Imports
from operator import itemgetter

from simplejson import load, dump


# Constants
EXTRACT_FILE = "inspections.json"
TRANSFORM_FILE = "restaurants.json"


# Initializations
def valid_phone(phone):
    return phone and len(phone) == 10 and phone.isnumeric()


def valid_date(date):
    return date and date != "1900-01-01T00:00:00.000"


def violation(datum):
    return {
        "description": datum.get("violation_description"),
        "critical": True if datum.get("critical_flag") == "Y" else False
    }


def inspection(datum):
    return {
        "date": datum.get("inspection_date"),
        "grade": datum.get("grade"),
        "score": datum.get("score"),
        "violations": [violation(datum)]
    }


def restaurant(datum, date):
    return {
        "name": datum.get("dba"),
        "phone": datum.get("phone"),
        "building": datum.get("building"),
        "street": datum.get("street"),
        "borough": datum.get("boro"),
        "state": "NY",
        "zipcode": datum.get("zipcode"),
        "latitude": datum.get("latitude"),
        "longitude": datum.get("longitude"),
        "inspections": {date: inspection(datum)}
    }


def transform(extract_file, transform_file):
    # Create extract_file before running this
    with open(extract_file, "r") as f:
        data = load(f)

    # Filter out inspections with invalid phone or inspection_date
    valid_data = list(filter(lambda r: valid_phone(r.get("phone")) and valid_date(r.get("inspection_date")), data))
    # Print number of valid inspections in dataset
    print("valid inspections: ", len(valid_data))  # 394749
    # Sort valid inspections by restaurant name
    sorted_valid_data = sorted(valid_data, key=itemgetter("dba"))

    # Initialize restaurants dict
    rests = {}

    for datum in sorted_valid_data:
        phone = datum.get("phone")
        date = datum.get("inspection_date")

        if phone in rests:
            insps = rests.get(phone).get("inspections")

            if date in insps:
                insp = insps.get(date)
                viol = violation(datum)
                insp.get("violations").append(viol)

                if (insp.get("grade") is None or insp.get("score") is None) and (datum.get("grade") and datum.get("score")):
                    insp["grade"] = datum.get("grade")
                    insp["score"] = datum.get("score")

            else:
                insps[date] = inspection(datum)

        else:
            rests[phone] = restaurant(datum, date)

    # Initialize restaurants list
    rests_list = []

    for phone, rest in rests.items():
        insps_list = [insp for insp in rest.get("inspections").values()]
        sorted_insps_list = sorted(insps_list, key=itemgetter("date"), reverse=True)
        rest["inspections"] = sorted_insps_list
        rests_list.append({phone: rest})

    # Print number of restaurants with valid inspections in dataset
    print("restaurants list: ", len(rests_list))  # 24359

    # Create transform_file before running this
    with open(transform_file, "w+") as f:
        dump(rests_list, f, indent=4)

    print("Transformation Process Completed Successfully")


if __name__ == '__main__':
    # Transform raw data
    transform(EXTRACT_FILE, TRANSFORM_FILE)
