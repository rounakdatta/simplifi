import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
import pickle
from ast import literal_eval
import pandas as pd
import numpy as np



def read_data(filename):
    data = pd.read_csv(filename, sep='\t')
    data['tags'] = data['tags'].apply(literal_eval)
    return data



train = read_data('data/train.tsv')
validation = read_data('data/validation.tsv')



X_train, y_train = train['title'].values, train['tags'].values
y_val = validation['title'].values


print("Test1..........")


import re


REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def text_prepare(text):

    text = text.lower()# lowercase text
    text = re.sub(REPLACE_BY_SPACE_RE," ",text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(BAD_SYMBOLS_RE,"",text)# delete symbols which are in BAD_SYMBOLS_RE from text
    text = " ".join([s for s in text.split(" ") if s not in STOPWORDS])# delete stopwords from text
    return text



# Now we can preprocess the titles using function *text_prepare* and  making sure that the headers don't have bad symbols:



X_train = [text_prepare(x) for x in X_train]


print("Test2..........")



from nltk.tokenize.treebank import TreebankWordTokenizer
twd = TreebankWordTokenizer()
twd.tokenize(X_train[0])



# Dictionary of all tags from train corpus with their counts.
tags_counts = {}
# Dictionary of all words from train corpus with their counts.
words_counts = {}

from collections import Counter

with open("tags.txt", "rb") as fp:
    all_tags = pickle.load(fp)

with open("vocab.txt", "rb") as fp:
    vocabulary = pickle.load(fp)


tags_counts = Counter(all_tags)
words_counts = Counter(vocabulary)

import operator

TOP_WORDS=sorted_d = sorted(words_counts.items(), key=operator.itemgetter(1),reverse=True)[:5000]


print("Test3..........")


import operator
DICT_SIZE = 5000
ALL_WORDS =[i for i,j in sorted(words_counts.items(), key=operator.itemgetter(1),reverse=True)[:5000]]

WORDS_TO_INDEX = {}
for count, word in enumerate(ALL_WORDS):
    WORDS_TO_INDEX.update({word:count})
    
INDEX_TO_WORDS = dict((v,k) for k,v in WORDS_TO_INDEX.items())
#ALL_WORDS = WORDS_TO_INDEX.keys()

def my_bag_of_words(text, words_to_index, dict_size):

    result_vector = np.zeros(dict_size)
    
    for word in text.split():
        if word in words_to_index.keys():
            x= words_to_index[word]
            result_vector[x]=1
    return result_vector


print("Test4..........")

from scipy import sparse as sp_sparse

X_test = ['Unable to install flask in windows', 'Error in numpy array']

X_test_mybag = sp_sparse.vstack([sp_sparse.csr_matrix(my_bag_of_words(text, WORDS_TO_INDEX, DICT_SIZE)) for text in X_test])




print("Test5..........")




from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer(classes=sorted(tags_counts.keys()))
y_train = mlb.fit_transform(y_train)
y_val = mlb.fit_transform(y_val)


with open("model.pkl", "rb") as fp:
    classifier_mybag = pickle.load(fp)

print("Test6..........")

y_val_predicted_labels_mybag = classifier_mybag.predict(X_test_mybag)


y_val_pred_inversed = mlb.inverse_transform(y_val_predicted_labels_mybag)
y_val_inversed = mlb.inverse_transform(y_val)
for i in range(len(X_test)):
    print('Title:\t{}\nPredicted labels:\t{}\n\n'.format(
        X_test[i],
        ','.join(y_val_pred_inversed[i])
    ))