'''
#################################################
#	NLTK Wrapper								#
#   Written Spring 2015 in Urbana-Champaign		#
#	By Morgan Bentell							#
#	Using Python 3 and the NLTK Library			#
#################################################
'''
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.util import ngrams
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import reuters
from nltk.tokenize import TreebankWordTokenizer
import os
stemmer = SnowballStemmer("english")
goodList = open("./dicts/goodStemmed.txt").read().split('\n')
badList = open("./dicts/badStemmed.txt").read().split('\n')
negationList = open("./dicts/negations.txt").read().split('\n')
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

# Description: Word class that holds information about the word such as its stemmed representation, POS-tag, negation information (True/False)
# and sentiment weight represented either as +1, 0 or -1 depending on whether the word is found in a dictionary of positive words.
# It may be found in either, both or none of the dictionaries. 
class Word():

	# Description: Constructor that initializes the properties of the word by calling the appropriate methods
	#
	# @param w - the raw string representation of the word
	def __init__(self, w):
		self.original = w.upper()
		self.stemmed = stemmer.stem(w).upper()
		self.pos_tag = nltk.pos_tag([w])[0][1]
		self.setWeight()

	#Description: Sets the appropriate weight to a word (-1/0/+1) depending on the occurences in the respective dictionaries.
	def setWeight(self):
		self.negation = False
		self.econ = False
		self.weight = 0
		if self.stemmed in goodList:
			self.weight += 1
		if self.stemmed in badList:
			self.weight -= 1
		if self.stemmed in negationList:
			self.negation = True


# Description: Sentence class that contains a list of words in the sentence, and information metrics about the sentence
# such as number of words, number of positive and negative words and overall sentiment based on those numbers.
class Sentence():
	def __init__(self,s):
		self.words = []	
		self.numPosWords = 0
		self.numNegWords = 0
		self.original = s
		self.wordsFromSentence()
		self.sentiment = self.sentenceWeight(self.words)
		self.numberofwords = len(self.words)
		self.prop = self.sentiment/self.numberofwords

	#Description: Tokenizes the sentence and puts the tokens in a dictionary
	def wordsFromSentence(self):
		for word in TreebankWordTokenizer().tokenize(self.original):
			word = word.strip('`.,!\'";:#/&@?+()[]{}-\\\t\n1234567890')
			if word != "" and len(word) > 1:
				self.words.append(Word(word))

	# Description: Calculates the total sentiment weight of a sentence.
	# This method has a feature that can alter flip the sign of the rest of a sentence after encountering a negation word.
	# 
	# @param words - A list of words in a sentence
	#
	# @return returns ingeget sum of the individual weight of the words in a sentence.
	def sentenceWeight(self, words):
		
		#Base case
		if(words == []):
			return 0
		
		# This piece of code will swich the sign on the remainder of the article after a negation word.	
		# elif(words[0].negation):
		# 	return -1*self.sentenceWeight(words[1:len(words)])

		# Add the appropriate weight to the recursion call
		else:
			if(words[0].weight < 0):
				self.numNegWords += 1
			elif(words[0].weight > 0):
				self.numPosWords += 1
			return words[0].weight + self.sentenceWeight(words[1:len(words)])

# Description: Body class that will represent the body of a piece of text, or any collection of sentences.
class Doc():
	
	# Description: constructor that initializes the document properties and calls the approrpiate methods in order to do so.
	#
	# @param body - a raw string of the text to be processed into words and sentences
	def __init__(self, body):
		self.sentences = []
		self.sentenceWeight = 0
		self.numPosWords = 0
		self.numNegWords = 0
		self.numWords = 0
		self.raw = body
		self.sentenceTokenize()
		self.computeSentiment()
		self.numberOfSentences = len(self.sentences)
		self.prop = self.sentiment/self.numWords

	# Description: Divides the full document text into sentences and adds them to the objects sentence dictionary
	def sentenceTokenize(self):
		for s in sent_detector.tokenize(self.raw.strip()):
			self.sentences.append(Sentence(s))

	# Description: Computes the trivial sentiment of a document based on the number of positive and negative words in the document
	def computeSentiment(self):
		for s in self.sentences:
			self.numPosWords += s.numPosWords
			self.numNegWords -= s.numNegWords
			self.numWords += s.numberofwords
		self.sentiment = self.numPosWords + self.numNegWords

	# Descriptopn: Produces a textfile that outputs a breakdown of the document
	def breakdown(self):
		f = open("./breakdown.txt", 'w')
		for sentence in self.sentences:
			f.write("Sentence text: "+sentence.original+"\n")
			f.write("Sentence weight: "+str(sentence.sentiment)+"\n")
			f.write("Sentence breakdown: "+"\n")
			for word in sentence.words:
				f.write("\t"+word.stemmed + " " +str(word.weight)+"\n")
		f.write("Number of positive words: " + str(self.numPosWords)+"\n")
		f.write("Number of negative words: " + str(self.numNegWords)+"\n")
		f.write("Discrete score: "+str(self.sentiment)+"\n")
		f.write("Lengt normalized: "+str(self.prop)+"\n")



with open("./testnews/news1_bad.txt", encoding="utf-8", errors="ignore") as f:
	bad = Doc(f.read())
	print(bad.prop)
	bad.breakdown()



