import os
import tweepy
import time
from dotenv import load_dotenv

# Loads env variables
load_dotenv()
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_key = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticates to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) # Consumer key and consumer secret 
auth.set_access_token(access_token, access_key) # Accesses token and access token

# Create API 
api = tweepy.API(auth)

# Read lines from txt
lines = []
with open('quotes.txt') as f:    
    lines = f.readlines()

# Iterates over lines
for line in lines:    
    # Quote fits in one single tweet. No thread necesary    
    if (len(line) <= 273 and len(line)>4):         
        api.update_status(f'{line} #quote')        
        time.sleep(3600)
    
    # Thread necesary    
    elif (len(line)>=2):
        # 1st tweet of the thread
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
        
        # Responses to the original tweet
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
        
        # Last tweet of the thread
        if(tweet!=""):                
            reply = api.update_status(status=f'...{tweet}', in_reply_to_status_id=old, auto_populate_reply_metadata=True)                
            tweet = ""        
        time.sleep(3600)