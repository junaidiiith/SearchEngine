from file_lister import recursive_list_files
import os,sys
import pickle, json
from nltk import corpus
from nltk import stem
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction import DictVectorizer
from collections import Counter, OrderedDict
stop_words = set(corpus.stopwords.words('english'))


def stemwords(words,stemmer=None):
	if not stemmer:
		stemmer = stem.SnowballStemmer('english')
	stemmed_word = list()
	for i in range(len(words)):
		words[i] = stemmer.stem(words[i])

	return words
		

def tokenize(text,tokenizer=None):
	if not tokenizer:
		tokenizer = RegexpTokenizer(r'\w+')
	return tokenizer.tokenize(text)

def create_indices(files):
	indices_dict = dict()
	inv = dict()
	v = DictVectorizer()
	word_tuples = list()
	for f in files:
		inv[files.index(f)] = f
		words = stemwords(tokenize(open(f).read()))
		word_tuples.append(tuple(words))
		for i in range(len(words)):
			if words[i] not in stop_words:
				try:
					if files.index(f) not in indices_dict[words[i]]['doc_ids']:
						indices_dict[words[i]]['occurances'] += 1
					try:
						indices_dict[words[i]]['doc_ids'][files.index(f)].append(i)
					except:
						indices_dict[words[i]]['doc_ids'][files.index(f)] = [i]
				except:
					indices_dict[words[i]] = dict()
					indices_dict[words[i]]['occurances'] = 1
					indices_dict[words[i]]['doc_ids'] = dict()
					indices_dict[words[i]]['doc_ids'][files.index(f)] = [i]

	vectors = v.fit_transform(Counter(f) for f in tuple(word_tuples))
	vector_models = dict()
	vector_models['vectors'] = vectors
	vector_models['words'] = v.vocabulary_
	return indices_dict,vector_models,len(files),inv

def form_indices_from_directory(directory):
	cwd = os.getcwd()
	directory = sys.argv[1]
	datafiles = list()
	if directory[0] in ['/','~']:
		datafiles = recursive_list_files(directory,['.dat','.txt'])
	else:
		datafiles = recursive_list_files(cwd+'/'+directory,['.dat','.txt'])

	return create_indices(datafiles)

if __name__ == '__main__':
	location = input("Enter the custom corpus location (Default ./data)")
	indices,inv = dict(),dict()
	data = dict()
	if not location:
		indices,vector_models,docs,inv = form_indices_from_directory(location)
		data['word vectors'] = vector_models
	else:
		indices,vector_models,docs,inv = form_indices_from_directory("./data")
		data['word vectors'] = vector_models

	
	data['indices'] = indices
	data['total docs'] = docs
	data['inv'] = inv
	with open('corpus.p','wb') as fp:
		pickle.dump(data,fp,protocol=pickle.HIGHEST_PROTOCOL)