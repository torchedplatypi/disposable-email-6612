import requests
import csv
import numpy as np 
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
    




# url = open('4-7-2019.csv_output','r').read().split('\n')
# url = open('4-7-2019.csv_output','r')
# phish = np.array([])
# curWeb = url.readline().strip('\n')
# curWeb = url.readline().strip('\n')

# running = 1
# i = 0

# print(calssifyLink(testlink))
# searResult= np.array([]);

# while running:
#     print(i)
#     curWeb = url.readline().strip('\n')
#     try:
#         r = requests.get(curWeb,headers=headers)
#         text = r.text;
#         searResult = np.append(searResult,hasCredential(text))
#     except:
#         searResult = np.append(searResult,-1)
#         print("unvalid links")

#     if url.readline() == 0:
#         running = 0
#     i = i +1;





    



