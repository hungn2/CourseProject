import pandas as pd

from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabaz_score
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import AgglomerativeClustering
from typing import List, Set


def _get_alphabet(documents: List[str]) -> Set[str]:
	print('Constructing an alphabet given our documents...')
	return set([word for doc in documents for word in doc.split(' ')])


def _encode_documents(documents: List[str]) -> pd.DataFrame:
	print('Encoding documents...')
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
	print('Determing the best cluster...')
	sse = {}
	n_cluster_start = max(int(len(documents) / 100), 2)
	n_cluster_end = max(int(len(documents) / 10), 3)

	for k in range(n_cluster_start, n_cluster_end):
	    #kmeans = KMeans(n_clusters=k, max_iter=9000).fit(documents)
	    kmeans = AgglomerativeClustering(n_clusters=k, linkage="ward").fit(documents)
	    #kmeans = GaussianMixture(n_components=7).fit_predict(documents)
	    label = kmeans.labels_
	    sil_coeff = silhouette_score(documents, label, metric='euclidean')
	    chs = calinski_harabaz_score(documents, label)
	    print("For k={}, The Silhouette Coefficient is {}, {}".format(k, sil_coeff, chs))
	    sse[k] = sil_coeff

	best_n_clusters = max(sse, key=sse.get)

	kmeans = AgglomerativeClustering(n_clusters=best_n_clusters, linkage="ward").fit(documents)

	labels = kmeans.labels_
	return kmeans.labels_


def deduplicate_docs(documents: List[str]) -> List[str]:
	encoded_docs = _encode_documents(documents)

	labels = _get_best_cluster(encoded_docs)

	label_to_doc = {}

	for idx, label in enumerate(labels):
		if label not in label_to_doc:
			label_to_doc[label] = idx

	return [documents[i] for i in label_to_doc.values()]