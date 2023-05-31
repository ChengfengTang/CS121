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

# Download the Punkt Tokenizer Models, this is used for tokenizing text.
nltk.download('punkt')

fingerprints = []
# List of pages to avoid
pagesToAvoid = [r"https://cbcl\.ics\.uci\.edu/public_data/[\w\-./]+",  # Useless texts with junk numbers
                r"http://mondego\.ics\.uci\.edu/datasets/[\w\-./]+",  # can't load
                r"https://www\.ics\.uci\.edu/~kay/[\w\-./]+"]  # too large

alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
         "w", "x", "y", "z"]


# Function to read files from a given path
def readFiles(path):
    # Initialize an empty dictionary to store documents
    docs = {}

    # Iterate over all the files in the provided directory
    for domain in os.listdir(path):
        domainFolder = os.path.join(path, domain)  # Join the path and domain name to create the full path
        if os.path.isdir(domainFolder):  # If the path is a directory

            for page in os.listdir(domainFolder):  # Iterate over all the files in the directory
                # Join the domain folder path and page name to create the full file path
                file_path = os.path.join(domainFolder, page)
                with open(file_path, 'r') as f:  # Open the file
                    temp = json.load(f)  # Load the file content as JSON
                    docs[temp['url']] = temp['content']  # Store the file content to the dictionary
            print("ok", len(docs))  # Print the number of documents
    return docs  # Output the documents


def tokenize(content):
    # Parse the HTML content
    soup = BeautifulSoup(content, 'html.parser')
    # Extract text from the HTML
    text = soup.get_text()
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    # Get important words
    important_words = get_important_words(soup)
    # Create a PorterStemmer object
    stemmer = PorterStemmer()
    # Stem tokens
    tokens = [stemmer.stem(token) for token in tokens if token.isalnum()]
    # Stem important words
    important_words = [stemmer.stem(word) for word in important_words if word.isalnum()]
    # Return the tokens and important words
    return tokens, important_words


def get_important_words(soup):
    # Define a list of important HTML tags
    important_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong']
    # Initialize an empty list to store important words
    important_words = []
    # For each important tag
    for tag in important_tags:
        # Find all the elements with that tag
        elements = soup.findAll(tag)
        for element in elements:
            # Tokenize the text of the element
            words = nltk.word_tokenize(element.get_text())
            # Add the tokens to the list of important words
            important_words.extend(words)

    return important_words


# Function to generate the index of the documents
def getIndex(documents):
    unigramIndex = defaultdict(list)
    idToURL = {}  # dictionary to map IDs to URLs for retrieval
    importantWordsIndex = {}  # Dictionary to map IDs to important words in the document
    counter = 1
    docCounter = 1  # Document counter will now serve as ID
    totalDocs = len(documents)  # Total number of documents

    simhashes = {}  # Dictionary to store Simhashes
    tokenSets = {}  # Dictionary to store sets of tokens

    for url, text in documents.items():
        # Avoid pages using regular expression
        if any(re.search(pattern, url) for pattern in pagesToAvoid):
            print(text)
            continue
        print(url)
        idToURL[docCounter] = url  # Map the URL with its ID
        tokens, important_words = tokenize(text)
        importantWordsIndex[docCounter] = important_words  #  Map the ID with its important words
        temp1 = nltk.FreqDist(tokens)

        # Compute and store the Simhash for this document
        tempSimHash = Simhash(tokens)
        for ids in range(1, docCounter):

            # Compute the Hamming distance between the Simhashes of these two documents
            distance = simhashes[ids].distance(tempSimHash)

            # If the distance is small, the documents are similar
            if distance < 2:
                print(f"Documents {ids} and {docCounter} are similar (Simhash distance = {distance})")
                break
                continue

            # Compute the Jaccard similarity between the sets of tokens for these two documents
            jaccardSimilarity = len(tokenSets[ids] & set(tokens)) / len(tokenSets[ids] | set(tokens))

            # If the Jaccard similarity is close to 1, the documents are very similar or identical
            if jaccardSimilarity > 0.9:  # 0.9 is just an example threshold
                print(
                    f"Documents {ids} and {docCounter} are identical or very similar (Jaccard similarity = {jaccardSimilarity})")
                break
                continue

        simhashes[docCounter] = tempSimHash
        # Store the set of tokens for this document
        tokenSets[docCounter] = set(tokens)

        # Indexing unigrams
        for token, frequency in temp1.items():
            positions = [i for i, t in enumerate(tokens) if t == token]  # Find positions of the token
            idf = math.log(totalDocs / len(unigramIndex[token])) if unigramIndex[token] else 0  # Calculate IDF
            tf_idf = frequency * idf  # Calculate TF-IDF
            unigramIndex[token].append([docCounter, frequency, positions, tf_idf])

        docCounter += 1
        if docCounter % (len(documents) // 3) == 0:  # Now we save every 1/3
            saveIndex("unigram index" + str(counter) + ".json", unigramIndex)
            unigramIndex.clear()
            counter += 1
        print("ok ", docCounter, counter, len(unigramIndex))

    if unigramIndex:  # Save the last partial index if it exists
        saveIndex("unigram index" + str(counter) + ".json", unigramIndex)

    # Also save the ID-URL mappings
    with open('id to URL.json', 'w') as f:
        json.dump(idToURL, f)

    # Save the important words dictionary
    with open('important_words.json', 'w') as f:
        json.dump(importantWordsIndex, f)

    # Merge each type of index separately
    mergeIndex(counter, 'unigram')

#  Function to merge indices
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

# Function to save the index to a file
def saveIndex(path, index):
    # Open a file at the given path
    with open(path, 'w') as f:
        # Dump the index into the file as JSON
        json.dump(dict(sorted(index.items())), f)

# Test function
if __name__ == "__main__":
    # Define the path where the documents are stored

    path = "\\Users\\tommy\\Desktop\\CS121-main\\DEV"
    # Read the files from the provided path
    docs = readFiles(path)
    print("Indexing")
    # Get the index of the documents
    getIndex(docs)

    # mergeIndex(3, 'unigram')
