# -*- coding: utf-8 -*-
'''
Created on Mon Dec 6 17:42:37 2013

Scrape initial dataset for LDA and Sentence Extraction

@author: nbantilan
'''

import urllib2
import bs4

#hard coded the query for bmcph journal
url = "http://www.pubmedcentral.nih.gov/oai/oai.cgi?verb=ListRecords&set=bmcph&metadataPrefix=pmc"


def queryEntrez(queryString):
    response = urllib2.urlopen(queryString)
    responseXML = response.read()
    return responseXML


def soupify(responseXML):
    soup = bs4.BeautifulSoup(responseXML, 'xml')
    return soup


def getResumptionToken(soup):
    """Takes a soupified XML response and returns resumptionToken tag text"""
    return soup.find('resumptionToken').get_text()


if __name__ == "__main__":
    #number of results to pull
    response = queryEntrez(url)
    soup = soupify(response)
    records = soup.find_all('record')

    for i in range(len(records)):
        record = records[i].find('abstract').get_text()\
            + records[i].find('body').get_text()
        record = record.encode('ascii', 'ignore')
        with (open('smallData/' + str(i) + '.txt', "w")) as text:
            text.write(record)
