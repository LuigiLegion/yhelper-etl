# Imports
import os

import simplejson
import firebase_admin
from firebase_admin import credentials, firestore


# Constants
TARGET_FILE_PATH = "../../data/restaurants.json"
FIRESTORE_SAK_FILE_PATH = "secrets/service-account-key.json"
FIRESTORE_COLLECTION_NAME = "restaurants"
FIRESTORE_RECORD_LIMIT = 15000
FIRESTORE_LOAD_CYCLE = 0


# Initializations
def file_path(file_name: str) -> str:
    return f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/{file_name}"


def load(
    target_file_path: str,
    sak_file_path: str,
    collection_name: str,
    record_limit: int,
    load_cycle: int,
) -> None:
    try:
        # Determine Firestore service account key file path
        path = file_path(sak_file_path)

        # Initialize Firestore client
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        # Load restaurants data from file
        with open(target_file_path, "r") as f:
            data = simplejson.load(f)

        # Initialize Firestore collection reference
        collection_ref = db.collection(collection_name)

        # Determine lower, upper, and max bounds
        lower_bound = record_limit * load_cycle
        upper_bound = record_limit * (load_cycle + 1)
        max_bound = len(data)

        if upper_bound > max_bound:
            upper_bound = max_bound

        for i in range(lower_bound, upper_bound):
            for key, datum in data[i].items():
                collection_ref.document(key).set(datum)
                print(f"Added: {key}")

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Data Load Process Completed Successfully")


if __name__ == "__main__":
    load(
        TARGET_FILE_PATH,
        FIRESTORE_SAK_FILE_PATH,
        FIRESTORE_COLLECTION_NAME,
        FIRESTORE_RECORD_LIMIT,
        FIRESTORE_LOAD_CYCLE,
    )
