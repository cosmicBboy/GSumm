# -*- coding: utf-8 -*-
'''
Created on Mon Dec 6 17:42:37 2013

PubMed Article Search Entrez Query

@author: nbantilan
'''

import urllib2
import bs4
from pandas import *
import os
import re
from itertools import chain

############################
##                           ##
##  Define data elements  ##
##                           ##
############################

metadata_elements = ['title',
                     'pubdate',
                     'doi',
                     'pmc_id',
                     'journalId',
                     'publisher',
                     'article_type',
                     'authors',
                     'keywords']

textdata_elements = ['doi',
                     'pmc_id',
                     'section',
                     'paragraphIndex',
                     'sentenceIndex',
                     'sentence']

##################################
##                                   ##
##  Data Structuring Functions  ##
##                                   ##
##################################


#parses sentences
def parseSentence(text, pattern=''):

    if pattern != '':
        pass
    else:
        pattern = r'(\.)(\s)([A-Z]|[0-9])'

    sentences = re.split(pattern, text)
    return sentences

#query the Entrez Utility to do a topic-specific search, builds url to return pmc_id
def searchEntrezQuery(subjectQuery, database = 'pmc', start = 0, max_return = 10, openAccess = True):

#base url, database, and term query
    entrezBaseUrl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
    db = 'db=' + database
    term = '&term=' + subjectQuery

    #control structure for returning PMC open access articles
    if openAccess == True:
        term = term + '+AND+open+access[filter]'

    #ret start for response starting point, retmax for number of responses to return
    retstart = '&retstart=' + str(start)
    retmax = '&retmax=' + str(max_return)
    usehistory = '&usehistory=y'

    #final search string
    query = entrezBaseUrl + db + term + retstart + retmax + usehistory
    return query

#return query_key and WebEnv for fulltext harvesting
def getWebEnv(entrezSearch):
    response = urllib2.urlopen(entrezSearch)
    responseXML = response.read()
    responseXML = bs4.BeautifulSoup(responseXML, 'xml')
    webEnv = responseXML.find_all('WebEnv')[0].get_text()
    query_key = responseXML.find_all('QueryKey')[0].get_text()
    return query_key, webEnv

def fetchEntrezQuery(query_key, webEnv, database = 'pmc', start = 0, max_return = 10):
    base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    db = 'db=' + database
    query_key = '&query_key=' + str(query_key)
    webEnv = '&WebEnv=' + str(webEnv)
    retstart = '&retstart=' + str(start)
    retmax = '&retmax=' + str(max_return)

    #form fetch url
    fetchUrl = base + db + query_key + webEnv + retstart + retmax
    return fetchUrl

def fetchEntrezArticles(fetchUrl):
    response = urllib2.urlopen(fetchUrl)
    responseXML = response.read()
    responseXML = bs4.BeautifulSoup(responseXML, 'xml')
    articleList = responseXML.find_all('article')
    return articleList

