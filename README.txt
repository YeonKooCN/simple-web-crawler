Author:
@YeyangGu 14333845
@JustinLock 71327880

I. File list
------------
indexBuilder.py     Search Engine Index Builder Implementation
searchDriver.py     Search Engine Search Function Implementation
indexReader.py      A simple file to quickly open index stored in index.pickle
index.pickle        Pickle file containing index
bookkeeping.json        URL/file map that comes with WEBPAGES_RAW
Outputs                 This folder contain sample outputs
README                  This file



In order to run the program successfully, make sure WEBPAGES_RAW is in the main directory.



II. Design
----------
A. Program design

1. Style
The code covers building an index and a basic retrieval component. By basic retrieval component; we mean that at this point you just need to be able to query your index for links (The query can be as simple as single word at this point).
These links do not need to be accurate/ranked. We will cover ranking in the next milestone.

2. Purpose
The purpose of this program is to be able to return results for single-word queries such as "Informatics", "Mondego", and "Irvine".