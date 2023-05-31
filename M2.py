import math

import math

import shelve
import json
import heapq
from collections import defaultdict

import nltk
from nltk.stem import PorterStemmer

# List of alphabets
alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z"]


# Define the SearchEngine class
class SearchEngine:
    def __init__(self):
        self.unigramIndex = ""
        # Load pre-processed mappings from files
        with open('id to URL.json', 'r') as f:
            self.id_to_url = json.load(f)
        with open('common.json', 'r') as f:
            self.common = json.load(f)
        with open('important_words.json', 'r') as f:
            self.important_words = json.load(f)
        # Initialize PorterStemmer
        self.stemmer = PorterStemmer()

    # Method to process the query
    def processQuery(self, query):
        # Tokenize and stem the query
        tokens = nltk.word_tokenize(query)
        # Only retain alphanumeric tokens and apply stemming
        tokens = [self.stemmer.stem(token) for token in tokens if token.isalnum()]
        return tokens

    # Method to perform search
    def search(self, query):
        # Process the query
        tokens = self.processQuery(query)
        # Dictionary to store results
        results = defaultdict(float)
        # Set to keep track of documents with query
        docsWithQuery = set()
        # Dictionary to store positions of tokens
        allPos = defaultdict(list)
        print(docsWithQuery)
        for token in tokens:
            # For each token
            if token in self.common:  # If token is a common word
                postings = self.common[token]  # Access the postings list of this token
                # print("common: ", token, postings)
                for doc_id, freq, pos, tf_idf in postings:
                    if token in self.important_words[str(doc_id)]:  # If token is an important word, increase its weight
                        tf_idf *= 1 + math.log(freq)

                        # For every position that is within the query len of another position, modify the score
                        # a naive way to check if two words are next to each other, prone to spamming
                        counter = 0
                        for x in pos:
                            for i in range(x - len(tokens), x + len(tokens) + 1):  # Creates a range of numbers
                                if i in allPos[doc_id]:  # Checks if each number in range is in allPos
                                    counter += 1
                            if counter != 0:
                                tf_idf *= 1 + math.log(
                                    counter)  # Loop to adjust tf_idf based on proximity of other words
                        if counter != 0:
                            tf_idf = 1 + math.log(counter)
                        results[doc_id] += tf_idf
                    allPos[doc_id].extend(pos)
            else:
                # If the token is not a common word, look in specific JSON files based on its first character
                if token[0] in alpha:
                    with open('final unigram ' + token[0] + ".json", 'r') as f:
                        self.unigramIndex = json.load(f)
                elif token[0].isdigit():
                    with open("final unigram number.json", 'r') as f:
                        self.unigramIndex = json.load(f)
                else:
                    with open("final unigram non_alphanumeric.json", 'r') as f:
                        self.unigramIndex = json.load(f)
                # print(token)
                # If the token exists in the unigram index
                if token in self.unigramIndex:
                    # Get all the postings of that token
                    postings = self.unigramIndex[token]
                    # print(token, postings)
                    # For each posting
                    # Doc id, frequency, position, tf-idf score
                    for doc_id, freq, pos, tf_idf in postings:
                        # Same as above
                        if token in self.important_words[str(doc_id)]:
                            tf_idf *= 1 + math.log(freq)
                        counter = 0
                        for x in pos:
                            for i in range(x - len(tokens), x + len(tokens) + 1):  # creates range of numbers
                                if i in allPos[doc_id]:  # checks if each number in range is in allPos
                                    counter += 1
                            if counter != 0:
                                tf_idf *= 1 + math.log(counter)
                        if counter != 0:
                            tf_idf *= 1 + math.log(counter)
                        results[doc_id] += tf_idf
                        allPos[doc_id].extend(pos)
        print(allPos)
        # Sort results by tf-idf score in descending order
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        # Return the top 5 results
        N = 5
        topN = results[:N]
        print("Total of ", len(results))
        return [(self.id_to_url[str(doc_id)], score) for doc_id, score in topN]


if __name__ == "__main__":
    # Instantiate the SearchEngine
    SE = SearchEngine()
    # List of test queries
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    for query in queries:  # For each query
        results = SE.search(query)  # Perform search
        print(f"Top 5 URLs for query '{query}':")  # Print the results
        for url, score in results:
            print(f"URL: {url}, Score: {score}")
