from ExtractHRefClass import ExtractHRef
import AnalyzeWeb
import os, sys, re
from matplotlib import pyplot as plt
import classify_new
import operator
import numpy as np

class SuspiciousClassifier(object):

	def __init__(self, max_emails=100,phishing_cluster=1):
		self.folder = ""
		self.filename = ""
		self.extractor = ExtractHRef()
		self.max_emails = max_emails
		self.phish_clust = phishing_cluster
	def set_folder(self, f):
		self.folder = f

	def set_filename(self, f):
		self.filename = f
	def set_freq_data(self,folder, fs):
		classify_new.set_freq_data(folder, fs)

	def check_level(self, links, score, raw):
		# check links for suspicious entries #
		sus_link = 0
		for url in links:
			if AnalyzeWeb.classifyLink(url) == 1:
				sus_link = 1
				break
		print("Sus_link: %s" % sus_link)

		keyword_match = 0
		if score >= 3:
			keyword_match = 1
		
		print("keyword_match %s" % keyword_match)
		analysis_val = max(keyword_match, sus_link)

		body_content = ""
		linecount = 0
		cluster_val = 0
		line = raw
		#remove excess whitespace
		line = re.sub(' +', ' ',line)
		sentfrom = line.split(';')[0] #grab sender
		subjectline = line.split(';')[1]  #grab subject
		line = line.replace(sentfrom + ';' ,"")
		body = line.replace(subjectline + ';',"") #parse for body content
		body_content = body
		
		# check if cluster matches #

		scs = classify_new.freqPhishingTest(body_content)
		clust = max(scs.items(), key=operator.itemgetter(1))[0] 
		print(scs)
		print(clust)
		cluster_val = 0
		print(str(self.phish_clust))
		print(str(self.phish_clust) in clust)
		if str(self.phish_clust) in clust:
			cluster_val = 1
		return ((analysis_val << 1) + cluster_val)


	def read_file(self):

		all_levels = []
		self.extractor.set_filename(self.filename)
		self.extractor.prep_data()
		all_links = self.extractor.get_urls()
		all_keyword_score = self.extractor.get_keywordsScan()
		all_raw = self.extractor.get_raw()
		print(len(all_links))
		idx = 0
		for idx in range(len(all_links)):
			cur_l = self.check_level(all_links[idx], all_keyword_score[idx], all_raw[idx])
			print(cur_l)
			all_levels.append(cur_l)
			print(idx)
			if idx >= self.max_emails:
				break
		try:
			print("NO Threat Email")
			print(all_raw[all_levels.index(0b00)])
			print("Cluster Match Only")
			print(all_raw[all_levels.index(0b01)])
			print("Link/Keyword Match Only")
			print(all_raw[all_levels.index(0b10)])
			print("Both Match")
			print(all_raw[all_levels.index(0b11)])
		except:
			pass
		labels = ["NO THREAT", "Cluter Match Only", "Link/Keyword Match Only", "Both Match"]
		vals = [0b00, 0b01, 0b10, 0b11]

		sizes = [len([a for a in all_levels if a == v]) for v in vals]
		fig1, ax1 = plt.subplots()
		ax1.pie(sizes, labels=labels)
		ax1.axis('equal')

		plt.savefig("./pie_chart.png")
		
		dangerous = [all_raw[i] for i in [i for i, x in enumerate(all_levels) if x == 0b11]]
		np.savetxt("high_threat_output.csv", dangerous, delimiter=";", fmt='%s')

if __name__ == "__main__":
	
	x = SuspiciousClassifier(28, 3)
	if len(sys.argv) > 1:
		filename = sys.argv[1]
	x.set_filename("../../data/mailinator_data/4-5-2019.csv")
	x.set_freq_data("../../data", ["Cluster_0_Features.txt", "Cluster_1_Features.txt", "Cluster_2_Features.txt", "Cluster_3_Features.txt"])
	x.read_file()





