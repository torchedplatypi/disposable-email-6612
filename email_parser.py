# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 22:06:56 2019

@author: Nahom
"""
#!/usr/bin/python
import sys
import os
import glob
import re 

#This script runs on every csv file now

#grab current working directory and list of csv files
cwd = os.getcwd() 
filelist = [i for i in glob.glob('*.{}'.format('csv'))]


#setups for text file names and directory names
extension = ".txt"
holder = "email_"
linecount = 0 #number of emails per csv tracker
training = "training_data"
slash = "/"
senders = "senders.txt"
subjects = "subject.txt"
words = "words.txt"
senders = cwd + slash + senders #file containing every sender instance
subjects = cwd + slash + subjects #file containing every subject line instance
words = cwd + slash + words #file containing a body of words for email content

#checking to see if a training data folder exists
trainingd = cwd + slash + training
if os.path.isdir(trainingd):
    trainingd = trainingd
else:
    os.mkdir(trainingd)

#does the file exist
if os.path.isfile(senders):
   fsend = open(senders, "r+")
   fsubj = open(subjects,"r+")
   fwords = open(words,"r+")
   
else:
   fsend = open(senders, "w")
   fsubj = open(subjects,"w")
   fwords = open(words,"w")
   
#goes through every csv file
for csv in filelist:
    fn = re.sub('\.csv', '', csv)
    post = cwd + slash + training + slash + fn #directory to put each individual set of emails in
    os.mkdir(post)
    #looks like each line is an email
    with open(csv) as file:
        for line in file:
            linecount += 1
            num = str(linecount)
            #remove excess whitespace
            line = re.sub(' +', ' ',line)
            #create new file in txt
            fnf = holder + num + extension
            outfile = open(fnf,"w")
            #get old filepath
            pre = cwd + slash + fnf
            #print(pre)
            #create new filepath   
            #print(post)
            post = cwd + slash + training + slash + fn + slash + fnf
            #print(post)
            #rename file to move to training folder
            os.rename(pre,post)
            sentfrom = line.split(';')[0] #grab sender
            subjectline = line.split(';')[1]  #grab subject
            line = line.replace(sentfrom + ';' ,"")
            body = line.replace(subjectline + ';',"") #parse for body content
            fsend.write(sentfrom + '\n')
            fsubj.write(subjectline + '\n')
            fwords.write(body + '\n\n' )
            outfile.write(sentfrom + '\n')
            outfile.write(subjectline + '\n')
            outfile.write(body + '\n')
            outfile.close()
        
fsend.write('\n')
fsubj.write('\n')
fwords.write('\n' )     
fsend.close()
fsubj.close()
fwords.close()       
       

        

