import logging
from typing import List, Set, cast

import pandas as pd
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.metrics import (calinski_harabasz_score, davies_bouldin_score,
                             silhouette_score)
from sklearn.mixture import GaussianMixture


def _get_alphabet(documents: List[str]) -> Set[str]:
    logging.info('Constructing an alphabet given our documents...')
    return set([word for doc in documents for word in doc.split(' ')])


def _encode_documents(documents: List[str]) -> pd.DataFrame:
    logging.info('Encoding documents...')
    alphabet = _get_alphabet(documents)
    doc_word_counts = []

    for idx, doc in enumerate(documents):
        doc_words = set([word for word in doc.split(' ')])

        word_dict = {
            k: 1 if k in doc_words else 0
            for k in alphabet}
        doc_word_counts.append(word_dict)

    return pd.DataFrame(doc_word_counts)


def _get_best_cluster(documents: pd.DataFrame) -> List[int]:
    logging.info('Determing the best cluster...')
    metrics = {}
    n_cluster_start = max(int(len(documents) / 2), 3)
    n_cluster_end = max(int(len(documents)), 3)
    logging.info(f'Evaluating K between {n_cluster_start} and {n_cluster_end}')

    for k in range(n_cluster_start, n_cluster_end):
        #kmeans = KMeans(n_clusters=k, max_iter=9000).fit(documents)
        clusters = AgglomerativeClustering(
            n_clusters=k, affinity='cosine', linkage='average').fit(documents)
        #kmeans = GaussianMixture(n_components=7).fit_predict(documents)
        label = clusters.labels_
        sil_coeff = silhouette_score(documents, label, metric='euclidean')
        chs = calinski_harabasz_score(documents, label)
        logging.debug(
            'For k={}, The SC and CHS is {}, {}'.format(k, sil_coeff, chs))
        if sil_coeff > 0:
            metrics[k] = sil_coeff

    best_n_clusters = max(metrics, key=metrics.get)  # type: ignore
    logging.info(f'Best K is {best_n_clusters} with {metrics[best_n_clusters]}')
    clusters = AgglomerativeClustering(
        n_clusters=best_n_clusters, affinity='cosine', linkage='average').fit(documents)

    labels = clusters.labels_
    return cast(List[int], labels)


def deduplicate_docs(documents: List[str]) -> List[str]:
    encoded_docs = _encode_documents(documents)

    labels = _get_best_cluster(encoded_docs)

    label_to_doc = {}

    for idx, label in enumerate(labels):
        if label not in label_to_doc:
            label_to_doc[label] = idx

    return [documents[i] for i in label_to_doc.values()]
