from ExtractHRefClass import ExtractHRef
import AnalyzeWeb
import os, sys
class SuspiciousClassifier(object):

	def __init__(self):
		self.folder = ""
		self.filename = ""
		self.extractor = ExtractHRef()
		self.htmlevaulator = HtmlEvaluator()

	def set_folder(self, f):
		self.folder = f

	def set_filename(self, f):
		self.filename = f


	def read_file(self):

		suspicious_emails = []
		self.extractor.set_filename(self.filename)
		all_urls = self.extractor.get_urls()

		idx = 0
		for links_in_email in all_urls:
			for url in links_in_email:
				if AnalyzeWeb.classifyLink(url) == 1:
					suspicious_emails.append(idx)
					break
			idx+=1

		print(suspicious_emails)



if __name__ == "__main__":
	f = "filename"
	if len(sys.argv) > 1:
		f = sys.argv[1]
	sc = SuspiciousClassifier()
	sc.set_filename(f)
	sc.read_file()