def parseMetadata(responseXML):
    '''
    parses the response XML and returns a dictionary: keys -> metadata elements  values -> metadata values
    '''
    articleTitle = responseXML.find_all('article-title')[0].get_text()
    journalId = ''.join([ID.get_text() for ID in responseXML.find_all('journal-title')])        #parse journalId
    publisher = ''.join([pub.get_text() for pub in responseXML.find_all('publisher-name')])        #parse publisher
    articleId = responseXML.find_all('article-id', attrs = {'pub-id-type': 'pmc'})                #parse article ID
    subject = ''.join([sub.get_text() for sub in responseXML.find_all('subject')])                #parse subject
    
    #parse publication date
    try:
        date = responseXML.find_all('pub-date', attrs={'pub-type':'epub'})[0]
        year, month, day = date.find_all('year'), date.find_all('month'), date.find_all('day')
        year, month, day = year[0].get_text(), month[0].get_text(), day[0].get_text()
        pubdate = year + '-' + month + '-' + day
    except:
        pubdate = 'NA'

    #parse doi
    try:
        doi = responseXML.find_all('article-id', attrs = {'pub-id-type' : 'doi'})[0].get_text()
    except:
        doi = 'NA'

    #parse pmc_id
    try:
        pmc_id = responseXML.find_all('article-id', attrs = {'pub-id-type' : 'pmc'})[0].get_text()
    except:
        pmc_id = 'NA'

    #parsing author metadata
    authorXML = responseXML.find_all('contrib', attrs={'contrib-type' : 'author'})
    authorSurnames = [item.get_text() for item in list(chain(*[author.find_all('surname') for author in authorXML]))]
    authorFirstNames = [item.get_text() for item in list(chain(*[author.find_all('given-names') for author in authorXML]))]
    author = ' ; '.join([', '.join(author) for author in zip(authorSurnames, authorFirstNames)])

    #parse keyword group
    keywords = ','.join([kwd.get_text() for kwd in responseXML.find_all('kwd-group')])
    keywords = re.sub(r'\n', r';', keywords)
    if not keywords:
        keywords = 'NA'

    metadata = {'title' : articleTitle, 
                'pubdate' : pubdate, 
                'doi' : doi,
                'pmc_id' : pmc_id,
                'journalId' : journalId, 
                'publisher' : publisher, 
                'article_type' : subject, 
                'authors' : author, 
                'keywords' : keywords}

    metadataDataFrame = DataFrame(metadata, columns = metadata_elements, index = [0])
    return metadataDataFrame


def parseAbstract(responseXML):
    '''
    parses the response XML and returns a dataframe of abstract sentences
    '''    
    try:
        doi = responseXML.find_all('article-id', attrs = {'pub-id-type' : 'doi'})[0].get_text()
    except:
        doi = 'NA'

    #parse pmc_id
    try:
        pmc_id = responseXML.find_all('article-id', attrs = {'pub-id-type' : 'pmc'})[0].get_text()
    except:
        pmc_id = 'NA'

    #define abstract dictionary
    abstract = {'doi' : [], 'pmc_id' : [],'section' : [], 'paragraphIndex' : [], 'sentenceIndex' : [], 'sentence': []}
    
    try:
        #try to extract abstract sections 
        abstractRaw = responseXML.find_all('abstract', attrs={'abstract-type':None})
        sections = abstractRaw[0].find_all('sec')

        for section in sections:
            title = section.find_all('title')[0].get_text()
            paragraphs = [para.get_text() for para in section.find_all('p')]

            paragraphCounter = 1
            for para in paragraphs:
                sentences = parseSentence(para)
                for i in range(len(sentences)):
                    abstract['sentence'].append(sentences[i])
                    abstract['section'].append(title)
                    abstract['sentenceIndex'].append(i+1)
                    abstract['paragraphIndex'].append(paragraphCounter)
                    abstract['doi'].append(doi)
                    abstract['pmc_id'].append(pmc_id)
                paragraphCounter += 1
    except:
        abstract = {'doi': doi, 'pmc_id' : pmc_id, 'section' : ['NA'],'paragraphIndex':['NA'], 'sentenceIndex':['NA'],'sentence':['NA']}

    abstractDataFrame = DataFrame(abstract, columns = textdata_elements)
    return abstractDataFrame
    

def parseText(responseXML):
    '''
    parses the response XML and returns a dataframe of fulltext sentences
    '''
    try:
        doi = responseXML.find_all('article-id', attrs = {'pub-id-type' : 'doi'})[0].get_text()
    except:
        doi = 'NA'

    #parse pmc_id
    try:
        pmc_id = responseXML.find_all('article-id', attrs = {'pub-id-type' : 'pmc'})[0].get_text()
    except:
        pmc_id = 'NA'

    #define fulltext dictionary
    fulltext = {'doi' : [], 'pmc_id' : [], 'section' : [], 'paragraphIndex' : [], 'sentenceIndex' : [], 'sentence' : []}
    
    try:
        textRaw = responseXML.find_all('body')[0]
        sections = textRaw.find_all('sec', recursive = False)

        for section in sections:
            title = section.find_all('title', recursive = False)[0].get_text()
            paragraphs = [para.get_text() for para in section.find_all('p')]
            
            paragraphCounter = 1
            for para in paragraphs:
                sentences = parseSentence(para)
                for i in range(len(sentences)):
                    fulltext['sentence'].append(sentences[i])
                    fulltext['section'].append(title)
                    fulltext['sentenceIndex'].append(i+1)
                    fulltext['paragraphIndex'].append(paragraphCounter)
                    fulltext['doi'].append(doi)
                    fulltext['pmc_id'].append(pmc_id)
                paragraphCounter += 1
    except:
        fulltext = {'doi' : [doi], 'pmc_id' : [pmc_id], 'section' : ['NA'], 'paragraphIndex' : ['NA'], 'sentenceIndex' : ['NA'], 'sentence' : ['NA']}

    fulltextDataFrame = DataFrame(fulltext, columns = textdata_elements)
    return fulltextDataFrame


