# Imports
from operator import itemgetter
from simplejson import load, dump


# Constants
EXTRACT_FILE = "inspections.json"
TRANSFORM_FILE = "restaurants.json"


# Initializations
def violation(datum):
    return {
        "violation_description": datum.get("violation_description"),
        "critical_flag": datum.get("critical_flag")
    }


def inspection(datum):
    return {
        "score": datum.get("score"),
        "grade": datum.get("grade"),
        "inspection_type": datum.get("inspection_type"),
        "violations": [violation(datum)]
    }


def restaurant(datum, date):
    return {
        "dba": datum.get("dba"),
        "boro": datum.get("boro"),
        "building": datum.get("building"),
        "street": datum.get("street"),
        "zipcode": datum.get("zipcode"),
        "inspections": {date: inspection(datum)}
    }


def transform(extract_file, transform_file):
    # Create extract_file before running this
    with open(extract_file, "r") as f:
        data = load(f)

    # Filter out inspections with invalid phone, dba, or inspection_date
    valid_data = list(filter(lambda r: r.get("phone") and r.get("phone").isnumeric() and r.get("dba") and r.get("inspection_date"), data))
    # Print number of valid inspections in dataset
    print("valid inspections: ", len(valid_data))  # 397246
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
        insps_list = [{date: insp} for date, insp in rest.get("inspections").items()]
        sorted_insps_list = sorted(insps_list, key=lambda r: list(r.keys())[0], reverse=True)
        rest["inspections"] = sorted_insps_list
        rests_list.append({phone: rest})

    # Print number of restaurants with valid inspections in dataset
    print("restaurants list: ", len(rests_list))  # 26256

    # Create transform_file before running this
    with open(transform_file, "w+") as f:
        dump(rests_list, f, indent=4)

    print("Transformation Process Completed Successfully")


if __name__ == '__main__':
    transform(EXTRACT_FILE, TRANSFORM_FILE)
