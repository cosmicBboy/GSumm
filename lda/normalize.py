# -*- coding: utf-8 -*-
'''
Created on Thu May 8 20:46:22 2014

Creating a corpus

@author: Niels Bantilan
'''
import logging
from gensim import corpora, models

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)


mm = corpora.MmCorpus('../corpus/mediumData.mm')
print mm

tfidf = models.TfidfModel([doc for doc in mm])
tfidf.save('../corpus/mediumData.tfidf_model')
corpusTfidf = tfidf[[doc for doc in mm]]
