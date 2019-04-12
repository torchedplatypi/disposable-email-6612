filename ="testfile1.txt"
fHandle = open(filename)
lines = fHandle.readlines()
fHandle.close()
data = {}
for l in lines[1:]:
    l = l.strip('\n')
    l = l.strip('()')
    words = l.split(',')
    key = words[0]
    key = key.strip('u')
    key = key.strip('\'')
    value = float(words[1])
    data[key] = value

print (data)
