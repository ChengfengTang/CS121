import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser  # this is needed to open the URL in a web browser
from M1 import getIndex, readFiles, mergeIndex
from M2 import SearchEngine

class SearchApp:
    def __init__(self, root):
        self.root = root  # The root widget (window) of the application
        self.searchEngine = None  # Initialize the search engine object as None

        # Create the 'Index' button
        self.indexButton = tk.Button(root, text='Index', command=self.index)
        self.indexButton.pack()

        # Create a field for input query
        self.searchField = tk.Entry(root)
        self.searchField.pack()

        # Create the 'Search' button
        self.searchButton = tk.Button(root, text='Search', command=self.search)
        self.searchButton.pack()

        # Create a text field for results
        self.results = tk.Text(root)
        self.results.pack()

    def callback(self, url):
        webbrowser.open_new(url)

    # Define the function to index documents
    def index(self):
        # Open a dialog to choose a directory
        path = filedialog.askdirectory()
        if path:  # If a directory was selected
            # If the common.json file doesn't already exist, start indexing
            if not os.path.exists('common.json'):
                # Read the files from the selected path
                docs = readFiles(path)
                print("Indexing")
                # Get the index of the documents
                getIndex(docs)
                # Call MergeIndex to merge and split
                mergeIndex(3, 'unigram')
                # Inform the user that indexing is complete
                messagebox.showinfo('Info', 'Indexing completed')
            else:  # If common.json already exists, notify the user
                messagebox.showinfo('Info', 'Inverted Index already exists, no need to index again.')
            # Initialize the SearchEngine
            self.searchEngine = SearchEngine()
        else:  # If no directory was selected, notify the user
            messagebox.showinfo('Info', 'No directory selected')

    def search(self):
        # If the SearchEngine has not been initialized, ask the user to index first
        if self.searchEngine is None:
            messagebox.showinfo('Info', 'Please index first')
            return

        # Get the query from the search field
        query = self.searchField.get()
        # Start a timer
        start = time.time()
        # Perform the search
        results = self.searchEngine.search(query)
        # End the timer
        end = time.time()
        # Clear the results field
        self.results.delete(1.0, tk.END)
        # Print the search time to the results field
        self.results.insert(tk.END, "Time taken: " + str((end - start) * 1000) + " ms \n")
        # Print the top 5 results to the results field
        self.results.insert(tk.END, 'Top 5 results:\n')
        for i, (url, score) in enumerate(results):
            # Add the url as a hyperlink in the Text widget
            hyperlink = f'URL: {url}, Score: {score}\n'
            self.results.insert(tk.END, hyperlink)
            self.results.insert(tk.END, "\n\n")  # Adds two newline characters after each link
            tag = "link"+str(i)
            self.results.tag_add(tag, "end - 4 lines linestart", "end - 4 lines lineend")
            self.results.tag_config(tag, foreground="blue", underline=1)
            # Bind the link with correct url by passing url to lambda function
            self.results.tag_bind(tag, "<Button-1>", lambda e, url=url: self.callback(url))
            # Change cursor when hovering over the link
            self.results.tag_bind(tag, "<Enter>", lambda e: self.results.config(cursor="hand2"))
            self.results.tag_bind(tag, "<Leave>", lambda e: self.results.config(cursor=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
