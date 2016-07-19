
# coding: utf-8

# In[ ]:

#Script for collecting Follower information and ascertaining whether located in Boston
#Developed by: bpben
#Date: 12/28/15

#Requires that you have a twitter API account set up


# In[ ]:

import csv
import json
import requests
import tweepy
import datetime
import time
import re
import os
from collections import defaultdict
import operator


# In[ ]:

#Authorization info for Tweepy
atoken = 'xxx'
asecret = 'xxx'
ckey = 'xxx'
csecret = 'xxx'
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

#Path for output (id list, user data)
path = r''
os.chdir(path)

#List of users for which you want followers (exclude '@')
usernames = ['BostonCalendar','artsboston','globeevents','TheBostonCal']


# In[ ]:

#Follower extraction function - Writes folower userids to text file
#Specify number of followers in second argument, "full" if you want all followers (may take a while)
def getFollowers(users, option):
    if type(users) is not list:
        users = [users]
    for name in users:
        print "Getting {} followers of {}".format(option, name)
        api = tweepy.API(auth)
        ids = []
        if (option=='full')|(option=='Full'):
            option = float("inf")
        else:
            try:
                int(option)
            except:
                return('Number of followers is not numeric, try again')      
        for page in tweepy.Cursor(api.followers_ids,screen_name=name).pages():
            if len(ids)>option:
                print "Reached stop-point of {} ids, ending pull.".format(option)
                ids = ids[0:option]
                break
            else:
                ids.extend(page)
                time.sleep(30)
        f = open(path+'ids_{}.txt'.format(name),'w')
        for id in ids:
            f.write(str(id))
            f.write('\n')
        f.close()
        print "User ids writen to {}".format(path+'ids_'+name+'.txt')


# In[ ]:

getFollowers(usernames,100)


# In[ ]:

#User info extraction function
#Reads in id.txt file, creates list of returned data (for later parsing)
#Can specify number of users, "full" if you want all
#*Future version will be able to specify fields
def getUserInfo(infile, option):
    ids = set()
    f = open(infile,'r')
    for item in f.readlines():
        ids.add(unicode(item.strip('\n')))
    ids = list(ids)
    api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())
    print "Obtaining user info for {} users.".format(option)
    #If all, make option = infinity
    if (option=='full')|(option=='Full'):
        option = float("inf")
    else:
        try:
            int(option)
        except:
            return('Number of followers is not numeric, try again')
    #If subset, truncate id list
    if len(ids)>=int(option):
        ids = ids[0:int(option)]
        
    userInfo = []
    for user in ids:
        try:
            userInfo.append(api.get_user(user_id=user))
        except tweepy.TweepError as e:
            if e.message[0]['code'] == 88:
                print "Rate limit hit, pausing 15 minutes."
                time.sleep(60 * 15)
                continue
            else:
                print "Unknown error, stopping!"
                raise
        except StopIteration:
            print "Reached end of id list."
    return(userInfo)


# In[ ]:

info = getUserInfo(path+'ids_BostonCalendar.txt','10')


# In[ ]:

#Parse user info and export to CSV
#Provide list of dicts/jsons, field names and output file, will spit it out into csv
fields = ['id','description','location','time_zone']
def parseUser(data, fields, outfile):
    overwrite = raw_input('This will overwrite '+outfile+' Is that okay? (Y/N)')
    if (overwrite =='Y')|(overwrite =='y'):
        with open(outfile, 'w') as output:
                csvWriter = csv.writer(output, delimiter=',')
                csvWriter.writerow(fields)
        for user in data:
            u = []
            for field in fields:
                if field in user:
                    u.append(unicode(user[field]).encode('utf-8'))
                else:
                    u.append('')
            with open(outfile, 'ab') as output:
                csvWriter = csv.writer(output, delimiter=',')
                csvWriter.writerow(u)
    else:
        return('Stopping parse')


# In[ ]:

parseUser(info,fields,path+'test.csv')


# In[ ]:

#Localize user and export localized to CSV
#Provide list of dicts/jsons, field names, list of location words (e.g. "Boston") and output file
#Will search User descriptions and locations for the words
def localUser(data, fields, locwords, outfile):
    overwrite = raw_input('This will overwrite '+outfile+' Is that okay? (Y/N)')
    if (overwrite =='Y')|(overwrite =='y'):
        with open(outfile, 'w') as output:
                csvWriter = csv.writer(output, delimiter=',')
                csvWriter.writerow(fields)
        lcount = 0
        for user in data:
            u = []
            local = 0
            if type(locwords) is not list:
                locwords = [locwords]
            for loc in locwords:
                if (re.match('{}'.format(loc),str(user['description']),re.IGNORECASE)) or (re.match('{}'.format(loc),str(user['location']),re.IGNORECASE)):
                    local = 1
            if local == 1:
                for field in fields:
                    if type(field) is not list:
                        field = [field]
                    if field in user:
                        u.append(unicode(user[field]).encode('utf-8'))
                    else:
                        u.append('')
                with open(outfile, 'ab') as output:
                    csvWriter = csv.writer(output, delimiter=',')
                    csvWriter.writerow(u)
                lcount += 1
        print "Total {} of {} users localized.".format(lcount, len(data))
    else:
        return('Stopping parse')


# In[ ]:

neigh = ['Boston','Allston','Brighton','Back Bay','Beacon Hill','West End','Charlestown','Chinatown','Dorchester','Downtown','East Boston','Fenway','Kenmore','Hyde Park','Jamaica Plain','Mattapan','Mission Hill','North End','Roslindale','Roxbury','South Boston','South End','Bay Village','West Roxbury']
localUser(info,fields,neigh,path+'test2.csv')

