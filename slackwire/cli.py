import click
from slackwire import slack
from slackwire.deduplicate import deduplicate_docs
import os
import os.path

import math
import sys
import time
import metapy
import pytoml

@click.command()
def retrieve_combined_data():
    slack_contents = _get_slack_data()
    campuswire_contents = _get_campuswire_data()

    combined_docs = slack_contents + campuswire_contents

    deduplicated_docs = deduplicate_docs(combined_docs)

    with safe_open_w("combined_dataset/combined_dataset.dat") as f:
        f.write('\n'.join(deduplicated_docs))


def _get_campuswire_data():
    # TODO
    print('Retrieving campuswire data...')
    return []

def _get_slack_data():
    print('Retrieving slack data...')
    slack_client = slack.SlackClient()
    threads = slack_client.get_all_threads()

    slack_contents = []
    for thread in threads:
        contents = ''

        thread_replies = slack_client.get_thread_replies(thread.thread_ts)
        contents += str(thread)
        for message in thread_replies:
            contents += str(message)
        slack_contents.append(contents)
    return slack_contents


@click.command()
def retrieve_slack_data():
    with safe_open_w("slack_dataset/slack_dataset.dat") as f:
        f.write('\n'.join(_get_slack_data()))
            

@click.command()
def retrieve_campuswire_data():
    with safe_open_w("campuswire_dataset/campuswire_dataset.dat") as f:
        f.write('\n'.join(_get_campuswire_data()))

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
        dataset = "slack_dataset"
    elif only_campuswire:
        cfg = "campuswire_config.toml"
        dataset = "campuswire_dataset"
    else:
        cfg = "combined_config.toml"
        dataset = "combined_dataset"

    idx = metapy.index.make_inverted_index(cfg)
    ranker = metapy.index.OkapiBM25()

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
    with open(f'{dataset}/{dataset}.dat', "r") as f:
        contents = f.readlines()
        for relevant_doc in relevant_docs:
            print("DOC ID: " + str(relevant_doc) + "\n" + contents[relevant_doc].replace("REPLY:", "\nREPLY:"))

@click.command()
@click.option('--only-slack',
              help='Search only slack for your query.')
@click.option('--only-campuswire',
              help='Search only campuswire for your query.')
def search_eval(only_slack: bool, only_campuswire: bool):
    """Evaluate queries in Slack and/or Campuswire for IR evaluation."""
    if only_slack:
        cfg = "slack_config.toml"
    elif only_campuswire:
        cfg = "campuswire_config.toml"
    else:
        cfg = "combined_config.toml"

    idx = metapy.index.make_inverted_index(cfg)
    ranker = metapy.index.OkapiBM25()
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    ndcg= ndcg / num_queries
            
    print("NDCG@{}: {}".format(top_k, ndcg))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))

if __name__ == '__main__':
    retrieve_combined_data()