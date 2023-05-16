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

    def process_query(self, query):
        # Tokenize and stem the query
        tokens = nltk.word_tokenize(query)
        # Same processing function in M1.py
        tokens = [self.stemmer.stem(token) for token in tokens if token.isalnum()]
        return tokens

    def search(self, query):
        tokens = self.process_query(query)
        results = defaultdict(float)
        for token in tokens:
            # Only use unigram index for this simple search
            if token in self.unigram_index:
                postings = self.unigram_index[token]
                for doc_id, freq, pos, tf_idf in postings:
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
