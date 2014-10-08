# -*- coding: utf-8 -*-
'''
Created on Thu May 8 20:46:22 2014

Creating a corpus

@author: Niels Bantilan
'''

from gensim import corpora
import sys


def createCorpus(filePath, dictName, docName):

    #load dictionary
    dictionary = corpora.Dictionary.load('%s/%s' % (filePath, dictName))
    print dictionary.values()

    #load text
    with open('%s/%s' % (filePath, docName), 'r') as docs:
        documents = [line for line in docs.readlines()]

    corpus = [dictionary.doc2bow(d.split()) for d in documents]
    corpora.MmCorpus.serialize('%s/%s' % (filePath, 'mediumData.mm'), corpus)

    return corpus

if __name__ == "__main__":
    try:
        filePath = sys.argv[1]
        dictName = sys.argv[2]
        docName = sys.argv[3]
    except:
        pass
    corpus = createCorpus(filePath, dictName, docName)
    #print corpus
