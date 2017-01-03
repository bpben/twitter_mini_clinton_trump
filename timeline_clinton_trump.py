# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 22:21:42 2016
#Retrieves tweets on Clinton/Trump timelines

@author: bpben
"""

from twitter import *
import json
import os
import time
import cPickle

#Working directory
os.chdir(r'')

#Twitter API stuff
token = 	''
token_secret = ''
consumer_key = ''
consumer_secret = ''

auth=OAuth(token, token_secret, consumer_key, consumer_secret)

tauth = Twitter(auth = auth)

users = ['realDonaldTrump', 'HillaryClinton']

def gettimeline(user, num):
    if num>200:
        print('Specified number of tweets too high, defaulting to max (200)')
        num = 200
    tweetset = set()
    data = []
    print('Retrieving most recent {} tweets for {}').format(num,user)
    new = tauth.statuses.user_timeline(screen_name=u, 
        include_rts=True, count=num)
    for t in new:
        if t['id'] not in tweetset:
            data.append(t)
    print('Retrieved {} tweets').format(len(data))
    return(data)

def savepickle(data, user, filename): 
    with open('./'+user+'.pkl', 'w') as f:
        data = cPickle.dump(data, filename)

for u in users:
    data = gettimeline(u, 200)
    savepickle(data, u, u+'.pkl')