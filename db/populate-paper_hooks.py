# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 12:09:28 2013

@author: dchen
"""

#import MySQLdb
import os

##password = raw_input("MySQL DB Password: ")
#
#conn = MySQLdb.connect(host = "*****", user = "*****", passwd = "*****")
#
#cursor = conn.cursor() #create the cursor connection to MySQL
##conn.autocommit(1)
#
#myQ = "use gsumm;"
#cursor.execute(myQ)
#
#myQ = "select * from paper_metadata;"
#cursor.execute(myQ)
#
#os.getcwd()
#os.chdir("/home/dchen/git/phds-gsumm/summaries")
#os.getcwd()
#os.listdir("./")
#
#
##listOfColNames = []
##listOfColNames = [title, topic, objectives, hypothesis, study_design, sampling_method, findings, implications, future_research, limitations]
##listOfColNames[2]

with open("/home/dchen/git/phds-gsumm/summaries/allsummaries_escaped.tsv", "r") as hooks:
    with open("/home/dchen/git/phds-gsumm/db/sqloutput.sql","w") as f:
        numObservation = 816
        currentLine = 0
        section = []
        
        for line in hooks:
            if currentLine == 0:
                currentLine += 1
                continue
            if currentLine >= 0 and currentLine <= numObservation:
                section = line.split('\t')
                #print section
                currentLine += 1
                
                title = str(section[0])
                topic = str(section[1])
                objectives = str(section[2])
                hypothesis = str(section[3])
                study_design = str(section[4])
                sampling_method = str(section[5])
                findings = str(section[6])
                implications = str(section[7])
                future_research = str(section[8])
                limitations = str(section[9])
                doi = str(section[10][:-1])
                #print title
                #print limitations
                
                query = 'INSERT INTO paper_hooks \n (title, topic, objectives, hypothesis, study_design, sampling_method, findings, implications, future_research, limitations, doi) \n VALUES (\n "' + title + '" , \n"' + topic  + '" , \n"' + objectives + '" , \n"' + hypothesis + '" , \n"' + study_design + '" , \n"' + sampling_method + '" , \n"' + findings + '" , \n"' + implications + '" , \n"' + future_research + implications + '" , \n"' + limitations + '" , \n"' + doi + '"\n);\n'
                
                #print "************************************************************"
                print query
                f.write(query)


#INSERT INTO table_name (column1,column2,column3,...)
#VALUES (value1,value2,value3,...);



