# -*- coding: utf-8 -*-
'''
Created on Mon Dec 6 17:42:37 2013

Scrape initial dataset for LDA and Sentence Extraction

@author: nbantilan
'''

import urllib2
import bs4
import sys

#hard coded the query for bmcph journal
url = "http://www.pubmedcentral.nih.gov/oai/oai.cgi?verb=ListRecords&set=bmcph&metadataPrefix=pmc"
resumptionUrl = 'http://www.pubmedcentral.nih.gov/oai/oai.cgi?verb=ListRecords&resumptionToken='


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

    #number of results to pull, determined by command line argument
    numResults = int(sys.argv[1])
    path = str(sys.argv[2]) + '/'

    queryCount = 0
    response = queryEntrez(url)
    soup = soupify(response)
    records = soup.find_all('record')

    while queryCount < numResults:

        for i in range(len(records)):

            if queryCount > numResults:
                break

            else:
                #increment counter
                queryCount += 1

                #try to grab abstract text
                try:
                    abstract = records[i].find('abstract').get_text()
                except:
                    abstract = ''

                #try to grab body text
                try:
                    body = records[i].find('body').get_text()
                except:
                    body = ''

                record = abstract + body
                record = record.encode('ascii', 'ignore')
                prepend = str(0) * (len(str(numResults)) - len(str(queryCount)))
                with (open(path + (prepend + str(queryCount)) + '.txt', "w")) as text:
                    text.write(record)

        newUrl = resumptionUrl + getResumptionToken(soup)
        response = queryEntrez(newUrl)
        soup = soupify(response)
        records = soup.find_all('record')
