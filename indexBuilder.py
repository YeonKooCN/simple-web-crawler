import json
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk import word_tokenize
import time
import io
import pickle
import math
import re


class indexBuilder:

    def __init__(self, json_file_name):
        self.json_file = json_file_name
        self.folder_list = []
        self.docID = []
        self.corpusCount = 0
        self.count = 0


    def readJSON(self):
        """
        Reads JSON file to iterate through WEBPAGES_RAW
        """
        with open(self.json_file) as data_file:
            try:
                data = json.load(data_file)
            except ValueError:
                data = {}
        for d in data:
            # Total size
            self.corpusCount = self.corpusCount + 1
            # List of all the folders saved as paths
            self.folder_list.append("WEBPAGES_RAW/" + d)
            # Extracting just the docIDs
            self.docID.append(d)


    def tokenizeFile(self, folder_path):
        """
        This method tokenizes all the files in WEBPAGES_RAW.
        Add each unique word in a dictionary, and corresponding DocIDs as values for a unique word
        Add a placeholder for each DocID for storing tf-idf etc.
        """
        t0 = time.time()
        tokenizer = RegexpTokenizer(r'\w+')
        wordsdict = {}
        word_position = 0
        # Exception Handling: Error checking each file
        try:
            doc = io.open(folder_path, 'r', encoding='utf-8')
        except ValueError:
            return wordsdict
        # Read in local webpage files and store as data
        data = doc.read().encode('utf-8')
        doc.close()
        # Prase the webpages using BeautifulSoup
        soup = BeautifulSoup(data, 'html.parser')
        # Strip out unnecessary information
        [s.extract() for s in soup(['style', 'script', '[document]'])]
        # Only take in words inside these tags
        for tag in ['b', 'h1', 'h2', 'h3', 'title', 'body', 'strong']:
            # For each tag use find_all to get the text
            for text in soup.find_all(tag):
                # Get the text and throw out anything that isn't a letter
                text = text.getText()
                text = re.sub(r'[^a-zA-Z1-9]', " ", text)
                # Tokenize text using Regexp Tokenizer
                text_r = tokenizer.tokenize(text)
                # Convert all tokens to lower case
                text_l = [w.lower() for w in text_r]
                # Each word is added to the words dict
                for word in text_l:
                    if word in wordsdict.keys():
                        wordsdict[word]
                    # Create a new word in the words dict when there is no occurence
                    else:
                        wordsdict[word] = []
        self.count += 1
        print ("Count: ", self.count)
        print ("Folder: ", folder_path)
        return wordsdict


    def postingsList(self):
        """
        Create an index of pages listed by docID containing a listing of all their terms
        This method will later be called when building inverted index.
        """
        pages = {}
        for i in range(len(self.folder_list)):
            pages[self.docID[i]] = self.tokenizeFile(self.folder_list[i])
            
        return pages


    def buildInvertedIndex(self):
        """
        Now that we have index setup as file_name -> word, we need to invert the index
        to word -> file_name
        """
        pages = self.postingsList()
        invertedIndex = {}
        count = 0
        # Go through every page
        for file_name in pages.keys():
            count += 1
            for word in pages[file_name].keys():
                if word in invertedIndex.keys():
                    invertedIndex[word][file_name] = pages[file_name][word]
                else:
                    invertedIndex[word] = {}
                    invertedIndex[word][file_name] = pages[file_name][word]

        return invertedIndex


    def writeToFile(self, target):
        """
        The method is for writing pickle file to be store on local subdirectory
        """
        print ("Writing to file................")
        with open('index.pickle', 'wb') as handle:
            pickle.dump(target, handle)
        print ("Wrtiting to file completed!")
        print ("Index file name: 'index.pickle'. The file can be found under the subdirectory.")

    def getNumber(self):
        return self.corpusCount

if __name__ == "__main__":
    total_t0 = time.time()
    index = indexBuilder("bookkeeping.json")
    index.readJSON()
    invertedIndex = index.buildInvertedIndex()
    print ("-------------------------------------------------------------------------")
    print ("Size of index (unique words): ", len(invertedIndex))
    index.writeToFile(invertedIndex)
    number_of_file = index.getNumber()
    print ("Total running time: ", (time.time() - total_t0), "seconds")
    print("Total number of webpages processed:", number_of_file)
    print ("-------------------------------------------------------------------------")

