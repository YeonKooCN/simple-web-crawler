import pickle

pickle_in = open("index.pickle", "rb")
index = pickle.load(pickle_in)

print(index)