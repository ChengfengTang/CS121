import shelve
import json
import heapq
from collections import defaultdict

import nltk
from nltk.stem import PorterStemmer


class SearchEngine:
    def __init__(self):
        self.unigramIndex = shelve.open('final unigram')
        self.bigramIndex = shelve.open('final bigram')
        self.trigramIndex = shelve.open('final trigram')
        # Files that map IDs to URLs
        with open('id to URL.json', 'r') as f:
            self.id_to_url = json.load(f)
        self.stemmer = PorterStemmer()

    def processQuery(self, query):
        # Tokenize and stem the query
        tokens = nltk.word_tokenize(query)
        # Same processing function in M1.py
        tokens = [self.stemmer.stem(token) for token in tokens if token.isalnum()]
        return tokens

    def search(self, query):
        tokens = self.processQuery(query)
        results = defaultdict(float)

        docsWithQuery = set()
        for i in range(len(tokens) - 1):
            # Check if each pair of consecutive tokens appear next to each other in the documents
            if tokens[i] in self.unigramIndex and tokens[i + 1] in self.unigramIndex:
                postings1 = self.unigramIndex[tokens[i]]
                postings2 = self.unigramIndex[tokens[i + 1]]
                for doc_id1, freq1, pos1, tf_idf1 in postings1:
                    for doc_id2, freq2, pos2, tf_idf2 in postings2:
                        if doc_id1 == doc_id2 and any(j - i == 1 for i, j in zip(pos1, pos2)):
                            # If the same document contains both tokens next to each other
                            docsWithQuery.add(doc_id1)

        for token in tokens:
            # For each token
            if token in self.unigramIndex:
                # Only if it exists in the unigram index
                postings = self.unigramIndex[token]
                # Get all the postings of that token
                # Doc id, frequency, position, tf-idf score
                for doc_id, freq, pos, tf_idf in postings:
                    if doc_id in docsWithQuery:
                        results[doc_id] += tf_idf
        # Sort results by tf-idf score in descending order
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        # Return the top 5 results
        N = 5
        topN = results[:N]
        return [(self.id_to_url[str(doc_id)], score) for doc_id, score in topN]


if __name__ == "__main__":
    SE = SearchEngine()
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering" ] 
    for query in queries:
        results = SE.search(query)
        print(f"Top 5 URLs for query '{query}':")
        for url, score in results:
            print(f"URL: {url}, Score: {score}")
