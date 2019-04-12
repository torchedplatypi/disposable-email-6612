# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 21:33:23 2019

@author: Nahom
"""

#!/usr/bin/python
import sys
import os
import glob

#import sklearn.feature_extraction.text
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import math
#this script runs a unsupervised classifier on data
body = []
#get the dataset option or help menu
if len(sys.argv) == 1:
    print('ERROR: Missing arguments. Try again...')
    sys.exit()
option = sys.argv[1]
#current working directory
cwd = os.getcwd()
#display all options
if option == '-h':
    print('This is the help option. Below are the available options for learning')
    print('-o\tThis will run the algorithm on the entire data set. Insert filename to text file containing all the words of the set.')
    print('-d\tThis will run the algorithm on a single day. Insert path to day directory as second argument')
    print('-e\tThis will run the algorithm on a single email. Insert the path to the email as second argument')
    print('Thank You!!!')
#option to run on entire dataset
elif option == '-o' and len(sys.argv) == 3:
    #grab the words text file that contains all the words of the entire data set
    dataset = sys.argv[2]
    fh = open(dataset)
    body = []
    #append each email to a list stripping of all trailing whitespace
    for line in fh:
        if line != '\n' and line != '\r\n':
            body.append(line.rstrip())
            #print(line)
#option to run on a subset by day
elif option == '-d' and len(sys.argv) == 3:
    directory = sys.argv[2]
    path = cwd + '/' + directory
    #grab each individual email file
    filelist = [i for i in glob.glob(path + '/*.txt')]
    body = []
    #go through each email and grab the message content
    for file in filelist:
        fh = open(file)
        count = 0
        for line in fh:
            if count == 2:
                body.append(line.rstrip())
                #need this because email_parser sometimes adds an extra line
                break;
            else:
                count += 1
#option to run on a single email, pretty useless option    
elif option == '-e' and len(sys.argv) == 3:
    email = sys.argv[2]
    path = cwd + '/' + email   
    fh = open(path)
    count = 0
    body = ''
    for line in fh:        
        if count == 2:
            body = line.rstrip()
            break;
        else:
            count += 1
#error output
else:
    print('Error: Incorrect arguments or number of arguments. Try again...')    

#learning portion of the code 
#vectorize the email contents
vect = TfidfVectorizer(stop_words='english',max_df=.5,min_df=2)
X = vect.fit_transform(body)
X_dense = X.todense()
#use PCA to transform the features
bodlen = len(body)
n = 5000
cycles = math.ceil(float(len(body)) / n)
randomdata = np.random.permutation(bodlen)
body = body[randomdata]
for i in range(0,int(cycles)):
    if bodlen < n:
        temp = PCA(n_components=2).fit_transform(X_dense[i*n:,:])
    else:
        temp = PCA(n_components=2).fit_transform(X_dense[i*n:(i+1)*n])
    bodlen -= n
    if i == 0:
        coords = temp
    else:
        coords = np.concatenate([coords,temp],axis=0)

#turn off interactive
plt.ioff()
#get the top features and output to a text file
features = vect.get_feature_names()
row = np.squeeze(X[1].toarray())
topn_ids = np.argsort(row)[::-1][:25]
top_features = [(features[i],row[i]) for i in topn_ids]
outfile = open('testfile1.txt','w')
outfile.write('features \t\t score\n')
for index in top_features:
    outfile.write(str(index))
    outfile.write('\n')
outfile.close()
#cluster based on number of clusters
n_clusters = 3
clf = KMeans(n_clusters=n_clusters, max_iter=100, init='k-means++',n_init=1)
labels = clf.fit_predict(X)
label_colors = ['#2AB0E9','#2BAF74','#D7665E', '#CCCCCC']
colors = [label_colors[i] for i in labels]
plt.scatter(coords[:,0], coords[:,1],c=colors)
#output plot as a figure
path = 'test1.png'
plt.savefig(path,format = 'png')
plt.close()
print('Code Execution Finished')