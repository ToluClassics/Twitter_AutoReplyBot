import json
import sys
import tweepy
import importlib
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import json
import os
import boto3

ssm = boto3.client('ssm')
TEXT = os.environ.get('TEXT')
HANDLES = os.environ.get('HANDLES')

#this handles the authentication to the twitter streaming API
class Authentication():
  def __init__(self,CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET):
    self.CONSUMER_KEY = CONSUMER_KEY
    self.CONSUMER_SECRET = CONSUMER_SECRET
    self.ACCESS_TOKEN = ACCESS_TOKEN
    self.ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET

  def authenticate(self):
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    return auth

#this class is used to streamline tweets to user timelines
class TwitterClient():
  def __init__(self,twitter_user=None):
    self.auth = Authentication(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET).authenticate()
    self.twitter_client = API(self.auth)
    self.twitter_user = twitter_user

  def get_timeline_tweets(self,num_tweets):
    tweets = []
    for tweet in Cursor(self.twitter_client.user_timeline,id =self.twitter_user ).items(num_tweets):
      tweets.append(tweet)
    
    return tweets

  def get_twitter_api(self):
    return self.twitter_client

  def get_friend_list(self,num_friends):
    friends = []
    for friend in Cursor(self.twitter_client.friends,id =self.twitter_user).items(num_friends):
      friends.append(friend)
    
    return friends

  def get_hometimeline_tweets(self,num_tweets):
    home_tweets = []
    for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
      home_tweets.append(tweet)
    
    return home_tweets

class TwitterStreamer():
  """
  Class that streams tweets and processes them
  """
  def stream_tweets_user(self,tweet_filename,location_list,auth):

    listener = StdOutListener(tweet_filename)
    auth = auth.authenticate()

    stream = Stream(auth,listener)
    stream.filter(locations=location_list)

  def stream_tweets_keywords(self,tweet_filename,keyword_list,auth):
 
    listener = StdOutListener(tweet_filename)
    auth = auth.authenticate()

    stream = Stream(auth,listener)
    stream.filter(track=keyword_list)

#Define a class that inherits from the stream listener class
class StdOutListener(StreamListener):
  """
  Class that prints the listened tweets to command lline
  """
  def __init__(self,tweet_filename):
    self.tweet_filename = tweet_filename

  def on_data(self,data):
    try:
      #print(data)
      #write the tweets to a json file
      with open(self.tweet_filename,'a') as tf:
        tf.write(data)
    except BaseException as e:
      print(str(e))
    return True
  
  def on_error(self,status):
    #return False in case of a twiitter limit error
    if status == 420:
      return False
    print(status)

#function to get variables from parameter store
def get_parameter(param_name):
    response = ssm.get_parameter(Name=param_name,WithDecryption=True)
    credentials = response['Parameter']['Value']
    return credentials

def lambda_handler(event, context):
    
    #retrieve parameters
    ACCESS_TOKEN = get_parameter('/TwitterBot/access_token')
    ACCESS_TOKEN_SECRET = get_parameter('/TwitterBot/access_token_secret')
    CONSUMER_SECRET = get_parameter('/TwitterBot/Consumer_Secret')
    CONSUMER_KEY = get_parameter('/TwitterBot/Consumer_key')
    
    
    #authenticate tweepy
    auth = Authentication(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    twitter_streamer = TwitterStreamer()
    twitterApi = API(auth)
    
    accounts = HANDLES.split(",")
    
    for account in accounts:
      twitter_client = TwitterClient(account)
      user_tweets=twitter_client.get_timeline_tweets(10)
      
      user_id = user_tweets[0].id
      
      for tweet in user_tweets:
        TWEET_ID = str(tweet.id)
        tweet = twitterApi.get_status(TWEET_ID)
        comment = TEXT
        try:
          res = twitterApi.update_status(comment, in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True)
        except:
          print("No New Tweet")
    
    
    