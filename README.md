# Yhelper ETL

### Video Presentation:

Coming soon...

### Description:

ETL process that extracts NYC DOH restaurant inspection data from the Socrata Open Data API, transforms it by removing invalid entries and grouping inspections by date under a single restaurant by phone number, and loads it into a Firestore document-based NOSQL database with a REST API.

The REST API will allow consumers to easily retrieve a single restaurant's historical inspection data and incorporate it into their solutions.

MVP completed in a day for a solo project.

### Tech Stack:

Built using Python, sodapy, and Firestore.

### Dev Team:

- Tal Luigi ([LinkedIn](https://www.linkedin.com/in/talluigi) | [GitHub](https://github.com/luigilegion))
