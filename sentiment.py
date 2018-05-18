import tweepy
import os
import re
import string
from nltk.tokenize import TweetTokenizer
from stop_words import get_stop_words
from tweepy import OAuthHandler
from dotenv import load_dotenv, find_dotenv
from collections import Counter
from textblob import TextBlob
import matplotlib.pyplot as plt


class SentmentAnalysis:
	def __init__(self):
		
		self.dotenv_path = find_dotenv()
		load_dotenv(self.dotenv_path)
 
		self.CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
		self.CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
		self.ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
		self.ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

		try:
			self.auth = OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
			self.auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")


	def tweetTokenize(self, tweet):
		tknzr = TweetTokenizer()
		return (tknzr.tokenize(tweet))


	def removeNoiseTweet(self, tweet):
		#Convert to lower case
		tweet = tweet.lower()
		
		#Convert www.* or https?://* to URL
		tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL', tweet)
		
		#Convert @username to AT_USER
		tweet = re.sub('@[^\s]+','AT_USER', tweet)
		
		#Remove additional white spaces
		tweet = re.sub('[\s]+', ' ', tweet)
		
		#Replace #word with word
		tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
		
		return tweet 


	def removeStopWords(self, tweet):
		punctuation = list(string.punctuation)
		tweet_token = self.tweetTokenize(tweet) 
		stop_words = get_stop_words('english') + punctuation + ['rt', 'via', 'URL', 'AT_USER']
		w_stop = [w for w in tweet_token if w not in stop_words]
		return w_stop


	def getData(self, hashtag):
		tweetList = []
		
		for tweet in tweepy.Cursor(self.api.search, q=hashtag, lang="en").items(2000):
			tweetList.append(tweet.text)

		return (tweetList)


	def printData(self, cleanTweetList, tweetList, pt, nt, ng):
		
		
		for i in range(1, 2000):
			print('==========================================')
			print (tweetList[i], '\n')
			print(cleanTweetList[i])
			print('==========================================')

		# percentage of negative tweets
		print("Positive tweets percentage: {0} %".format(100*(pt/2000)))
	
		# percentage of negative tweets
		print("Negative tweets percentage: {0} %".format(100*(ng/2000)))
		
		# percentage of neutral tweets
		print("Neutral tweets percentage: {0} %".format(100*(nt/2000)))

	
	def bagOfWords(self, tweet_list):
		
		#Transforma uma lista de listas em uma unica lista
		#The piece of code below means
		#for sublist in l:
			#for item in sublist:
		#flat_list.append(item)
		
		flat_tweet_list = [tweet for sublist in tweet_list for tweet in sublist]
		
		return flat_tweet_list


	def get_sentiment(self, tweet):
		
		#transforma uma lista de tokens em uma unica string
		tweet_str = ' '.join(tweet)
		
		#Cria um objeto textblob do tweet passado como parâmetro
		blob = TextBlob(tweet_str)

		#Determina o sentimento do tweet
		if (blob.sentiment.polarity > 0):
			return 'positive'
		elif (blob.sentiment.polarity == 0):
			return 'neutral'
		else:
			return 'negative'

	
	def showCategoricalData(self, pt, nt, ng, hashtag):
		data = {
			'Positive': pt,
			'Negative': ng,
			'Neutral': nt
		}

		names = list(data.keys())
		values = list(data.values())

		fig, axs = plt.subplots(figsize=(6, 3))
		axs.bar(names, values)
		fig.suptitle(hashtag)	
		plt.xlabel("Sentimento")
		plt.ylabel("Quantidade")
		plt.show()

def main():
	
	nsa = SentmentAnalysis()
	
	pt = 0
	nt = 0
	ng = 0
	hashtag="#BestAdviceYourMomGave"

	cleanTweetList = []
	tweetList = nsa.getData(hashtag)
	
	for tweet in tweetList:
		cleanUpTweet = nsa.removeNoiseTweet(tweet)
		cleanTweet = nsa.removeStopWords(cleanUpTweet)
		cleanTweetList.append(cleanTweet)
	
	for i in range(1, 2000):
		
		sentiment = nsa.get_sentiment(cleanTweetList[i])
		
		if(sentiment == 'positive'):
			tweetList[i] = 'Positive: '+ tweetList[i]
			pt += 1
		elif (sentiment == 'neutral'):
			tweetList[i] = 'Neutral: '+ tweetList[i]
			nt += 1
		else:
			tweetList[i] = 'Negative: '+ tweetList[i]
			ng += 1

	nsa.showCategoricalData(pt, nt, ng, hashtag)
	nsa.printData(cleanTweetList, tweetList, pt, nt, ng)
	
if __name__ == "__main__":
	main()

	#clean_tweet = self.removeNoiseTweet(tweet.text)
	#noStopWords_tweet = self.removeStopWords(str(clean_tweet))
	#tweet_list.append([tweet for tweet in noStopWords_tweet])