def batchStructureData(articleList):
    '''
    performs a batchquery on the pmc-oa API and structures metadata, abstracts, and fulltext of each pmc-id
    '''
    metadataDataFrame = DataFrame(columns = metadata_elements)
    abstractDataFrame = DataFrame(columns = textdata_elements)
    fulltextDataFrame = DataFrame(columns = textdata_elements)

    for article in articleList:
        metadataDataFrame = metadataDataFrame.append(parseMetadata(article), ignore_index = True)
        abstractDataFrame = abstractDataFrame.append(parseAbstract(article), ignore_index = True)
        fulltextDataFrame = fulltextDataFrame.append(parseText(article), ignore_index = True)

    return {'metadata' : metadataDataFrame, 'abstract' : abstractDataFrame, 'fulltext' : fulltextDataFrame}


def buildDatabase(query, filenamePrefix, savePath):
    '''
    takes a filename and path argument to a .csv file and builds an 
    article database of fulltext and abstract parsed by section and an article metadatabase 
    '''
    #article harvesting pipeline
    print 'harvesting articles...'
    url = searchEntrezQuery(query)
    webEnv= getWebEnv(url)

    #hard code a for loop for running batch queries (to avoid overloading the system)
    max_total = 2000
    batches = 100
    queryNumber = max_total/batches

    #define empty dataframes
    metadataDataFrame = DataFrame(columns = metadata_elements)
    abstractDataFrame = DataFrame(columns = textdata_elements)
    fulltextDataFrame = DataFrame(columns = textdata_elements)

    for i in range(queryNumber):
        start = i * batches
        fetchUrl = fetchEntrezQuery(webEnv[0], webEnv[1], start = start, max_return = batches)
        print 'query number: ' + str(i + 1)
        articleList = fetchEntrezArticles(fetchUrl)
        batchData = batchStructureData(articleList)

        metadataDataFrame = metadataDataFrame.append(batchData['metadata'], ignore_index = True)
        abstractDataFrame = abstractDataFrame.append(batchData['abstract'], ignore_index = True)
        fulltextDataFrame = fulltextDataFrame.append(batchData['fulltext'], ignore_index = True)

    #database filenames
    meta_filename = filenamePrefix + '_meta.tsv'
    abstract_filename = filenamePrefix + '_abstract.tsv'
    fulltext_filename = filenamePrefix + '_fulltext.tsv'

    #save to directory
    os.chdir('/')
    os.chdir(savePath)
    metadataDataFrame.to_csv(meta_filename, sep = '\t', encoding = 'utf-8', index_label = 'row')
    abstractDataFrame.to_csv(abstract_filename, sep = '\t', encoding = 'utf-8', index_label = 'row')
    fulltextDataFrame.to_csv(fulltext_filename, sep = '\t', encoding = 'utf-8', index_label = 'row')



##################################
##                                   ##
##  Script for Structuring Data ##
##                                   ##
##################################

#queryList = ['health+policy','asthma','malaria','obesity','hiv+aids']
queryList = ['malaria','obesity','hiv+aids']
savePath = os.path.expanduser('~/git/phds-gsumm_data/PubMed')

for query in queryList:
    print 'querying: ' + query
    buildDatabase(query, query, savePath)
