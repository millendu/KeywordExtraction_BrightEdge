from bs4 import BeautifulSoup
import urllib2
import bs4
import operator
import nltk
import sys
from urllib2 import urlopen
from bs4.element import Comment
from nltk.tokenize import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
from nltk.tokenize import RegexpTokenizer
from nltk import pos_tag

#urls = ['http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/','http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/','http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster']

def tagVisible(element):
	if element.parent.name in ['article', 'style', 'script', 'head', 'title', 'meta', '[document]']:
		return False
	if isinstance(element, Comment):
		return False
	return True

def filterText(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	texts = soup.findAll(text=True)
	visible_texts = filter(tagVisible, texts)
	return [visible_text.encode('utf8') for visible_text in visible_texts]

def analyzeText(visible_texts):
	keywords = {}
	for sentence in visible_texts:
		word_tokenized = word_tokenize(sentence)
		tagged = nltk.pos_tag(word_tokenized)
		for i in range(0,len(tagged)-1):
			keyword = ''
			present =0
			if tagged[i][1] =='JJ':
				if tagged[i+1][1] == 'NNP':
					keyword = tagged[i][0] + ' ' + tagged[i+1][0]
					try:
						keywords[keyword] = keywords[keyword] + 1
					except:
						keywords[keyword] = 1
				if tagged[i+1][1] == 'NNS':
					keyword = tagged[i][0] + ' ' + tagged[i+1][0]
					try:
						keywords[keyword] = keywords[keyword] + 1
					except:
						keywords[keyword] = 1
			if(tagged[i][1]=='VBG'):
				Key = tagged[i][0]
				j = i + 1
				if j == len(tagged):
					break
				while (tagged[j][1] == 'NN' or tagged[j][1] == 'NNP' or tagged[j][1] == 'NNS'):
					Key = Key + ' ' + tagged[j][0]
					present = 1
					j = j + 1
					if j == len(tagged):
						break
				if(present != 0):
					try:
						keywords[keyword] = keywords[keyword] + 1
					except:
						keywords[keyword] = 1
	return keywords

def main(url):
	visible_text = filterText(url)
	output = analyzeText(visible_text)
	sorted_output = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
	top_10_keywords = []
	for word in sorted_output:
		if word[0] == '':
			continue
		top_10_keywords.append(word[0])
		if len(top_10_keywords) == 10:
			break
	return top_10_keywords

if __name__ == "__main__":
	if(len(sys.argv) == 1 ):
		print('Url is not specified.. Please specify the url')
		sys.exit()
	print(main(sys.argv[1]))




