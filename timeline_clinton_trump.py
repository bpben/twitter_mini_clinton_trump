# -*- coding: utf-8 -*-
"""
Created on Mon Nov 07 22:21:42 2016
#Retrieves last x tweets on Clinton/Trump timelines

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

tweetSets = {}
tweetSets['realDonaldTrump'] = set()
tweetSets['HillaryClinton'] = set()

#Get most recent x tweets (max is 200)
x = 200
for u in ['realDonaldTrump','HillaryClinton']:
    new = tauth.statuses.user_timeline(screen_name=u, include_rts=True, count=x)
    for t in new:
        if t['id'] not in tweetSets[u]:                
            if os.path.isfile('./'+u+'.pkl'):
                with open('./'+u+'.pkl') as f:
                    data = cPickle.load(f)
                data.append(t)
                print "Have {} tweets".format(len(data))
            else:
                data = []                    
                data.append(t)
            with open('./'+u+'.pkl', 'w') as f:
                cPickle.dump(data, f)
            tweetSets[u].add(t['id'])