import requests
import unicodedata
keyword = ['password','username','log in', 'sign in', 'login', 'credit card', 'creditcard', 'ssn', 'social security', 'pin', 'account number', 'routing number']
testlink ='http://www.b.com'
#  Call the calssifyLink() function to get classficataion result 
#  if return value is 1, it means it contains login,password, sign in information
#  if return value is 0, it means it doesn't
#  if return value is -1, it means it is not a valid link

def hasCredential(str):
    content = unicodedata.normalize('NFKD', str)
    content = content.lower()
    matches = 0
    for key in keyword:     # by item
        result = content.find(key)
        if result != -1:
            matches +=1
    if matches >= 4:
        return 1
    return 0
def classifyLink(str):
    headers = {'Accept-Encoding': 'identity'}
    try:

        r = requests.get(str,headers=headers,allow_redirects=True)
        text = r.text
        return hasCredential(text)
    except:
        return -1
    