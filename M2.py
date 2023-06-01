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
stopWords = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
    "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's",
    "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
    "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
]

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
        # print(allPos)

        # Initialize an empty list to store IDs of documents where the full query appears in order
        validId = []
        # Calculate the number of query tokens that are not stop words
        n = len([x for x in tokens if x not in stopWords])
        print(n)  # Print this number for debugging purposes
        # If there is more than one token in the processed query (i.e., there is a sequence to look for)
        if n > 1:
            # Loop over each document where some query words were found
            for x in allPos.keys():
                # Get the list of positions for the current document
                temp = allPos[x]
                # Sort the positions in ascending order
                temp.sort()
                # Look for a sequence of 'n' consecutive positions
                for i in range(len(temp) - n + 1):  # The possible starting indices for such sequence in the list
                    # If all the 'n' numbers starting from the i-th position form a consecutive sequence
                    if all(temp[i + j + 1] - temp[i + j] == 1 for j in range(n - 1)):
                        # Add the current document's ID to the validId list
                        validId.append(x)
                        # Once a valid sequence is found in a document, stop looking in this document
                        break
        # Now, filter out the results to only include those documents where the full query appears in order
        # Sort the documents by their tf-idf scores in descending order
        # Only include those documents that are in validId, or if validId is empty (i.e., the query had less than 2 words)
        results = sorted(
            [(doc_id, score) for doc_id, score in results.items() if doc_id in validId or len(validId) == 0],
            key=lambda x: x[1], reverse=True)

        # Set the number of results to return
        N = 5

        # Get the top 'N' results
        topN = results[:N]

        print("Total of ", len(results))  # Print the total number of valid results found

        # Return the top 'N' results, converting the document IDs back to URLs and packaging them with their scores
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
