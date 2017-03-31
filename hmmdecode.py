import string
import sys
import re
import math
import json
from collections import defaultdict
reload(sys)
sys.setdefaultencoding("utf-8")

output=open('hmmoutput.txt',"w")
with open('hmmmodel.txt', 'r') as in_file:
	model = json.load(in_file)

wordtaginformation = model["emission"]
alltags = model["tags"]
tagtransitioncount = model["transition"]
previosProbability = defaultdict(int)

raw_training_data = open(sys.argv[1],"r")
sentence = raw_training_data.readlines()

for tags in alltags:
	previosProbability[tags] = tagtransitioncount["start"][tags]
alltags.remove("start")

for count in range(len(sentence)):
	backpointer = [defaultdict(int)]
	wordtagmatrix = [defaultdict(int)]
	wordtag = sentence[count].replace('\n','').split(" ")
	newlytaggedwords = []
	tagger = ""   
	maxval = -1000
	states = alltags
	length = len(wordtag) -1
	if wordtag[0] in wordtaginformation:
		tagsofword = wordtaginformation[wordtag[0]]
		for tag in tagsofword:
			if (tag in previosProbability  and previosProbability[tag] != 0):
				wordtagmatrix[0][tag] = previosProbability[tag] + wordtaginformation[wordtag[0]][tag]
	else:
		for tag in alltags:
			if tag in previosProbability  and previosProbability[tag] != 0:
				wordtagmatrix[0][tag] = previosProbability[tag]

	if(len(wordtag) > 1):
		for index in range(1,len(wordtag)):
			wordtagmatrix.append(defaultdict(int))
			backpointer.append(defaultdict(int))
			if wordtag[index] in wordtaginformation:
				tagsofword = wordtaginformation[wordtag[index]]
				for tag in tagsofword:
					maxProbability = -1000
					for t in alltags:
						if t in wordtagmatrix[index-1] and wordtagmatrix[index-1][t] != 0:
							currentprob = wordtagmatrix[index-1][t] + tagtransitioncount[t][tag] + wordtaginformation[wordtag[index]][tag]
							if maxProbability <= currentprob:
								maxProbability = currentprob
								backpointer[index][tag] = t
					wordtagmatrix[index][tag] = maxProbability
			else:
				for tag in alltags:
					maxProbability = -1000 
					for t in  alltags:
						if((t in wordtagmatrix[index-1]) and wordtagmatrix[index-1][t] != 0):
							currentprob = wordtagmatrix[index-1][t] + tagtransitioncount[t][tag]
							if maxProbability <= currentprob:
								maxProbability = currentprob
								backpointer[index][tag] = t
					wordtagmatrix[index][tag] = maxProbability

	print wordtagmatrix
	if wordtag[length] in wordtaginformation:
	        states = wordtaginformation[wordtag[length]]
	        
	for i in states:
		if maxval <= wordtagmatrix[length][i]:
			maxval = wordtagmatrix[length][i]
			tagger = i
	    
	newlytaggedwords.append(wordtag[length]+"/"+tagger)

	for t in range(len(wordtag) - 2, -1, -1):
		if tagger not in backpointer[t+1]:
			for i in alltags:
				if i in backpointer[t+1]:
					tagger = backpointer[t+1][i]
					break;
		else:
			tagger = backpointer[t+1][tagger]
		newlytaggedwords.append(wordtag[t]+"/"+tagger)

	for i in range(len(newlytaggedwords)-1, -1, -1):
		output.write(str(newlytaggedwords[i])+" ")
	output.write("\n")



