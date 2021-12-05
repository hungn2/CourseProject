import click
from slackwire.datasets import retrieve_slack_dataset, retrieve_campuswire_dataset, write_dataset, SLACK_DATASET, CAMPUSWIRE_DATASET, COMBINED_DATASET, get_dataset_paths
from slackwire.deduplicate import deduplicate_docs

import math
import sys
import time
import metapy
import pytoml
import logging

@click.group()
@click.option('--very-verbose',
              is_flag=True,
              help='Print verbose log info. Only use for significant debugging.')
@click.option('--verbose',
              is_flag=True,
              help='Print verbose log info. Only use for general debugging.')
def slackwire(very_verbose: bool, verbose: bool) -> None:
    if very_verbose:
        logging.basicConfig(level=logging.DEBUG)
        return
    if verbose:
        logging.basicConfig(level=logging.INFO)
        return
    logging.basicConfig(level=logging.ERROR)


@slackwire.command(help='Initializes slack dataset.')
def initialize_slack() -> None:
    print('Initializing Slack...')
    write_dataset(SLACK_DATASET, retrieve_slack_dataset())
    print('Slack has been initialized.')


@slackwire.command(help='Initializes campuswire dataset.')
def initialize_campuswire() -> None:
    print('Initializing Campuswire...')
    write_dataset(CAMPUSWIRE_DATASET, retrieve_campuswire_dataset())
    print('Campuswire has been initialized.')


@slackwire.command(help='Initializes both slack and campuswire datasets.')
def initialize_combined() -> None:
    print('Initializing both Slack and Campuswire...')
    slack_contents = retrieve_slack_dataset()
    campuswire_contents = retrieve_campuswire_dataset()

    write_dataset(SLACK_DATASET, slack_contents)
    write_dataset(CAMPUSWIRE_DATASET, campuswire_contents)
    combined_docs = slack_contents + campuswire_contents

    deduplicated_docs = combined_docs # deduplicate_docs(combined_docs)

    write_dataset(COMBINED_DATASET, deduplicated_docs)
    print('Both Slack and Campuswire have been initialized.')


@slackwire.command(help='Query for information from Slack and/or Campuswire.')
@click.option('--only-slack',
              is_flag=True,
              help='Search only slack for your query.')
@click.option('--only-campuswire',
              is_flag=True,
              help='Search only campuswire for your query.')
def search(only_slack: bool, only_campuswire: bool) -> None:
    """Search Slack and/or Campuswire for specific topics."""
    query = click.prompt('Enter your query', type=str)
    cfg, dataset = get_dataset_paths(only_slack, only_campuswire)

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
    with open(dataset, "r", encoding='utf-8') as f:
        contents = f.readlines()
        for relevant_doc in relevant_docs:
            print("DOC ID: " + str(relevant_doc) + "\n" + contents[relevant_doc].replace("REPLY:", "\nREPLY:"))

@slackwire.command(help='Evaluate queries in Slack and/or Campuswire.')
@click.option('--only-slack',
              is_flag=True,
              help='Search only slack for your query.')
@click.option('--only-campuswire',
              is_flag=True,
              help='Search only campuswire for your query.')
def search_eval(only_slack: bool, only_campuswire: bool) -> None:
    """Evaluate queries in Slack and/or Campuswire for IR evaluation."""
    cfg, _ = get_dataset_paths(only_slack, only_campuswire)

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

    logging.info('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    ndcg= ndcg / num_queries
            
    logging.info("NDCG@{}: {}".format(top_k, ndcg))
    logging.info("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))

if __name__ == '__main__':
    initialize_combined()
