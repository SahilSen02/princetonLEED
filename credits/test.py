import json

f = open('credit.json')

data = json.load(f)

print(data['Location and Transportation'])

f.close()