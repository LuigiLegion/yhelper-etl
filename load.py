# Imports
import pathlib

import simplejson
import firebase_admin
from firebase_admin import credentials, firestore


# Constants
TRANSFORM_FILE = "restaurants.json"
FIRESTORE_SAK_FILE = "serviceAccountKey.json"
FIRESTORE_COLLECTION = "restaurants"
FIRESTORE_RECORD_LIMIT = 15000
FIRESTORE_LOAD_CYCLE = 0


# Initializations
def file_path(file_name):
    return f"{pathlib.Path(__file__).parent.absolute()}/{file_name}"


def load(transform_file, sak_file, collection, limit, cycle):
    try:
        # Determine Firestore service account key file path
        path = file_path(sak_file)

        # Initialize Firestore client
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        # Create transform_file before running this
        with open(transform_file, "r") as f:
            data = simplejson.load(f)

        # Initialize Firestore collection reference
        coll_ref = db.collection(collection)

        # Determine lower, upper, and max bounds
        lower_bound = limit * cycle
        upper_bound = limit * (cycle + 1)
        max_bound = len(data)

        if upper_bound > max_bound:
            upper_bound = max_bound

        for i in range(lower_bound, upper_bound):
            for key, datum in data[i].items():
                coll_ref.document(key).set(datum)
                print(f"Added: {key}")

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Load Process Completed Successfully")


if __name__ == '__main__':
    # Load transformed data to Firestore
    load(TRANSFORM_FILE, FIRESTORE_SAK_FILE, FIRESTORE_COLLECTION, FIRESTORE_RECORD_LIMIT, FIRESTORE_LOAD_CYCLE)
