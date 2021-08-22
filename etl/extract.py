# Imports
from typing import Optional

from sodapy import Socrata
from simplejson import dump


# Constants
SOCARTA_ACCESS_TOKEN = None
SOCRATA_COLLECTION_NAME = "data.cityofnewyork.us"
SOCRATA_DOCUMENT_ID = "43nn-pn8j"
SOCRATA_RECORD_LIMIT = 400000
SOURCE_FILE_PATH = "../data/inspections.json"


# Initializations
def extract(
    access_token: Optional[str],
    collection_name: str,
    document_id: str,
    record_limit: int,
    source_file_path: str,
) -> None:
    """
    Extracts source data from Socrata by initializing a Socarata client for a
    collection given a collection name and access token, extracting the data
    from a document given a document ID and record limit, and writing the data
    to a JSON file given a source file path.
    """

    try:
        client = Socrata(collection_name, access_token)
        data = client.get(document_id, limit=record_limit)
        print(f"total inspections count: {len(data)}")  # 395980

        with open(source_file_path, "w") as f:
            dump(data, f, indent=4)

    except Exception as err:
        print(f"Error: {err}")
        raise err

    else:
        print("Data Extraction Process Completed Successfully")


if __name__ == "__main__":
    extract(
        SOCARTA_ACCESS_TOKEN,
        SOCRATA_COLLECTION_NAME,
        SOCRATA_DOCUMENT_ID,
        SOCRATA_RECORD_LIMIT,
        SOURCE_FILE_PATH,
    )
