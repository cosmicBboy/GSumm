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

tfidf = models.TfidfModel.load('../corpus/mediumData.tfidf_model')
corpusTfidf = tfidf[[doc for doc in mm]]

dictionary = corpora.Dictionary.load('../corpus/mediumData.dict')

#extract n LDA topics, using 1 pass and updating once every 1 chunk
lda = models.ldamodel.LdaModel(corpus=corpusTfidf,
                               id2word=dictionary,
                               num_topics=20,
                               update_every=1,
                               chunksize=10000,
                               passes=10)

lda.save('../corpus/mediumData.lda_model')
