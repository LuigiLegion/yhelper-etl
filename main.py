# Imports
from etl.extract import extract
from etl.transform import transform
from etl.load import load


# Constants
SOCARTA_ACCESS_TOKEN = None
SOCRATA_COLLECTION_NAME = "data.cityofnewyork.us"
SOCRATA_DOCUMENT_ID = "43nn-pn8j"
SOCRATA_RECORD_LIMIT = 400000
SOURCE_FILE_PATH = "data/inspections.json"
TARGET_FILE_PATH = "data/restaurants.json"
FIRESTORE_SAK_FILE_PATH = "secrets/service-account-key.json"
FIRESTORE_COLLECTION_NAME = "restaurants"
FIRESTORE_RECORD_LIMIT = 15000
FIRESTORE_LOAD_CYCLE = 0


# Initializations
def main():
    extract(
        SOCARTA_ACCESS_TOKEN,
        SOCRATA_COLLECTION_NAME,
        SOCRATA_DOCUMENT_ID,
        SOCRATA_RECORD_LIMIT,
        SOURCE_FILE_PATH,
    )

    transform(SOURCE_FILE_PATH, TARGET_FILE_PATH)

    load(
        TARGET_FILE_PATH,
        FIRESTORE_SAK_FILE_PATH,
        FIRESTORE_COLLECTION_NAME,
        FIRESTORE_RECORD_LIMIT,
        FIRESTORE_LOAD_CYCLE,
    )


if __name__ == "__main__":
    main()
