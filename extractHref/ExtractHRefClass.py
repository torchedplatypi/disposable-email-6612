import re

class ExtractHRef(object):
    def __init__(self, f):
        self.filename=f

    def get_urls(self):
        fHandle = open(filename)
        pattern = r'(http[s]?://[^\s|^\)|^\]]+)'
        output =[]
        lines = fHandle.readlines()
        fHandle.close()
        img_ext = ['.jpg','.gif','.png']
        for l in lines:
            out = re.findall(pattern,l)
            urlList = []
            # urList contains the list of urls in one particular email message body
            for url in out:
                # get rid of the parenthesis surrounding the urls
                url.strip("\"")
                # get rid of the </a></div> ending in some of the urls
                url = re.sub('\</div>$', '', url)
                url = re.sub('\</a>$', '', url)
                length = len(url)
                # skip links ending with .jpg or gif or png
                if url[length-4:] in img_ext:
                    pass 
                elif url not in urlList:
                    urlList.append(url)
            output.append(urlList)
        
        return output


if __name__ == "__main__":
    data = ExtractHRef("4-7-2019.csv")
    urls = data.get_urls()