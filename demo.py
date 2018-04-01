import tweepy
import os
from tweepy import OAuthHandler
from dotenv import load_dotenv, find_dotenv


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
 
api = tweepy.API(auth)

def myTimeLine(myStatus):
	api.update_status(status = myStatus)

def getStatus():
	for status in tweepy.Cursor(api.home_timeline).items(10):
		print(status.text)
		 
#for status in tweepy.Cursor(api.home_timeline).items(10):
	# Process a single status
	#process_or_store(status._json)

def getMyFollowers():
	for friend in tweepy.Cursor(api.friends).items():
		print(friend._json)

def getMyTweets():
	for tweet in tweepy.Cursor(api.user_timeline).items():
		print(tweet._json) 

def main():
		
	myStatus = "Hello World! My name's is Richard"
	#myTimeLine(myStatus)

	getStatus()
	getMyTweets()

if __name__ == "__main__":
	main()