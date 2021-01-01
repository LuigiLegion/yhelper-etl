# Imports
from operator import itemgetter
from simplejson import load, dump


# Initializations
def inspection(datum):
    return {
        "inspection_date": datum.get("inspection_date"),
        # "action": datum.get("action"),
        # "violation_code": datum.get("violation_code"),
        "violation_description": datum.get("violation_description"),
        "critical_flag": datum.get("critical_flag"),
        "score": datum.get("score"),
        "grade": datum.get("grade"),
        # "grade_date": datum.get("grade_date"),
        # "record_date": datum.get("record_date"),
        "inspection_type": datum.get("inspection_type")
    }


def restaurant(datum, insp, date):
    return {
        # "camis": datum.get("camis"),
        "dba": datum.get("dba"),
        "boro": datum.get("boro"),
        "building": datum.get("building"),
        "street": datum.get("street"),
        "zipcode": datum.get("zipcode"),
        # "phone": datum.get("phone"),
        # "cuisine_description": datum.get("cuisine_description"),
        # "latitude": datum.get("latitude"),
        # "longitude": datum.get("longitude"),
        # "community_board": datum.get("community_board"),
        # "council_district": datum.get("council_district"),
        # "census_tract": datum.get("census_tract"),
        # "bin": datum.get("bin"),
        # "bbl": datum.get("bbl"),
        # "nta": datum.get("nta"),
        "inspections": {date: [insp]}
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
        insp = inspection(datum)
        date = insp.get("inspection_date")

        if phone in rests:
            insps = rests.get(phone).get("inspections")

            if date in insps:
                insps.get(date).append(insp)
            else:
                insps[date] = [insp]
        else:
            rest = restaurant(datum, insp, date)
            rests[phone] = rest

    # Print number of restaurants with valid inspections in dataset
    print("restaurants: ", len(rests.keys()))  # 26256

    # Create transform_file before running this
    with open(transform_file, "w+") as f:
        dump(rests, f, indent=4)

    print("Transformation Process Completed Successfully")
