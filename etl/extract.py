# Imports
from typing import Optional

from simplejson import dump
from sodapy import Socrata


# Constants
SOCARTA_TOKEN = None
SOCRATA_COLLECTION = "data.cityofnewyork.us"
SOCRATA_DOCUMENT = "43nn-pn8j"
SOCRATA_RECORD_LIMIT = 400000
EXTRACT_FILE = "../data/inspections.json"


# Initializations
def extract(
    token: Optional[str],
    collection: str,
    document: str,
    limit: int,
    extract_file: str,
) -> None:
    try:
        # Initialize Socrata client
        client = Socrata(collection, token)

        # Extract data from document
        data = client.get(document, limit=limit)

        # Print number of inspections in dataset
        print(f"total inspections count: {len(data)}")  # 395980

        # Dump inspections data to file
        with open(extract_file, "w") as f:
            dump(data, f, indent=4)

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Extraction Process Completed Successfully")


if __name__ == "__main__":
    # Extract source data from Socrata
    extract(
        SOCARTA_TOKEN,
        SOCRATA_COLLECTION,
        SOCRATA_DOCUMENT,
        SOCRATA_RECORD_LIMIT,
        EXTRACT_FILE,
    )
