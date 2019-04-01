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

#this script is used on one csv file at a time. Optimization will be the least of my worries at the moment
#grab the csv file to parse
csv = sys.argv[1]
#get current working directory to move files to training_set
cwd = os.getcwd()
#remove the csv part of the file we are looking for
fn = re.sub('\.csv', '', csv)
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

post = cwd + slash + training + slash + fn #directory to put each individual set of emails in
os.mkdir(post)

#does the file exist
if os.path.isfile(senders):
   fsend = open(senders, "r+")
   fsubj = open(subjects,"r+")
   fwords = open(words,"r+")
   
else:
   fsend = open(senders, "w")
   fsubj = open(subjects,"w")
   fwords = open(words,"w")
   
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
        outfile.write(line)
        outfile.close()
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

fsend.write('\n')
fsubj.write('\n')
fwords.write('\n' )     
fsend.close()
fsubj.close()
fwords.close()       
       

        

