import string
import sys
import re
import math
import json
from collections import defaultdict

modelData = {}
counttag=defaultdict(int)
wordtagcount = defaultdict(lambda : defaultdict(int))
tagtransitioncount = defaultdict(lambda : defaultdict(float))
alltags = []

'''reading the data'''
raw_training_data = open(sys.argv[1],"r")
sentence = raw_training_data.readlines()
for index in range(len(sentence)):
	wordtag = sentence[index].replace('\n','').split(" ")
	previoustag = "start"
	for splitindex in range(len(wordtag)):
		wordtagsplit = wordtag[splitindex].rsplit("/",1)
		counttag[wordtagsplit[1]] += 1
		wordtagcount[wordtagsplit[0]][wordtagsplit[1]] += 1
		tagtransitioncount[previoustag][wordtagsplit[1]] += 1
		previoustag = wordtagsplit[1]

alltags = tagtransitioncount.keys()

for tag in alltags:
	for subtag in alltags:
		if subtag not in tagtransitioncount[tag]:
			tagtransitioncount[tag][subtag] = 0.0
	sumofoutgoingtags =  sum(tagtransitioncount[tag].values())
	tagtransitioncount[tag].update((key, (math.log(value + 1) - math.log(sumofoutgoingtags + len(alltags) - 1))) for key, value in tagtransitioncount[tag].items())

for word in wordtagcount:
		wordtagcount[word].update((key, (math.log(value) - math.log(counttag[key]))) for key, value in wordtagcount[word].items()) 

modelData["tags"] = list(alltags)
modelData["transition"] = tagtransitioncount
modelData["emission"] = wordtagcount

with open('hmmmodel.txt','w') as writefile:
	json.dump(modelData,writefile)
writefile.close()