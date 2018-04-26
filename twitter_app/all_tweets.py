from collections import Counter
import nltk
import tweepy
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
import requests
import json

from nltk.tokenize import sent_tokenize
import json
from pprint import pprint
import datetime as dt
import time
import os
import sys
from netaddr import *
import re

################### TWITTER BAGLANTI #############################################

consumer_key = "YtFLOwF6x2HRc2urZyzjqF326"
consumer_secret = "xb5zF97HP3scRFv66utqsG3ufrQrnrund1GICflruVAeNvtQZM"
access_key = "474099485-Vygs5EG6JiKuZ511sPNcooJM0SQ9S85nhQTzkjkU"
access_secret = "Or6R8VroT78F5wwQP48d3uztWrqFKxGyQZraw4eyt8vSV"

baslik = {
'Authorization': 'Token 00d2e3a10c82420414b2d36d28fb5afc2cd8e8a5',
'Content-Type': 'application/json'
}


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

stop_words = set(stopwords.words('turkish'))
stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','@','#','http','https','//','``',"''",'...','/','..','_','-'])
url = "https://api.cognitus.ai/api/v1/sentiment"
#################### TUM TWEETLER ###############################################


def All_Tweets(api,username):

    user =api.get_user(username)
    screenname=user.screen_name.encode('utf+8')

    print(str(user.statuses_count))

    page = 1
    tweets = 0
    tweet_text=[]
    info=[]
    data=[]
    while True:
     new_tweets = api.user_timeline(screen_name=screenname, include_rts=True, count=100,page=page)

     with open('tweetlerSum.txt', 'a') as out:
         if new_tweets:
            for tweet in new_tweets: #'type=tweepy.models.Status'
                tweets+=1
                info.append(tweet)
                if hasattr(tweet,'retweeted_status'):
                      #out.write(tweet.retweeted_status.text + '\n')
                      #print(tweet.retweeted_status.text)
                      tweet_text.append(tweet.retweeted_status.text)
                else:
                      #print(tweet.text)
                      #out.write(tweet.text + '\n')
                      tweet_text.append(tweet.text)
         else:
             break
         page+=1
     dir(info)
    clean_data=[]
    for tweet in tweet_text:
        item = ' '.join(word.lower() for word in tweet.split() \
            if not word.startswith('#') and \
               not word.startswith('@') and \
               not word.startswith('http') and \
               not word.startswith('RT'))
        if item == "" or item == "RT":
            continue
        clean_data.append(item)


    countpoz=0
    countneg=0
    countnotr=0
    for tweet in clean_data:

          veri = {"text": tweet}
          if (requests.post(url, json=veri, headers=baslik).json())["polarity"] > 0 :
              #print(veri["text"] ,":", "pozitif")
              countpoz+=1
          elif (requests.post(url, json=veri, headers=baslik).json())["polarity"] < 0:
              #print(veri["text"] ,":", "negatif")
              countneg+=1
          else:
              countnotr+=1


    print(countpoz,countneg,countnotr)
    return tweet_text


if name == '__main__':
    account_name = "iusiber"

    All_Tweets(api,account_name)
