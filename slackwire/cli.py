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
def retrieve_combined_data():
    pass

@click.command()
def retrieve_slack_data():
    # retrieve documents from slack
    slack_client = slack.SlackClient()
    threads = slack_client.get_all_threads()

    num_threads = 50
    with safe_open_w("slack_dataset/slack_dataset.dat") as f:
        for i in range(num_threads):
            thread_replies = slack_client.get_thread_replies(
                threads[i].thread_ts)
            if thread_replies:
                contents = "THREAD: " + \
                    thread_replies[0].message.replace("\n", " ") + " "
                for j in range(1, len(thread_replies)):
                    contents += "REPLY: " + \
                        thread_replies[j].message.replace("\n", " ") + " "
                f.write(contents + "\n")
            else:
                print(f'Thread {threads[i].thread_ts} could not be found')

@click.command()
def retrieve_campuswire_data():
    pass

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w')


@click.command()
@click.argument('query')
@click.option('--only-slack',
              help='Search only slack for your query.')
@click.option('--only-campuswire',
              help='Search only campuswire for your query.')
def search(query: str, only_slack: bool, only_campuswire: bool):
    """Search Slack and/or Campuswire for specific topics."""
    if only_slack:
        cfg = "slack_config.toml"
    elif only_campuswire:
        cfg = "campuswire_config.toml"
    else:
        cfg = "combined_config.toml"
    idx = metapy.index.make_inverted_index(cfg)

    # Print out information about corpus index
    # print("num_docs = ", idx.num_docs())
    # print("unique_terms = ", idx.unique_terms())
    # print("avg_doc_length = ", idx.avg_doc_length())
    # print("total_corpus_terms = ", idx.total_corpus_terms())

    # Create Ranker
    ranker = metapy.index.OkapiBM25()

    # Rank index based on query
    query_doc = metapy.index.Document()
    query_doc.content(query)
    results = ranker.score(idx, query_doc, 10)

    # Print out relevant document contents
    print("\n*******Search Results*******\n")
    for num, (d_id, _) in enumerate(results):
        content = idx.metadata(d_id).get('content')
        print("Doc ID: {}\n{}\n".format(d_id, content.replace("REPLY:","\nREPLY:")))

if __name__ == '__main__':
    retrieve_combined_data()