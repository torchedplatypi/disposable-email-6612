# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 21:33:23 2019

@author: Nahom
"""

#!/usr/bin/python
import sys
import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
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
elif option == '-o' and len(sys.argv) >= 3:
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
elif option == '-d' and len(sys.argv) >= 3:
    directory = sys.argv[2]
    path = directory
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
elif option == '-e' and len(sys.argv) >= 3:
    email = sys.argv[2]
    path = email   
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

row,col = X.shape
X_dense = X.todense()
r,c = X_dense.shape
#use PCA to transform the features
n = 5000
cycles = math.ceil(float(r) / n)
for i in range(0,int(cycles)):
    if r < n:
        temp = PCA(n_components=2).fit_transform(X_dense[i*n:,:])
    else:
        temp = PCA(n_components=2).fit_transform(X_dense[i*n:(i+1)*n,:])
    r -= n
    if i == 0:
        coords = np.array(temp)
    else:
        coords = np.concatenate([coords,temp],axis=0)

#turn off interactive
plt.ioff()
#get the top features of the dataset and output to a text file
features = vect.get_feature_names()
#cluster based on number of clusters
try:
    n_clusters = int(sys.argv[3])
except:
    print("ERROR: could not parse number of clusters from input")
    sys.exit()
clf = KMeans(n_clusters=n_clusters, max_iter=100, init='k-means++',n_init=1)
labels = clf.fit_predict(X)
label_colors = ['#2AB0E9','#2BAF74','#D7665E', '#CCCCCC', '#AAAAAA', '#BBBBBB', '#EEEEEE', '#FFFFFF']
#cluster0 -> blue
#cluster1 -> green
#cluster2 -> red
colors = [label_colors[i] for i in labels]

plt.scatter(coords[:,0], coords[:,1],c=colors)
#output plot as a figure
path = 'Clustering_DataSet.png'
plt.savefig(path,format = 'png')
plt.close()
#finding top features per cluster

unilabels = np.unique(labels)
count = 0
for label in unilabels:
    
    ind = np.where(labels==label)
    uD = X[ind].toarray()
    uD[uD < .1] = 0
    utmeans = np.mean(uD,axis=0)
    utopn_ids = np.argsort(utmeans)[::-1][:50]
    clus_feat = [(features[i],utmeans[i]) for i in utopn_ids]
    strcount = str(count)
    fnf = 'Cluster_' + strcount + '_Features.txt' 
    cfile = open(fnf,'w')
    cfile.write('features \t\t score\n')
    for feat in clus_feat:
        cfile.write(str(feat))
        cfile.write('\n')
    cfile.close()
    count += 1

print('Code Execution Finished')
