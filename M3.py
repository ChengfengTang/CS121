import os
import tkinter as tk
from tkinter import messagebox
from M1 import getIndex, readFiles
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
        if not (os.path.exists('final unigram.db') and os.path.exists('final bigram.db') and os.path.exists('final trigram.db')):
            path = "/Users/chengfeng/Desktop/CS121/ANALYST"  # replace with actual path
            docs = readFiles(path)
            getIndex(docs)
            messagebox.showinfo('Info', 'Indexing completed')
            self.searchEngine = SearchEngine()

        else:
            messagebox.showinfo('Info', 'Inverted Index already exists, no need to index again.')

    def search(self):
        if self.search_engine is None:
            messagebox.showinfo('Info', 'Please index first')
            return

        query = self.searchField.get()
        results = self.searchEngine.search(query)
        self.results.delete(1.0, tk.END)
        self.results.insert(tk.END, 'Top 5 results:\n')
        for url, score in results:
            self.results.insert(tk.END, f'URL: {url}, Score: {score}\n')

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
