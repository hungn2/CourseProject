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

To setup Slack API access, you will need to create an app integration.
Go to this link: https://api.slack.com/authentication/basics
And select 'Create a new slack app', then 'create a new app'.
A menu will pop up, select 'From scratch'. Then select the UIUC MCS workspace for 'Pick a workspace to develop your app in:'.

Now that your App has been created, click on "Oauth and Permissions" on the left.
Under 'User Token Scopes', add a new Oauth Scope *channels:history*.
Scroll to the top of the 'Oauth and Permissions' page and select "Install to workspace" and hit allow. You will then see a "User OAuth Token". Copy this token.
```bash
export SLACK_TOKEN=<Insert your User Oauth Token Here>
```

## Commands

The entrypoint for all commands is *slackwire*.
You can print out help messages for general command info via:
```bash
slackwire --help
```

Below is a list of commands you can execute with Slackwire:


1) To retrieve data from both CampusWire and Slack and store it locally:
```bash
slackwire initialize_combined
```

2) To retrieve data from Slack only and store it locally:
```bash
slackwire initialize_slack
```

3) To retrieve data from CampusWire only and store it locally:
```bash
slackwire initialize_campuswire
```

4) To query for relevant threads in both databases, the Slack database only, or the CampusWire database only:
```bash
slackwire search
slackwire search --only-slack
slackwire search --only-campuswire
```

You will then be prompted for your query.


5) To evaluate queries based on the *queries.txt and *qrels.txt files:
```bash
slackwire search_eval
slackwire search_eval --only-slack
slackwire search_eval --only-campuswire
```
