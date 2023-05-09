import os
import json
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
    for url, text in documents.items():
        tokens = tokenize(text)
        # https://www.educative.io/answers/what-is-freqdist-in-python
        temp = nltk.FreqDist(tokens)
        for token, frequency in temp.items():
            index[token].append([url, frequency])
    return index


def saveIndex(index):
    #  https://www.geeksforgeeks.org/json-dump-in-python/
    with open("inverted index.json", 'w') as f:
        json.dump(index, f)

if __name__ == "__main__":
    path = "/Users/chengfeng/Desktop/ANALYST"
    docs = readFiles(path)
    index = getIndex(docs)
    saveIndex(index)
    print("# of documents: " , len(docs))
    print("# of unique tokens: " , len(index))
    print("Total size of index on disk: " , os.path.getsize("inverted_index.json") / 1024) # in KB
