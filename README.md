# CourseProject

## By Blake Jones & Hung Nguyen

This project allows users to query for relevant documents in Slack and/or CampusWire for CS 410. The search results can also be evaluated based on the Cranfield Evaluation Methodology.

First, install dependencies by entering the following command:
```bash
pip install .
```

The CLI commands below can then be used.

1) To retrieve data from both CampusWire and Slack and store it locally (**TO BE IMPLEMENTED**):
```bash
retrieve_combined_data
```

2) To retrieve data from Slack only and store it locally (**CURRENTLY LIMITED BY API RATES: RETRIEVING 50 MOST RECENT THREADS ONLY**):
```bash
retrieve_slack_data
```

3) To retrieve data from CampusWire only and store it locally (**TO BE IMPLEMENTED**):
```bash
retrieve_campuswire_data
```

4) To query for relevant threads in both databases, the Slack database only, or the CampusWire database only:
```bash
search "your query here"
search "your query here" --only-slack=true
search "your query here" --only-campuswire=true
```

5) To evaluate queries based on the *queries.txt and *qrels.txt files:
```bash
search_eval
search_eval --only-slack=true
search_eval --only-campuswire=true
```
