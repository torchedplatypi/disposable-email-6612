def freqPhishingTest(bodycontent, freq1, freq2, freq3):
	"Return score of email per cluster"

	### Import and save 'WORD',<VALUE> pairs into dictionaries ###
	f1Handle = open(freq1)
	f2Handle = open(freq2)
	f3Handle = open(freq3)
	lines1 = f1Handle.readlines()
	lines2 = f2Handle.readlines()
	lines3 = f3Handle.readlines()
	f1Handle.close()
	f2Handle.close()
	f3Handle.close()
	data1 = {}
	data2 = {}
	data3 = {}

	for i in lines1[1:]:
	    i = i.strip('\n')
	    i = i.strip('()')
	    words1 = i.split(',')
	    key1 = words1[0]
	    key1 = key1.strip('u')
	    key1 = key1.strip('\'')
	    value1 = float(words1[1])
	    data1[key1] = value1

	for j in lines2[1:]:
	    j = j.strip('\n')
	    j = j.strip('()')
	    words2 = j.split(',')
	    key2 = words2[0]
	    key2 = key2.strip('u')
	    key2 = key2.strip('\'')
	    value2 = float(words2[1])
	    data2[key2] = value2

	for k in lines3[1:]:
	    k = k.strip('\n')
	    k = k.strip('()')
	    words3 = k.split(',')
	    key3 = words3[0]
	    key3 = key3.strip('u')
	    key3 = key3.strip('\'')
	    value3 = float(words3[1])
	    data3[key3] = value3


	### Iterate over each word in the message, checking to see if the word
	### appears in each high-freq table then aggregate values
	bodyWords = bodycontent.split() #split at each space
	for x in bodyWords:
			score1 += data1.get(bodyWords[x])
			score2 += data2.get(bodyWords[x])
			score3 += data3.get(bodyWords[x])
			score4 += data4.get(bodyWords[x])


	d = {
			"Cluster 1 Score" : score1,
			 "Cluster 2 Score" : score2,
			 "Cluster 3 Score" : score3, 
			 "Cluster 4 Score" : score4
			}

	return d