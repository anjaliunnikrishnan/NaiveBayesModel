# from __future__ import division

import math as m
import time
import sys
import re
import string
import pdb
import json
import re

file = open(sys.argv[1], 'r')

# file = open('sample.txt', 'r')
training_file = file.read()

training_file = training_file.strip()
training_file = training_file.split("\n")

pos_tag = 0
neg_tag = 0
true_tag = 0
fake_tag = 0
true_big_doc = []
fake_big_doc = []
pos_big_doc = []
neg_big_doc = []
pos_or_neg = ''
true_or_fake = ''
document_count = len(training_file)

word_given_pn = {}
word_given_tf = {}
identifiers = []
stopwords = set(["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"])
# punctuations = ['.', '!', '?', '--', '/', ':', '(', ')', '<', '>', '[', ']', ';', '"', ',', '+', '=', '*', '@', '#', '$', '%', '&', '~']
uniqueWords = []
alldocs = []
for i in range(document_count):
    temp_sentence = training_file[i].strip()  
    temp_sentence = temp_sentence.strip().lower()
    temp_sentence = re.sub('[!#"%$&)(+*-,/.;:=<?>@\[\]~]',' ',temp_sentence)
    
    # print(temp_sentence)
    
    temp_words = temp_sentence.split(' ')
    
  #   print(temp_words[1])
#     print(temp_words[2])
    
    if temp_words[1]=='fake':
    	fake_big_doc.append(temp_sentence)
        fake_tag += 1
    
    else:
    	true_big_doc.append(temp_sentence)
        true_tag += 1
        
    if temp_words[2]=='neg':
    	neg_big_doc.append(temp_sentence)
        neg_tag += 1
        
    else:
		pos_big_doc.append(temp_sentence)
		pos_tag += 1
    
    for word in temp_words:			
        if word not in uniqueWords and word not in stopwords:
        	uniqueWords.append(word)
       
# print('Done Adding')
# print(pos_big_doc)

pos_word_count = 0
neg_word_count = 0
true_word_count = 0
fake_word_count = 0

prior_probability = {}
# print(document_count)
prior_probability['pos'] = m.log(pos_tag/float(document_count))
prior_probability['neg'] = m.log(neg_tag/float(document_count))
prior_probability['true'] = m.log(true_tag/float(document_count))
prior_probability['fake'] = m.log(fake_tag/float(document_count))

# preprocessing of data - getting word count for each class
word_count = {}
def word_counts(tag, bigdoc):
	tag_count = 0
	for line in bigdoc:
# 		print line
		words = line.strip().split(' ')[3:]
		for word in words:
			if word not in stopwords:
# 				print(# word)
				if word not in word_count:
					word_count[word] = {}
					word_count[word][tag] = 1
				elif word in word_count and tag in word_count[word]:
					word_count[word][tag] += 1
				elif word in word_count and tag not in word_count[word]:
					word_count[word][tag] = 1
				tag_count += 1
	return tag_count


pos_word_count = word_counts("pos", pos_big_doc) 
neg_word_count = word_counts("neg", neg_big_doc) 
true_word_count = word_counts("true", true_big_doc) 
fake_word_count = word_counts("fake", fake_big_doc)     

# print len(uniqueWords),pos_word_count,neg_word_count

# print word_count['pleasurable'],'wordcount'
word_count_temp = dict()
for key in word_count:
	for subkey in word_count[key]:
		if subkey == 'pos':
			if 'neg' not in word_count[key]:
				if key not in word_count_temp:
					word_count_temp[key] = {}
				word_count_temp[key]['neg'] = 1
		if subkey == 'neg':
			if 'pos' not in word_count[key]:
				if key not in word_count_temp:
					word_count_temp[key] = {}
				word_count_temp[key]['pos'] = 1
		if subkey == 'true':
			if 'fake' not in word_count[key]:
				if key not in word_count_temp:
					word_count_temp[key] = {}
				word_count_temp[key]['fake'] = 1
		if subkey == 'fake':
			if 'true' not in word_count[key]:
				if key not in word_count_temp:
					word_count_temp[key] = {}
				word_count_temp[key]['true'] = 1

# print word_count_temp['pleasurable']
for key in word_count_temp:
	for subkey in word_count_temp[key]:
		if key in word_count and subkey not in word_count[key]:
			word_count[key][subkey] = word_count_temp[key][subkey]




# print 'inroom' in uniqueWords#,word_count['inroom']
for key in word_count:
	for subkey in word_count[key]:
		if subkey == 'pos':
			word_count[key][subkey] = m.log((word_count[key][subkey] + 1)*1.0 / (len(uniqueWords) + pos_word_count))
		if subkey == 'neg':
			word_count[key][subkey] = m.log((word_count[key][subkey] + 1)*1.0 / (len(uniqueWords) + neg_word_count))
		if subkey == 'true':
			word_count[key][subkey] = m.log((word_count[key][subkey] + 1)*1.0 / (len(uniqueWords) + true_word_count))
		if subkey == 'fake':
			word_count[key][subkey] = m.log((word_count[key][subkey] + 1)*1.0 / (len(uniqueWords) + fake_word_count))

stopword = open("nbmodel1.txt","w")
for word in stopwords:
	stopword.write(word + '\n')
stopword.close()

allwords = open("nbmodel2.txt","w")
for word in uniqueWords:
	allwords.write(word + '\n')
allwords.close()

probabilities = open("nbmodel3.txt","w")
probabilities.write(str(prior_probability['pos']) + ' ' + str(prior_probability['neg']) + ' ' + str(prior_probability['true']) + ' ' + str(prior_probability['fake']) + '\n')
for key in word_count:
	for subkey in word_count[key]:
		probabilities.write(key + ' ' + subkey + ' ' +  str(word_count[key][subkey]) + '\n')
probabilities.close()
# test_file = open('dev-text.txt', 'r').read().splitlines()

# for line in test_file:
# 	line = re.sub('[!#"%$&)(+*-,/.;:=<?>@\[\]~]',' ',line)
# 	print line.split(' ')[0],
# 	words = line.split(' ')[1:]
# 	pos_prob = prior_probability['pos']
# 	neg_prob = prior_probability['neg']
# 	true_prob = prior_probability['true']
# 	fake_prob = prior_probability['fake']

# 	for word in words:
# 		word = word.lower()
# 		if (word not in stopwords) and (word in uniqueWords):
# 			pos_prob += word_count[word]['pos']
# 			neg_prob += word_count[word]['neg']
# 			true_prob += word_count[word]['true']
# 			fake_prob += word_count[word]['fake']

# 	if max(true_prob,fake_prob) == true_prob:
# 		print "True",
# 	else:
# 		print "Fake",

# 	if max(pos_prob,neg_prob) == pos_prob:
# 		print "Pos"
# 	else:
# 		print "Neg"

	


