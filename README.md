# CS121 Spring 2023 

# How to operate the application
## Prerequisites
Ensure that you have installed all necessary packages including nltk, bs4, simhash, and tkinter.
```python
pip install nltk bs4 simhash tkinter
```
Next, download the NLTK tokenizer by running the following Python command:
```python
nltk.download('punkt')
```
Finally, you must have your dataset (a collection of files you want to index) stored on your local machine)

## Start the program
```python
python3 M3.py
```

## Indexer
Click the "Index" button in the GUI to select a directory. The program will then read the files in the provided path, create the index, and store it on disk. If the index already exists, the program will notify you. Indexing may take a while depending on the size of the dataset. The indexing status will be displayed in the console.

## Search
With the application running, enter your query in the text field in the GUI.

Click the "Search" button.

The search engine will retrieve and display the top five most relevant results in the GUI interface based on your query. The results are ranked using the TF-IDF score. The time taken for the search will also be displayed.


# Features
## Indexer
The Indexer reads a collection of documents, processes them, and creates an inverted index. The features of the indexer include:

• Creation of tokens for all alphanumeric sequences in the dataset.

• No stop words are removed during indexing.

• Porter stemming is applied to tokens for better textual matches.

• TF-IDF scores are calculated for each document.

• Index offloading: The inverted index hashmap is offloaded from main memory to a partial index on disk at least 3 times during index construction. These partial indexes are merged in the end.

Important text (in bold, in headings, and in titles) is treated as more important.

• Words that appear more than 50 times are treated as common words, stored under "common.json".

## Search Engine
• The Search Engine utilizes the inverted index to retrieve relevant documents based on a query. The features of the search engine include:

• Boolean Retrieval: The search engine can handle boolean queries with AND operations.

• TF-IDF Scoring: The search results are sorted based on their TF-IDF scores.

• Positional Indexing: The search engine takes into account the positions of the query tokens in the documents.


# Extra Credit
Extra percentual credit1 will be given for tasks that improve the retrieval and
the user search - except for the GUI, you must code from scratch. For example:

• Detect and eliminate duplicate pages. (1 pt for exact, 2 pts for near) ☑️

• Add HITS and Page Rank to ranking. (1.5 pts HITS, 2.5 for PR) 

• Implement 2-gram and 3-gram indexing and use it in retrieval. (1 pt) 

• Enhance the index with word positions and use them for retrieval. (2 pts) ☑️

• Index anchor words for the target pages. (1 pt). ☑️

• Implement a Web or local GUI interface instead of using the console.
(1 pt for the local GUI, 2 pts for a web GUI) ☑️
