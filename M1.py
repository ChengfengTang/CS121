import os
import json
import shelve

import nltk
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict


def readFiles(path):
    docs = {}
    for domain in os.listdir(path):
        domainFolder = os.path.join(path, domain)
        if os.path.isdir(domainFolder):
            for page in os.listdir(domainFolder):
                file_path = os.path.join(domainFolder, page)
                with open(file_path, 'r') as f:
                    temp = json.load(f)
                    docs[temp['url']] = temp['content']
            print("ok", len(docs))
    return docs


def tokenize(content):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    tokens = nltk.word_tokenize(text)

    # Create a PorterStemmer object
    stemmer = PorterStemmer()
    # Stem tokens
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens


def getIndex(documents):
    index = defaultdict(list)
    counter = 1
    doc_counter = 0
    for url, text in documents.items():
        tokens = tokenize(text)
        temp = nltk.FreqDist(tokens)
        for token, frequency in temp.items():
            index[token].append([url, frequency])

        doc_counter += 1
        if doc_counter >= 1000:
            saveIndex("inverted index" + str(counter) + ".json", index)
            index.clear()
            doc_counter = 0
            counter += 1

        print("ok ", counter, len(index))

    if index:  # Save the last partial index if it exists
        saveIndex("inverted index" + str(counter) + ".json", index)

    mergeIndex(counter)


def mergeIndex(counter):
    # Shelve doesn't hold data in memory.
    with shelve.open('final index') as finalIndex:
        for i in range(1, counter + 1):
            with open("inverted index" + str(i) + ".json", 'r') as f:
                temp = json.load(f)
                for token, posting in temp.items():
                    if token not in finalIndex:
                        finalIndex[token] = posting
                    else:
                        finalIndex[token].extend(posting)


def saveIndex(path, index):
    #  https://www.geeksforgeeks.org/json-dump-in-python/
    with open(path, 'w') as f:
        json.dump(index, f)


if __name__ == "__main__":
    path = "/Users/chengfeng/Desktop/ANALYST"
    docs = readFiles(path)
    print("Indexing")
    index = getIndex(docs)
    #   print("# of documents: " , len(docs))
    # print("# of unique tokens: " , len(index))
    # print("Total size of index on disk: " , os.path.getsize("inverted_index.json") / 1024) # in KB
