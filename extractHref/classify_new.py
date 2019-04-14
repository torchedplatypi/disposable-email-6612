### Import and save 'WORD',<VALUE> pairs into dictionaries ###
import os
all_lines = []
def set_freq_data(folder, fs):
	global all_lines
	for f in fs:
		ftemp = os.path.join(folder, f)
		fhandle = open(ftemp)
		all_lines.append(fhandle.readlines())
		fhandle.close()

def freqPhishingTest(bodycontent):
	"Return score of email per cluster"
	global all_lines
	
	all_data = []
	count = 0
	for line in all_lines:
		all_data.append({})
		for i in line[1:]:
			i = i.strip('\n')
			i = i.strip('()')
			words1 = i.split(',')
			key1 = words1[0]
			key1 = key1.strip('u')
			key1 = key1.strip('\'')
			value1 = float(words1[1])
			all_data[count][key1] = value1
		count += 1
	### Iterate over each word in the message, checking to see if the word
	### appears in each high-freq table then aggregate values
	bodyWords = bodycontent.split() #split at each space
	scores = [0]*len(all_lines)
	for x in range(len(bodyWords)):
		count = 0
		for d in all_data:
			scores[count] += d.get(bodyWords[x].lower(),0)
			count += 1
	d = {}
	for i in range(len(all_lines)):
		d["Clust" + str(i)] = scores[i]

	return d
