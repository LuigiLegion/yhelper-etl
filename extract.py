# Imports
from sodapy import Socrata
from simplejson import dump


# Initializations
def extract(token, collection, document, limit, extract_file):
    try:
        # Initialize Socrata client
        client = Socrata(collection, token)

        # Extract data from document
        data = client.get(document, limit=limit)
        # Print number of inspections in dataset
        print("total inspections: ", len(data))  # 398434

        # Create extract_file before running this
        with open(extract_file, "w+") as f:
            dump(data, f, indent=4)

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Extraction Process Completed Successfully")
