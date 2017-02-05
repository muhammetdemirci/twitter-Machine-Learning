#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import time
import os

#Twitter API credentials
consumer_key = "--"
consumer_secret = "--"
access_key = "--"
access_secret = "--"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#initialize a list to hold all the tweepy Tweets
	alltweets = []

	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
	alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print "...%s tweets downloaded of " % (len(alltweets)),screen_name

	#transform the tweepy tweets into a 2D array that will populate the csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
	with open('Users/%s/tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	pass

def get_all_followers(screen_name):

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	allFollowersUserName = []
	allFollowersUserName = [[user.screen_name] for user in  handle_errors(tweepy.Cursor(api.followers,screen_name=screen_name).items())]

	with open('Users/%s/tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["screen_name"])
		writer.writerows(allFollowersUserName)

	print screen_name," has ",len(allFollowersUserName)," followers"
	pass


def handle_errors(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.TweepError:
            time.sleep(20 * 60)

if __name__ == '__main__':

	users = []
	for user in users:
		newpath = r'Users/%s' %user
		if not os.path.exists(newpath):
			os.makedirs(newpath)
		get_all_tweets(user)
