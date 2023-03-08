import os
import tweepy
import time
# Authenticate to Twitter
# consumer key and consumer secret
auth = tweepy.OAuthHandler("wP7pxb7YXCZvGAdCiBvengM63", "oGPDfbvuTuqSyZVwj7HmmzreAxKbvSwSjf4IXBYnV4bL6nM63e")
# access token and access token 
secretauth.set_access_token("1253258850922311680-EkI5cokGDsBm8JwpqfOFid6W1sVJ8E", "NELpUgEpCG4BXJIk5cP8kIm5JClhPZA4ZZLDFeMJ8Vt3U")
# Create API 
objectapi = tweepy.API(auth)
# Hello World example
# api.update_status("Hello Tweepy")
# Read lines from txt
lines = []
with open('quotes.txt') as f:    
    lines = f.readlines()
for line in lines:    
    # Quote fits in one single tweet. No thread necesary    
    if (len(line) <= 273 and len(line)>4):         
        api.update_status(f'{line} #quote')        
        time.sleep(3600)
    # Thread necesary    
    elif (len(line)>=2):        
        words = line.split(" ")        
        tweet = ""        
        i = 0        
        next = True        
        while next and i < len(words):   
            if(len(tweet+words[i])<273):
                tweet = tweet+" " + words[i]                
                i += 1
            else:                
                next = False        
        original = api.update_status(f'{tweet}...')        
        old = original.id        
        tweet = ""        

        while i < len(words):                
            if(len(tweet+words[i])<273):                    
                tweet = tweet +" " + words[i]                    
                i += 1                
            else:                    
                reply = api.update_status(status=f'...{tweet}...', in_reply_to_status_id=old, auto_populate_reply_metadata=True)                    
                tweet = ""                    
                old = reply.id        
        if(tweet!=""):                
            reply = api.update_status(status=f'...{tweet}', in_reply_to_status_id=old, auto_populate_reply_metadata=True)                
            tweet = ""        
        time.sleep(3600)
