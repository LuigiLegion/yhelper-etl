# Imports
from simplejson import dump
from sodapy import Socrata


# Constants
SOCARTA_TOKEN = None
SOCRATA_COLLECTION = "data.cityofnewyork.us"
SOCRATA_DOCUMENT = "43nn-pn8j"
SOCRATA_RECORD_LIMIT = 400000
EXTRACT_FILE = "../data/inspections.json"


# Initializations
def extract(token, collection, document, limit, extract_file):
    try:
        # Initialize Socrata client
        client = Socrata(collection, token)

        # Extract data from document
        data = client.get(document, limit=limit)
        # Print number of inspections in dataset
        print("total inspections: ", len(data))  # 397481

        with open(extract_file, "w") as f:
            dump(data, f, indent=4)

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Extraction Process Completed Successfully")


if __name__ == "__main__":
    # Extract raw data from Socrata
    extract(SOCARTA_TOKEN, SOCRATA_COLLECTION, SOCRATA_DOCUMENT, SOCRATA_RECORD_LIMIT, EXTRACT_FILE)
