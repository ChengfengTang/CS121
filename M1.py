import os
import json
import shelve

import nltk
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from collections import defaultdict


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
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Create a PorterStemmer object
    stemmer = PorterStemmer()
    # Stem tokens
    tokens = [stemmer.stem(token) for token in tokens]
    # Return the tokens
    return tokens


def getIndex(documents):
    # Create a default dictionary to store the index
    index = defaultdict(list)
    # Initialize counters
    counter = 1
    doc_counter = 0
    # Iterate over all the documents
    for url, text in documents.items():
        # Tokenize the text
        tokens = tokenize(text)
        # Get the frequency distribution of the tokens
        temp = nltk.FreqDist(tokens)
        # Add the tokens and their frequencies to the index
        for token, frequency in temp.items():
            index[token].append([url, frequency])

        # Increase the document counter
        doc_counter += 1
        # If we have processed 1000 documents, save and clear the index
        if doc_counter >= 1000:
            saveIndex("inverted index" + str(counter) + ".json", index)
            index.clear()
            doc_counter = 0
            counter += 1

        # Print the current state
        print("ok ", counter, len(index))

    # Save the last partial index if it exists
    if index:
        saveIndex("inverted index" + str(counter) + ".json", index)

    # Merge all the indices
    mergeIndex(counter)


def mergeIndex(counter):
    # Use shelve to store the final index on disk
    with shelve.open('final index') as finalIndex:
        # Iterate over all the indices
        for i in range(1, counter + 1):
            # Open the index file
            with open("inverted index" + str(i) + ".json", 'r') as f:
                # Load the index as JSON
                temp = json.load(f)
                # Merge the index with the final index
                for token, posting in temp.items():
                    if token not in finalIndex:
                        finalIndex[token] = posting
                    else:
                        finalIndex[token].extend(posting)


def saveIndex(path, index):
    # Open a file at the given path
    with open(path, 'w') as f:
        # Dump the index into the file as JSON
        json.dump(index, f)


if __name__ == "__main__":
    # Define the path where the documents are stored
    path = "/Users/chengfeng/Desktop/CS121/ANALYST"
    # Read the files from the provided path
    docs = readFiles(path)
    print("Indexing")
    # Get the index of the documents
    getIndex(docs)
    #   print("# of documents: " , len(docs))
    # print("# of unique tokens: " , len(index))
    # print("Total size of index on disk: " , os.path.getsize("inverted_index.json") / 1024) # in KB
