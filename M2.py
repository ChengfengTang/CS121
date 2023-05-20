import shelve
import json
import heapq
from collections import defaultdict

import nltk
from nltk.stem import PorterStemmer


alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

class SearchEngine:
    def __init__(self):
        self.unigramIndex = ""
        # Files that map IDs to URLs
        with open('id to URL.json', 'r') as f:
            self.id_to_url = json.load(f)
        with open('common.json', 'r') as f:
            self.common = json.load(f)
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

        print(docsWithQuery)
        for token in tokens:
            # For each token
            if token in self.common:
                postings = self.common[token]
                for doc_id, freq, pos, tf_idf in postings:
                    #if doc_id in docsWithQuery:
                        results[doc_id] += tf_idf
            else:
                if token[0] in alpha:
                    with open('final unigram ' + token[0] + ".json", 'r') as f:
                        self.unigramIndex = json.load(f)
                elif token[0].isdigit():
                    with open("final unigram number.json", 'r') as f:
                        self.unigramIndex = json.load(f)
                else:
                    with open("final unigram non_alphanumeric.json", 'r') as f:
                        self.unigramIndex = json.load(f)
                if token in self.unigramIndex:
                    # Only if it exists in the unigram index
                    postings = self.unigramIndex[token]
                    # Get all the postings of that token
                    # Doc id, frequency, position, tf-idf score
                    for doc_id, freq, pos, tf_idf in postings:
                        #if doc_id in docsWithQuery:
                            results[doc_id] += tf_idf
        # Sort results by tf-idf score in descending order
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        # Return the top 5 results
        N = 5
        topN = results[:N]
        return [(self.id_to_url[str(doc_id)], score) for doc_id, score in topN]


if __name__ == "__main__":
    SE = SearchEngine()
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    for query in queries:
        results = SE.search(query)
        print(f"Top 5 URLs for query '{query}':")
        for url, score in results:
            print(f"URL: {url}, Score: {score}")
