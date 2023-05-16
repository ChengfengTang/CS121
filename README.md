# CS121
CS121 Spring 2023


Indexer

Create an inverted index for the corpus with data structures designed by you.

The inverted index is simply a map with the token

• Its tf-idf score for that document ☑

• Tokens: all alphanumeric sequences in the dataset. ☑️

• Stop words: do not use stopping while indexing, i.e. use all words, even
the frequently occurring ones. ☑️

• Stemming: use stemming for better textual matches. Suggestion: Porter
stemming, but it is up to you to choose. ☑️

• Important text: text in bold (b, strong), in headings (h1, h2, h3), and
in titles should be treated as more important than the in other places.
Verify which are the relevant HTML tags to select the important words


• Your indexer must off load the inverted index hash map from main memory to a 
partial index on disk at least 3 times during index construction; those partial indexes should be merged in the end.
Optionally, after or during merging, they can also be split into separate index
files with term ranges. Similarly, your search component must not load the
entire inverted index in main memory. Instead, it must read the postings from
the index(es) files on disk. ☑️


Search Engine

The Search Engine is a powerful retrieval tool built upon the inverted index. The search engine utilizes a variety of techniques and features to ensure relevant and accurate results.

Features
Boolean Retrieval: The search engine is capable of handling boolean queries with AND operations. It retrieves documents that contain all the tokens specified in the query.

TF-IDF Scoring: The search results are sorted based on their TF-IDF scores. This ensures that the most relevant documents, i.e., those with a higher frequency of the query tokens, are returned first.

Positional Indexing: The search engine takes into account the positions of the query tokens in the documents. It not only checks if a document contains the tokens but also if the tokens appear in the same order as in the query. This enhances the accuracy of the search results.

Bigrams and Trigrams: The search engine goes beyond unigram tokens and also includes bigrams and trigrams in its indexing and searching. This feature allows it to handle multi-word queries more effectively.

Future Implementations
Other Boolean Operators: In the future, the search engine will be enhanced to handle other boolean operations such as OR and NOT.

Phrase Queries: The search engine will be updated to support phrase queries, where a document is considered a match only if it contains the exact phrase specified in the query.

Relevance Feedback: The search engine will implement relevance feedback mechanisms, such as Rocchio's algorithm, to refine the search results based on user feedback.

Query Expansion: The search engine will use techniques like synonyms and stemming to expand the query, thereby retrieving more relevant documents.

Spell Check and Auto Suggestion: The search engine will provide spell check and auto-suggestion features to assist users in formulating their queries.




Extra Credit
Extra percentual credit1 will be given for tasks that improve the retrieval and
the user search - except for the GUI, you must code from scratch. For example:

• Detect and eliminate duplicate pages. (1 pt for exact, 2 pts for near)

• Add HITS and Page Rank to ranking. (1.5 pts HITS, 2.5 for PR)

• Implement 2-gram and 3-gram indexing and use it in retrieval. (1 pt) ☑

• Enhance the index with word positions and use them for retrieval. (2 pts) ☑

• Index anchor words for the target pages. (1 pt).

• Implement a Web or local GUI interface instead of using the console.
(1 pt for the local GUI, 2 pts for a web GUI)
