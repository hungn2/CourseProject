# CourseProject

## By Blake Jones & Hung Nguyen

This project allows users to query for relevant documents in Slack and/or CampusWire for CS 410. The search results can also be evaluated based on the Cranfield Evaluation Methodology.

### Installation

Install the package and it's dependencies by entering the following command from the repo root. All requirements to execute the app are located within the package. External data files may be generated if requested.
```bash
pip install .
```

### API Setup

Our package requires access to the CampusWire and Slack APIs. You must set environment variables with access credentials to your personal account.

To setup CampusWire API access, open a browser and navigate to CampusWire. Open Developer Tools and navigate to the Network Tab. Search for a request to the posts endpoint (e.g. `https://api.campuswire.com/v1/group/0a3aa370-c917-4993-b5cf-4e06585e7704/posts?number=20`). Look in the request headers for this request, and you will see an *authorization* header with value *Bearer <some_long_string>*. Copy the long string and run the following command:

```bash
export CAMPUSWIRE_TOKEN=<the_long_string>
```

To setup Slack API access, run the following command (which will use a Slackwire bot account):
```bash
export SLACK_TOKEN=xoxb-65616187589-2720748576117-LjSOdyfZRP6a8vwp9GnFzNdw
```

## Commands

Run these commands while in the slackwire directory.

1) To retrieve data from both CampusWire and Slack and store it locally:
```bash
retrieve_combined_data
```

2) To retrieve data from Slack only and store it locally:
```bash
retrieve_slack_data
```

3) To retrieve data from CampusWire only and store it locally:
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
