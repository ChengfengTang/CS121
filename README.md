# CS121
CS121 Spring 2023

Indexer

Create an inverted index for the corpus with data structures designed by you.

The inverted index is simply a map with the token

• Its tf-idf score for that document

• Tokens: all alphanumeric sequences in the dataset. ☑️

• Stop words: do not use stopping while indexing, i.e. use all words, even
the frequently occurring ones. ☑️

• Stemming: use stemming for better textual matches. Suggestion: Porter
stemming, but it is up to you to choose. ☑️

• Important text: text in bold (b, strong), in headings (h1, h2, h3), and
in titles should be treated as more important than the in other places.
Verify which are the relevant HTML tags to select the important words
Your indexer must off load the inverted

• index hash map from main memory to a partial index on disk at least 3 times
during index construction; those partial indexes should be merged in the end.
Optionally, after or during merging, they can also be split into separate index
files with term ranges. Similarly, your search component must not load the
entire inverted index in main memory. Instead, it must read the postings from
the index(es) files on disk. ☑️



Extra Credit
Extra percentual credit1 will be given for tasks that improve the retrieval and
the user search - except for the GUI, you must code from scratch. For example:
• Detect and eliminate duplicate pages. (1 pt for exact, 2 pts for near)
• Add HITS and Page Rank to ranking. (1.5 pts HITS, 2.5 for PR)
• Implement 2-gram and 3-gram indexing and use it in retrieval. (1 pt)
• Enhance the index with word positions and use them for retrieval. (2 pts)
• Index anchor words for the target pages. (1 pt).
• Implement a Web or local GUI interface instead of using the console.
(1 pt for the local GUI, 2 pts for a web GUI)
