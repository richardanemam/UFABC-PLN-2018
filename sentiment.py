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
		tweet_list = []

		for tweet in tweepy.Cursor(self.api.search, q=hashtag, lang="en").items(100):
			
			clean_tweet = self.removeNoiseTweet(tweet.text)
			noStopWords_tweet = self.removeStopWords(str(clean_tweet))

			tweet_list.append([tweet for tweet in noStopWords_tweet])

		return (tweet_list)



	def printData(self, tweet_list):
		for i in range(0, 100):
			print (tweet_list[i])

	def bagOfWords(self, tweet_list):
		
		#Transforma uma lista de listas em uma unica lista
		#The piece of code below means
		#for sublist in l:
			#for item in sublist:
		#flat_list.append(item)
		
		flat_tweet_list = [tweet for sublist in tweet_list for tweet in sublist]
		
		return flat_tweet_list

	def get_sentiment(self, tweet_list):
		
		tweet_str = ' '.join(tweet_list)
		
		blob = TextBlob(tweet_str)

		if blob.sentiment.polarity > 0:
			return 'positive'
		elif blob.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'
		
def main():
	
	nsa = SentmentAnalysis()
	get_tweet_list = nsa.getData(hashtag="#blackpanter")
	get_bag = nsa.bagOfWords(get_tweet_list)
	
	pt = 0
	nt = 0
	ng = 0
	
	for i in range(0, 99):
		

		sentiment = nsa.get_sentiment(get_tweet_list[i])
		if(sentiment == 'positive'):
			pt += 1
		elif (sentiment == 'neutral'):
			nt += 1
		else:
			ng += 1

	# percentagem of negative tweets
	print("Positive tweets percentage: {0} %".format(100*(pt/100)))
	
	# percentage of negative tweets
	print("Negative tweets percentage: {0} %".format(100*(ng/100)))
	# percentage of neutral tweets
	print("Neutral tweets percentage: {0} %".format(100*(nt/100)))


if __name__ == "__main__":
	main()
