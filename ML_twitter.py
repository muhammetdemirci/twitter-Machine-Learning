#-*- coding: utf-8 -*-
import pandas as pd
from io import StringIO
import requests
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv

def read_and_merge_userTweet(users):
    allUser = []
    for user in users:
        frame = pd.read_csv('Users/%s/tweets.csv' % user)
        userTweets = ""
        for i in range(0, frame["text"].size):
            userTweets += ". " + frame["text"][i]
        alltweets = "".join(userTweets.split("\n"))
        allUser.append([user, alltweets])



    with open('Users/alltweets.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["screen_name","alltweets"])
		writer.writerows(allUser)


if __name__ == '__main__':
    users = []

    read_and_merge_userTweet(users)
    frame = pd.read_csv('Users/alltweets.csv')
    
    corpus = []
    for i in range(0, frame["alltweets"].size):
        corpus.append(frame["alltweets"][i])    
    
    # Create tf–idf matrix
    vectorizer = TfidfVectorizer(stop_words = 'english', min_df = 0.2)
    # min_df = 0.2 means that the term must be in at least 20% of the documents
    X = vectorizer.fit_transform(corpus)
    
    k = 2 # Define the number of clusters in which we want to partion our data
    # Define the proper notion of distance to deal with documents
    dist = 1 - cosine_similarity(X)
    # Run the algorithm kmeans
    model = KMeans(n_clusters = k)
    model.fit(X);

    no_words = 4 # Number of words to print per cluster
    order_centroids = model.cluster_centers_.argsort()[:, ::-1] # Sort cluster centers by proximity to centroid
    terms = vectorizer.get_feature_names()
    labels = model.labels_ # Get labels assigned to each data

    for i in range(k):
    
        print "group ",i," users: ",
        for title in frame["screen_name"][labels == i]:
        	print title," ",
        print "" #add a whitespace


        print "group  ",i," users: ",
        for ind in order_centroids[i, :no_words]:
        	print terms[ind]," ",
        print ""
        print ""
