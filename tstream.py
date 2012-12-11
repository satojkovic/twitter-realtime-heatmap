import tweepy
import json
from pymongo import Connection
from bson import json_util
from tweepy.utils import import_simplejson

from pit import Pit

json = import_simplejson()
mongocon = Connection()

db = mongocon.tstream
col = db.tweets_tail

config = Pit.get('twitter.com', {'require': {'ConsumerKey':'', 'ConsumerSecret':'',  'AccessToken':'', 'AccessTokenSecret':'' }})

auth1 = tweepy.OAuthHandler(config['ConsumerKey'], config['ConsumerSecret'])
auth1.set_access_token(config['AccessToken'], config['AccessTokenSecret'])

class StreamListener(tweepy.StreamListener):
    mongocon = Connection()
    db = mongocon.tstream
    col = db.tweets
    json = import_simplejson()

    
    def on_status(self, tweet):
        print 'Ran on_status'

    def on_error(self, status_code):
        return False

    def on_data(self, data):
        if data[0].isdigit():
            pass
        else:
            col.insert(json.loads(data))
            print(json.loads(data))


l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
setTerms = ['bigdata', 'devops', 'hadoop', 'twitter']
streamer.filter(track = setTerms)
