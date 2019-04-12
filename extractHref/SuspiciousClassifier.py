from ExtractHRefClass import ExtractHRef
import AnalyzeWeb
import os, sys
from matplotlib import pyplot as plt
import classify_new

class SuspiciousClassifier(object):

	levels_of_suspicion
	def __init__(self):
		self.folder = ""
		self.filename = ""
		self.extractor = ExtractHRef()

	def set_folder(self, f):
		self.folder = f

	def set_filename(self, f):
		self.filename = f

	def check_level(self, links, score, raw):
		# check links for suspicious entries #
		sus_link = 0
		for url in links:
			if AnalyzeWeb.classifyLink(url) == 1:
				sus_link = 1
				break

		keyword_match = 0
		if score >= 2:
			keyword_match = 1

		analysis_val = max(keyword_match, sus_link)

		body_content = ""
		linecount = 0
		cluster_val = 0
		#remove excess whitespace
		line = re.sub(' +', ' ',line)
		#create new file in txt
		fnf = holder + num + extension
		sentfrom = line.split(';')[0] #grab sender
		subjectline = line.split(';')[1]  #grab subject
		line = line.replace(sentfrom + ';' ,"")
		body = line.replace(subjectline + ';',"") #parse for body content
		body_content = body
		 
		# check if cluster matches #
		clust = max(classify_new.freqPhishingTest(body_content))
		if clust == "Cluster 1 Score":
			cluster_val = 1
		return ((analysis_val << 1) + cluster_val)


	def read_file(self):

		all_levels = []
		self.extractor.set_filename(self.filename)
		all_links = self.extractor.get_urls()
		all_keyword_score = self.extractor.get_keywordsScan()
		all_raw = self.extractor.get_raw()
		print(len(all_urls))
		idx = 0
		for idx in range(len(all_links)):
			cur_l = check_level(all_links[idx], all_keyword_score[idx], all_raw[idx])
			print(cur_l)
			all_levels.append(cur_l)
			if idx % 20 == 0:
				print(idx)

		print("NO Threat Email")
		print(all_raw[all_levels.index(0b00)])
		print("Cluster Match Only")
		print(all_raw[all_levels.index(0b01)])
		print("Link/Keyword Match Only")
		print(all_raw[all_levels.index(0b10)])
		print("Both Match")
		print(all_raw[all_levels.index(0b11)])

		labels = ["NO THREAT", "Cluter Match Only", "Link/Keyword Match Only", "Both Match"]
		vals = [0b00, 0b01, 0b10, 0b11]

		sizes = [len([a for a in all_levels if a == v]) for v in vals]
		fig1, ax1 = plt.subplots()
		ax1.pie(sizes, labels=labels)
		ax1.axis('equal')

		plt.savefig("./pie_chart.png")

if __name__ == "__main__":
	f = "filename"
	if len(sys.argv) > 1:
		f = sys.argv[1]
	sc = SuspiciousClassifier()
	sc.set_filename(f)
	sc.read_file()





