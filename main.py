# Imports
from etl.extract import extract
from etl.transform import transform
from etl.load import load


# Constants
SOCARTA_TOKEN = None
SOCRATA_COLLECTION = "data.cityofnewyork.us"
SOCRATA_DOCUMENT = "43nn-pn8j"
SOCRATA_RECORD_LIMIT = 400000
EXTRACT_FILE = "data/inspections.json"
TRANSFORM_FILE = "data/restaurants.json"
FIRESTORE_SAK_FILE = "secrets/service-account-key.json"
FIRESTORE_COLLECTION = "restaurants"
FIRESTORE_RECORD_LIMIT = 15000
FIRESTORE_LOAD_CYCLE = 0


# Initializations
def main():
    # Extract raw data from Socrata
    extract(SOCARTA_TOKEN, SOCRATA_COLLECTION, SOCRATA_DOCUMENT, SOCRATA_RECORD_LIMIT, EXTRACT_FILE)
    # Transform raw data
    transform(EXTRACT_FILE, TRANSFORM_FILE)
    # Load transformed data to Firestore
    load(TRANSFORM_FILE, FIRESTORE_SAK_FILE, FIRESTORE_COLLECTION, FIRESTORE_RECORD_LIMIT, FIRESTORE_LOAD_CYCLE)


if __name__ == "__main__":
    main()
