# Yhelper ETL

### Video Presentation:

Coming soon...

### Description:

ETL process that extracts DOH NYC restaurant inspection results data using the Socrata Open Data API, transforms it by removing invalid entries and grouping inspections by date under a single restaurant by phone number, and loads it into a Firestore document-based NoSQL database with a built-in REST API.

The REST API will allow consumers to easily retrieve a single restaurant's historical inspection data and incorporate it into their solutions.

MVP completed in a day for a solo project.

### Tech Stack:

Built using Python, sodapy, and firebase-admin.

### Dev Team:

- Tal Luigi ([LinkedIn](https://www.linkedin.com/in/talluigi) | [GitHub](https://github.com/luigilegion))
