import sys
import re

test_file = open(sys.argv[1], 'r').read().splitlines()
out1 = open("nboutput.txt","w")
stopwords  = set(open("nbmodel1.txt",'r').read().splitlines())
uniqueWords = set(open("nbmodel2.txt",'r').read().splitlines())
probs = open("nbmodel3.txt","r").read().splitlines()

prior_probability = dict()
probz = probs[0].split(' ')
prior_probability['pos'] = float(probz[0])
prior_probability['neg'] = float(probz[1])
prior_probability['true'] = float(probz[2])
prior_probability['fake'] = float(probz[3])
word_count = dict()
probs = probs[1:]
for line in probs:
	line = line.split(' ')
	if line[0] in word_count:
		word_count[line[0]][line[1]] = float(line[2])
	else:
		word_count[line[0]] = dict()
		word_count[line[0]][line[1]] = float(line[2])

for line in test_file:
	pos_prob = prior_probability['pos']
	neg_prob = prior_probability['neg']
	true_prob = prior_probability['true']
	fake_prob = prior_probability['fake']

	line = re.sub('[!#"%$&)(+*-,/.;:=<?>@\[\]~]',' ',line)
	out1.write(line.split(' ')[0] + ' ')
	words = line.split(' ')[1:]
	

	for word in words:
		word = word.lower()
		if (word not in stopwords) and (word in uniqueWords):
			pos_prob += word_count[word]['pos']
			neg_prob += word_count[word]['neg']
			true_prob += word_count[word]['true']
			fake_prob += word_count[word]['fake']

	if max(true_prob,fake_prob) == true_prob:
		out1.write("True ")
	else:
		out1.write("Fake ")

	if max(pos_prob,neg_prob) == pos_prob:
		out1.write("Pos" + '\n')
	else:
		out1.write("Neg" + '\n')
