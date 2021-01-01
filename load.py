# Imports
import pathlib
import simplejson
import firebase_admin
from firebase_admin import credentials, firestore


# Initializations
def load(transform_file, collection):
    try:
        # Retrieve Firestore service account key file path
        path = str(pathlib.Path(__file__).parent.absolute())
        service_acc_key = path + "/serviceAccountKey.json"

        # Initialize Firestore client
        cred = credentials.Certificate(service_acc_key)
        firebase_admin.initialize_app(cred)
        db = firestore.client()

        # Create transform_file before running this
        with open(transform_file, "r") as f:
            data = simplejson.load(f)

        # Initialize Firestore collection reference
        coll_ref = db.collection(collection)

        for key, datum in data.items():
            coll_ref.document(key).set(datum)
            print(f"Added: {key}")

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Load Process Completed Successfully")
