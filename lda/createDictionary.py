# -*- coding: utf-8 -*-
'''
Created on Thu May 8 20:46:22 2014

Creating a dictionary

@author: Niels Bantilan
'''


from gensim import corpora
from nltk.corpus import stopwords
import re
import os
import sys

#define the stoplist
stopList = stopwords.words()


def preprocess(filePath):
    documents = list()
    fileNames = os.listdir(filePath)

    #preprocesses documents in the specified directory to remove punctuation
    for f in fileNames:
        with open('%s/%s' % (filePath, f)) as document:
            text = list()
            for line in document.readlines():
                removePunct = re.sub(r'\[.*?\]|\(.*?\)|\W', ' ', line.strip())
                removeNum = re.sub(r'[0-9]', ' ', removePunct)
                cleanSpace = re.sub(r'\s+', ' ', removeNum)
                text.append(cleanSpace.strip())
        documents.append(' '.join(text))

    with open('%s/%s' % ('../corpus', 'mediumData.txt'), 'w') as docs:
        docs.write('\n'.join(documents))

    return documents


def createDictionary(filePath, fileName):

    with open('%s/%s' % ('../corpus', fileName)) as document:
        dictionary = corpora.Dictionary(line.lower().split()
                                        for line in document.readlines())

    #retrieves the ids of stopwords
    stop_ids = [dictionary.token2id[stopword] for stopword in stopwords.words()
                if stopword in dictionary.token2id]

    #retreives the ids of words with a frequency of 1
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems()
                if docfreq == 1]

    #filters out stopwords and tokens that appear only once
    dictionary.filter_tokens(stop_ids + once_ids)

    #remove gaps in id sequence after words that were removed
    dictionary.compactify()
    dictionary.save('%s/%s' % ('../corpus', 'mediumData.dict'))
    return dictionary


if __name__ == "__main__":
    filePath = sys.argv[1]
    try:
        fileName = sys.argv[2]
    except:
        pass
    documents = preprocess(filePath)
    #print documents
    dictionary = createDictionary(filePath, fileName)
    #print dictionary.values


'''
Author Notes:
-Rewrite the code so that savePaths are not hard coded
'''
