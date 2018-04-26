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



def main(user):
	page = 1
	tweets = 0
	user = api.get_user(user)
	screenname=user.screen_name.encode('utf+8')
	new_tweets = api.user_timeline(screen_name=screenname, include_rts=True, count=100,page=page)
	tweet_array = []
	for i in new_tweets:
		tweets_dict = {}
		tweets_dict['tweet']=i.text
		tweets_dict['tarih']=i.created_at
		tweet_array.append(tweets_dict)
		del(tweets_dict)
	for i in tweet_array:########multithread
		item = ' '.join(word.lower() for word in i['tweet'].split() \
		if not word.startswith('#') and \
			not word.startswith('@') and \
			not word.startswith('http') and \
			not word.startswith('RT'))
		if item == "" or item == "RT":
			continue
		i['tweet'] = item
	polarite_dict ={}
	polarite_dict['Pozitif'] = 0
	polarite_dict['Negatif'] = 0
	polarite_dict['Notr'] = 0
	for i in tweet_array:
		veri = {'text':i['tweet']}
		y = requests.post(url, json=veri, headers=baslik).json()["polarity"]
		if y > 0:
			i['polarite'] = 'Pozitif'
			polarite_dict['Pozitif'] +=1
		elif y < 0:
			i['polarite'] = 'Negatif'
			polarite_dict['Negatif'] +=1
		elif y == 0:
			i['polarite'] = 'Notr'
			polarite_dict['Notr'] +=1

	return polarite_dict, tweet_array
