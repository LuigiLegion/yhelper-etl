# Imports
from extract import extract
from transform import transform
from load import load


# Constants
SOCARTA_TOKEN = None
SOCRATA_COLLECTION = "data.cityofnewyork.us"
SOCRATA_DOCUMENT = "43nn-pn8j"
SOCRATA_RECORD_LIMIT = 400000
EXTRACT_FILE = "inspections.json"
TRANSFORM_FILE = "restaurants.json"
FIRESTORE_COLLECTION = "restaurants"


# Initializations
def main():
    # Extract raw data from Socrata
    extract(SOCARTA_TOKEN, SOCRATA_COLLECTION, SOCRATA_DOCUMENT, SOCRATA_RECORD_LIMIT, EXTRACT_FILE)
    # Transform raw data
    transform(EXTRACT_FILE, TRANSFORM_FILE)
    # Load transformed data to Firestore
    # load(TRANSFORM_FILE, FIRESTORE_COLLECTION)


if __name__ == '__main__':
    main()
