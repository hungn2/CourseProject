import click
from slackwire import slack
import os
import os.path

import math
import sys
import time
import metapy
import pytoml


@click.command()
def slackwire():
    # retrieve documents from slack
    slack_client = slack.SlackClient()
    threads = slack_client.get_all_threads()

    # ISSUES (when trying to retrieve replies for more than 50 threads)
    # 1) get_thread_replies can't find some threads. Figure out root cause.
    # 2) API is rate limited. Need to add pauses to account for this.
    with safe_open_w("dataset/dataset.dat") as f:
        for i in range(50):
            thread_replies = slack_client.get_thread_replies(
                threads[i].thread_ts)
            if thread_replies:
                contents = "THREAD: " + \
                    thread_replies[0].message.replace("\n", " ") + " "
                for j in range(1, len(thread_replies)):
                    contents += "REPLY #" + str(j) + ": " + \
                        thread_replies[j].message.replace("\n", " ") + " "
                f.write(contents + "\n")
            else:
                print(f'Thread {threads[i].thread_ts} could not be found')

    with safe_open_w("dataset/dataset-full-corpus.txt") as a:
        for path, subdirs, files in os.walk("dataset/threads"):
            for filename in files:
                f = str(path) + "/" + filename
                a.write("[none] " + f + "\n")


def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


'''
@click.command()
@click.argument('query')
@click.option('--only-slack',
              help='Search only slack for your query.')
@click.option('--only-campuswire',
              help='Search only campuswire for your query.')
'''


def search(query: str, only_slack: bool, only_campuswire: bool):
    """Search Slack and/or Campuswire for specific topics."""
    # Call main aggregation function here.
    cfg = "config.toml"
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)

    ranker = metapy.index.OkapiBM25()
    #ranker = metapy.index.JelinekMercer(0.5)
    #ev = metapy.index.IREval(cfg)

    # ISSUES when using CLI:
    # 1) Code breaks here (after setting ranker) for *some* queries (e.g. "surprise")

    # Rank index based on query
    query_doc = metapy.index.Document()
    query_doc.content(query)
    results = ranker.score(idx, query_doc, 10)

    # Collect relevant documents
    relevant_docs = []
    for result in results:
        relevant_docs.append(result[0])

    # Print out relevant document contents
    print("\n*******Search Results*******\n")
    with open("dataset/dataset.dat", "r") as f:
        contents = f.readlines()
        for relevant_doc in relevant_docs:
            print(contents[relevant_doc].replace("REPLY #", "\nREPLY #"))

    # ISSUES when using CLI:
    # 1) Search results don't seem accurate for some queries (e.g. "probability")


if __name__ == '__main__':
    # slackwire()

    # "surprise" works when calling search directly without CLI
    # Copy config.toml, /dataset/, /idx/, and stopwords.txt from root folder to slackwire folder
    # to use search directly.
    search("surprise", False, False)
