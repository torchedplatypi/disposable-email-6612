import re

class ExtractHRef(object):
    def __init__(self, f=""):
        self.filename=f
        self.data_preped=False

    def set_filename(self, f):
        self.filename=f

    def prep_data(self):
        self.data_preped = True
        fHandle = open(self.filename)
        pattern = r'(http[s]?://[^\s\)\]\"]+)'
        urlListAll =[]
        keywordResult=[]
        lines = fHandle.readlines()
        fHandle.close()
        img_ext = ['.jpg','.gif','.png']
        sensitive_list=['name', 'address', 'card', 'telephone', 'age', 'routing number', 'account number', 'bank number', 'bank']
        self.raw_data = lines
        for l in lines:
            # performing keywords scan
            line_data = l.lower()
            words_list = line_data.split(' ')
            sensitive_information_score = 0
            for key_word in sensitive_list:
                if key_word in words_list: 
                    sensitive_information_score+=1
            keywordResult.append(sensitive_information_score)

            # extracting urls in the email
            out = re.findall(pattern,l)
            urlList = []
            # urList contains the list of urls in one particular email message body
            for url in out:
                # get rid of the </a></div> ending in some of the urls
                url = re.sub('\</div>$', '', url)
                url = re.sub('\</a>$', '', url)
                length = len(url)
                # skip links ending with .jpg or gif or png
                if url[length-4:] in img_ext:
                    pass 
                elif url not in urlList:
                    urlList.append(url)
            urlListAll.append(urlList)
        self.urlList = urlListAll
        self.keywordResult = keywordResult

    def get_urls(self):
        if not self.data_preped:
            self.prep_data()
        return self.urlList

    def get_keywordsScan(self): 
        if not self.data_preped:
            self.prep_data()
        return self.keywordResult

    def get_raw(self): 
        if not self.data_preped:
            self.prep_data()
        return self.raw_data
    

if __name__ == "__main__":
    data = ExtractHRef("data/4-5-2019.csv")
    urls = data.get_urls()
    keywordResults = data.get_keywordsScan()
