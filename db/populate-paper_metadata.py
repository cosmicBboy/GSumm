# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:42:00 2013

@author: dchen
"""

import MySQLdb
import os

#password = raw_input("MySQL DB Password: ")

conn = MySQLdb.connect(host = "*****", user = "*****", passwd = "*****")

cursor = conn.cursor() #create the cursor connection to MySQL
#conn.autocommit(1)

myQ = "use gsumm;"
cursor.execute(myQ)

myQ = "select * from paper_metadata;"
cursor.execute(myQ)

os.getcwd()
os.chdir("/home/dchen/git/phds-gsumm/web_scraper/structuredTextFiles/hiv+aids")
os.getcwd()
os.listdir("./")

with open("hiv+aids_metadata.tsv", "r") as metadata:
    numObservation = 3
    index = 0
    section = []
    
    for line in metadata:
        if index == 0:
            index += 1
            continue
        if index > 0 and index <= numObservation:
            section = line.split('\t')
           # print section
            index += 1
            
            doi = str(section[1])
            author = str(section[2])
            publication_date = str(section[3])
            journal = str(section[4])
            article_type = str(section[5])
            subject = str(section[6])
            subject_level_1 = str(section[7])
            eissn = str(section[8])
            publisher = str(section[9][:-1])
            print publisher
            
            query = 'INSERT INTO paper_metadata \n (id, author, publication_date, journal, article_type, subject, subject_level_1, eissn, publisher) \n VALUES (\n "' + doi + '" , \n"' + author  + '" , \n"' + publication_date + '" , \n"' + journal + '" , \n"' + article_type + '" , \n"' + subject + '" , \n"' + subject_level_1 + '" , \n"' + eissn + '" , \n"' + publisher + '"\n);'
            
            print query


#INSERT INTO table_name (column1,column2,column3,...)
#VALUES (value1,value2,value3,...);



