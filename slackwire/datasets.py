import logging
import os
import pathlib
from contextlib import contextmanager
from os import path
from pathlib import Path
from typing import Generator, List, TextIO, Tuple, Union

from slackwire import campuswire, slack

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
DATASETS_DIR = CURRENT_DIR / 'datasets'
SLACK_DIR = DATASETS_DIR / 'slack'
COMBINED_DIR = DATASETS_DIR / 'combined'
CAMPUSWIRE_DIR = DATASETS_DIR / 'campuswire'

SLACK_DATASET = SLACK_DIR / 'slack.dat'
CAMPUSWIRE_DATASET = CAMPUSWIRE_DIR / 'campuswire.dat'
COMBINED_DATASET = COMBINED_DIR / 'combined.dat'


@contextmanager
def _safe_open_w(path: Union[Path, str]) -> Generator[TextIO, None, None]:
    ''' Open "path" for writing, creating any parent directories as needed.'''
    os.makedirs(os.path.dirname(path), exist_ok=True)
    yield open(path, 'w', encoding='utf-8')


def write_dataset(path: Union[Path, str], dataset: List[str]) -> None:
    if os.path.exists(path):
        # Remove the existing dataset if it's present.
        os.remove(path)
    with _safe_open_w(path) as f:
        f.write('\n'.join(dataset))


def retrieve_slack_dataset() -> List[str]:
    logging.info('Retrieving slack data...')
    slack_client = slack.SlackClient()
    threads = slack_client.get_all_threads()

    slack_contents = []
    for thread in threads:
        contents = ''

        thread_replies = slack_client.get_thread_replies(thread.thread_ts)
        contents += str(thread)
        for message in thread_replies[1:]:
            contents += str(message)
        slack_contents.append(contents)
    return slack_contents


def retrieve_campuswire_dataset() -> List[str]:
    logging.info('Retrieving campuswire data...')
    campuswire_client = campuswire.CampusWire()
    threads = campuswire_client.get_all_threads()

    campuswire_contents = []
    for thread in threads:
        contents = ''

        thread_replies = campuswire_client.get_thread_comments(thread.id)
        contents += str(thread)
        for message in thread_replies:
            contents += str(message)
        campuswire_contents.append(contents)
    return campuswire_contents


def get_dataset_paths(only_slack: bool, only_campuswire: bool) -> Tuple[str, str]:
    dir_path = COMBINED_DIR
    dataset_name = COMBINED_DATASET
    if only_slack:
        dir_path = SLACK_DIR
        dataset_name = SLACK_DATASET
    if only_campuswire:
        dir_path = CAMPUSWIRE_DIR
        dataset_name = CAMPUSWIRE_DATASET

    return str(dir_path / 'config.toml'), str(dataset_name)
