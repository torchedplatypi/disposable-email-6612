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

#grab the csv file to parse
csv = sys.argv[1]
cwd = os.getcwd()
fn = re.sub('\.csv', '', csv)
extension = ".txt"
holder = "_email_"
linecount = 0
training = "training_data"
slash = "/"

#looks like each line is an email
with open(csv) as file:
    for line in file:
        linecount += 1
        num = str(linecount)
        line = re.sub(' +', ' ',line)
        fnf = fn + holder + num + extension
        outfile = open(fnf,"w")
        outfile.write(line)
        outfile.close()
        pre = cwd + slash + fnf
        post = cwd + slash + training + slash + fnf
        os.rename(pre,post)
        

