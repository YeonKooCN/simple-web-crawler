import pickle
import time
import sys
import os
import json


class searchDriver:

    """
    The next two lines of code are from Project 2 corpus.py
    """
    WEBPAGES_RAW_NAME = "WEBPAGES_RAW"
    JSON_FILE_NAME = os.path.join(".", WEBPAGES_RAW_NAME, "bookkeeping.json")

    def __init__(self):
        self.query = ""
        self.database = {}
        # Next line of code's from Project 2 corpus.py
        self.file_url_map = json.load(open(self.JSON_FILE_NAME), encoding="utf-8")


    def loadPickle(self):
        """
        This method opens local index file and loads it to self.database
        """
        t0 = time.time()
        print ("Loading pickle file....................")
        with open("index.pickle",'rb') as handle:
            self.database = pickle.load(handle)
        print ("Time to load pickle: ", time.time() - t0, "seconds.")
        # print(self.database)


    def startEngine(self):
        """
        This method initiates the search egnine
        """
        searchTerm = ""
        print("------------------------------------------------------")
        print("Initiating Search Engine..............")
        self.loadPickle()
        self.searchQuery()


    # Prompt user to enter search query
    def searchQuery(self):
        """
        This method prompts user to enter search query. The query can only be one word
        for the purpose of simplicity.
        """
        while True:
            print ("Please enter a search query:")
            print ("Enter number '0' to exit the program")
            searchTerm = str(input())
            # Convert all letters in the search term to lower case
            self.query = searchTerm.lower()
            print ("You have entered the word:", self.query)
            # Call one_word_query method to print search results
            self.one_word_query()
            print ("******************************************************")
            # Exception Handling: Throw exception if length of the query is more than one word
            if len(self.query.split()) > 1:
                print ("Exception: words in search query is more than one.")
            # Terminate program if user enters "0"
            elif self.query == "0":
                print ("Program shutting down... Have a good day!")
                print("------------------------------------------------------")
                sys.exit(0)


    def one_word_query(self):
        """
        This method takes in the one-word query user has eentered and print the first 20 search results
        """
        t0 = time.time()
        query = self.query
        s_map = self.file_url_map
        db = self.database
        count = 0
        var = 1

        if query in self.database.keys():
            print ("Searching results for the word:", query, ".........")
            print ("Only showing the first 20 URLs")
            # Count total number of search results
            for value in db[query]:
                count += 1
            
            for value in db[query]:
                # print the URL corresponding to the DocID
                print ("[", var, "]", s_map[value])
                # Return only 20 results
                var = var + 1
                if var > 20:
                    break

            print ("Search Completed.")
            print ("Total number of results: ", count)
            print ("Time to search:", (time.time() - t0), "seconds")

        else:
            print ("Unable to find results for this word.")



if __name__ == "__main__":
    driver = searchDriver()
    driver.startEngine()
