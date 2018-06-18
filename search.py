from nltk.tokenize import RegexpTokenizer
import math
import os
import pickle
from nltk import stem
import numpy as np


tokenizer = RegexpTokenizer(r'\w+')
stemmer = stem.SnowballStemmer('english')


def stemwords(words,stemmer=None):
	if not stemmer:
		stemmer = stem.SnowballStemmer('english')
	stemmed_word = list()
	for i in range(len(words)):
		words[i] = stemmer.stem(words[i])

	return words

def find_docs(query):
	
	words = stemwords(tokenizer.tokenize(query))
	docs = set()
	for word in words:
		print("Finding word",word)
		try:
			doc = set(indices[word]['doc_ids'].keys())
			docs = docs.union(doc)
		except:
			print("Unalbel to find")
			continue
		print(docs)
	return docs

def free_text_queries(query):
	docs = find_docs(query)
	docs = rank_docs(docs,query)
	print("Docs found are ",docs)
	return docs

def phrase_queries(query):
	words = stemwords(tokenizer.tokenize(query))
	positional_docs = dict()
	doc_set = set()
	for word in words:
		try:
			positional_docs[word] = dict()
			doc_set.insersection(set(indices[word]['doc_ids'].key()))
			for doc,positions in indices[word].items():
				positional_docs[word][doc] = set([position-words.index(word) for position in positions])
		except:
			return None

	if not doc_set:
		return None

	result = list()

	for ds in doc_set:
		intersect = positional_docs[word][ds]
		for word in words[1:]:
			intersect.insersection(positional_docs[word][ds])
			if not intersect:
				break

		if intersect:
			result.append(ds)
	return rank_docs(result,query)

	
def rank_docs(docs,query):
	scores = list()
	for doc in docs:
		val = 0.0
		words = stemwords(tokenizer.tokenize(query))
		for word in words:
			print("Searching for ", word, " in ", doc)
			print(type(document_vectors[doc]))
			print(document_vectors[doc].shape)
			tf = document_vectors[doc][vocab[word]]/(np.linalg.norm(document_vectors[doc]))
			df = indices[word]['occurances']
			td = total_docs
			val += tf*math.log(total_docs/df)
		
		scores.append((val,doc))
	scores.sort(reverse=True)	
	print(scores)
	return [score[1] for score in scores]


def print_docs(docs,query):
	for doc in docs:
		f = inverse_file_names[doc]
		command = "grep -o '"+query+"' "+f
		print(command)
		print(os.system(command))


if __name__ == '__main__':

	data = dict()
	with open('corpus.p','rb') as fp:
		data = pickle.load(fp)

	indices = data['indices']
	document_vectors = data['word vectors']['vectors'].A
	vocab = data['word vectors']['words']
	total_docs = data['total docs']
	inverse_file_names = data['inv']
	query = input("Enter your search query: ")
	docs = free_text_queries(query)
	print_docs(docs,query)