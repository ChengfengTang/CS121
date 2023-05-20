import math
import os
import json
import shelve
import string
import shelve
import json
import re
from simhash import Simhash
from nltk.util import bigrams, trigrams
import nltk
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict

from nltk import re

fingerprints = []
pagesToAvoid = [r"https://cbcl\.ics\.uci\.edu/public_data/[\w\-./]+",  # Useless texts with junk numbers
                r"http://mondego\.ics\.uci\.edu/datasets/[\w\-./]+",  # can't load
                r"https://www\.ics\.uci\.edu/~kay/[\w\-./]+"]  # too large
alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def readFiles(path):
    # Create a dictionary to store the documents
    docs = {}
    # Iterate over all the files in the provided directory
    for domain in os.listdir(path):
        # Join the path and domain name to create the full path
        domainFolder = os.path.join(path, domain)
        # Check if the path is a directory
        if os.path.isdir(domainFolder):
            # Iterate over all the files in the directory
            for page in os.listdir(domainFolder):
                # Join the domain folder path and page name to create the full file path
                file_path = os.path.join(domainFolder, page)
                # Open the file
                with open(file_path, 'r') as f:
                    # Load the file content as JSON
                    temp = json.load(f)
                    # Add the file content to the dictionary
                    docs[temp['url']] = temp['content']
            # Print the number of documents
            print("ok", len(docs))
    # Return the documents
    return docs


def tokenize(content):
    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    # Get the text from the HTML
    text = soup.get_text()
    tokens = nltk.word_tokenize(text)
    """
    global fingerprints
    # Tokenize the text only if there has not been a similar page
    temp = Simhash(tokens)
    for fingerprint in fingerprints:
        # Threshold is 2
        if temp.distance(fingerprint) < 3:
            return []
    fingerprints.append(temp)
    """
    # Create a PorterStemmer object
    stemmer = PorterStemmer()
    # Stem tokens
    tokens = [stemmer.stem(token) for token in tokens if token.isalnum()]
    # Return the tokens
    return tokens


def getIndex(documents):
    unigramIndex = defaultdict(list)
    # bigramIndex = defaultdict(list)
    # trigramIndex = defaultdict(list)
    idToURL = {}  # dictionary to map IDs to URLs for retrieval
    counter = 1
    docCounter = 1  # document counter will now serve as ID
    totalDocs = len(documents)  # keeps track of the total number of documents

    for url, text in documents.items():
        if any(re.search(pattern, url) for pattern in pagesToAvoid):
            print(text)
            continue
        print(url)
        idToURL[docCounter] = url  # map the url with its id
        tokens = tokenize(text)
        temp1 = nltk.FreqDist(tokens)
        temp2 = nltk.FreqDist(map(','.join, bigrams(tokens)))
        temp3 = nltk.FreqDist(map(','.join, trigrams(tokens)))
        # Indexing unigrams
        for token, frequency in temp1.items():
            positions = [i for i, t in enumerate(tokens) if t == token]  # Find positions of the token
            idf = math.log(totalDocs / len(unigramIndex[token])) if unigramIndex[token] else 0  # Calculate IDF
            tf_idf = frequency * idf  # Calculate TF-IDF
            unigramIndex[token].append([docCounter, frequency, positions, tf_idf])
        """
        # Indexing bigrams
        for token, frequency in temp2.items():
            positions = [i for i, t in enumerate(bigrams(tokens)) if
                         ' '.join(t) == token]  # Find positions of the token
            idf = math.log(totalDocs / len(bigramIndex[token])) if bigramIndex[token] else 0  # Calculate IDF
            tf_idf = frequency * idf  # Calculate TF-IDF
            bigramIndex[token].append([docCounter, frequency, positions, tf_idf])

        # Indexing trigrams
        for token, frequency in temp3.items():
            positions = [i for i, t in enumerate(trigrams(tokens)) if
                         ' '.join(t) == token]  # Find positions of the token
            idf = math.log(totalDocs / len(trigramIndex[token])) if trigramIndex[token] else 0  # Calculate IDF
            tf_idf = frequency * idf  # Calculate TF-IDF
            trigramIndex[token].append([docCounter, frequency,positions, tf_idf])
        """
        docCounter += 1
        if docCounter % (len(documents) // 3) == 0:  # Now we save every 1/3
            saveIndex("unigram index" + str(counter) + ".json", unigramIndex)
            # saveIndex("bigram index" + str(counter) + ".json", bigramIndex)
            # saveIndex("trigram index" + str(counter) + ".json", trigramIndex)
            unigramIndex.clear()
            # bigramIndex.clear()
            # trigramIndex.clear()
            counter += 1
        print("ok ", docCounter, counter, len(unigramIndex))  # , len(bigramIndex), len(trigramIndex))

    if unigramIndex:  # Save the last partial index if it exists
        saveIndex("unigram index" + str(counter) + ".json", unigramIndex)
    # if bigramIndex:
    #    saveIndex("bigram index" + str(counter) + ".json", bigramIndex)
    # if trigramIndex:
    #    saveIndex("trigram index" + str(counter) + ".json", trigramIndex)

    # Also save the ID-URL mappings
    with open('id to URL.json', 'w') as f:
        json.dump(idToURL, f)

    # Merge each type of index separately
    mergeIndex(counter, 'unigram')
    # mergeIndex(counter, 'bigram')
    # mergeIndex(counter, 'trigram')


def mergeIndex(counter, path):
    print("Merging " + path)

    common = {}
    finalIndexes = {name: {} for name in (list(string.ascii_lowercase) + ['number', 'non_alphanumeric'])}

    # Iterate over all the indices
    for i in range(1, counter + 1):
        # Open the index file
        with open(path + " index" + str(i) + ".json", 'r') as f:
            # Load the index as JSON
            temp = json.load(f)
            # Merge the index with the final index
            for token, posting in temp.items():
                sum = 0
                # Caching the popular terms in memory
                for x in posting:
                    sum += x[1]
                    if sum > 50:  # 50 has 10k, 80 has 7.6k, 100 has 1k
                        common[token] = posting
                        break

                if token[0] in alpha:
                    # Assign it to one of the alphabetic dictionaries
                    index_dict = finalIndexes[token[0]]
                elif token[0].isdigit():
                    # Assign it to the numeric dictionary
                    index_dict = finalIndexes['number']
                else:
                    # Assign it to the non-alphanumeric dictionary
                    index_dict = finalIndexes['non_alphanumeric']

                if token not in index_dict:
                    index_dict[token] = posting
                else:
                    index_dict[token].extend(posting)

    # Print total tokens in each dictionary
    for filename, index_dict in finalIndexes.items():
        print(filename, "# of unique tokens ", len(index_dict))

    print("Cached common words: ", len(common.keys()))

    # Save dictionaries to separate JSON files
    for filename, index_dict in finalIndexes.items():
        with open('final ' + path + ' ' + filename + '.json', 'w') as f:
            json.dump(index_dict, f)

    # Write common words to file
    with open('common.json', 'w') as cw:
        json.dump(common, cw)


def saveIndex(path, index):
    # Open a file at the given path
    with open(path, 'w') as f:
        # Dump the index into the file as JSON
        json.dump(dict(sorted(index.items())), f)


if __name__ == "__main__":
    """
    nltk.download('punkt')
    # Define the path where the documents are stored
    path = "\\Users\\tommy\\Desktop\\CS121-main\\DEV"
    # Read the files from the provided path
    docs = readFiles(path)
    print("Indexing")
    # Get the index of the documents
    getIndex(docs)
    """
    mergeIndex(3, 'unigram')
