import os
import time
import tkinter as tk
from tkinter import messagebox
from M1 import getIndex, readFiles, mergeIndex
from M2 import SearchEngine


class SearchApp:
    def __init__(self, root):
        self.root = root
        self.searchEngine = None

        self.indexButton = tk.Button(root, text='Index', command=self.index)
        self.indexButton.pack()

        self.searchField = tk.Entry(root)
        self.searchField.pack()

        self.searchButton = tk.Button(root, text='Search', command=self.search)
        self.searchButton.pack()

        self.results = tk.Text(root)
        self.results.pack()

    def index(self):
        if not (os.path.exists('common.json')):
            path = "\\Users\\tommy\\Desktop\\CS121-main\\ANALYST"
            # Read the files from the provided path
            docs = readFiles(path)
            print("Indexing")
            # Get the index of the documents
            getIndex(docs)
            mergeIndex(3, 'unigram')
            messagebox.showinfo('Info', 'Indexing completed')

        else:
            messagebox.showinfo('Info', 'Inverted Index already exists, no need to index again.')
        self.searchEngine = SearchEngine()

    def search(self):
        if self.searchEngine is None:
            messagebox.showinfo('Info', 'Please index first')
            return

        query = self.searchField.get()
        start = time.time()
        results = self.searchEngine.search(query)
        end = time.time()
        self.results.delete(1.0, tk.END)  # clear screen before displaying
        self.results.insert(tk.END,
                            "Time taken: " + str((end - start) * 1000) + " ms \n")
        self.results.insert(tk.END, 'Top 5 results:\n')
        for url, score in results:
            self.results.insert(tk.END, f'URL: {url}, Score: {score}\n')


if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
