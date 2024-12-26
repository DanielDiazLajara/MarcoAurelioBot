import os
import tweepy
import time
import random
from dotenv import load_dotenv
load_dotenv()

def get_random_quote():
    with open('quotes.txt', encoding="utf-8") as f:
        lines = f.readlines()
    # Eliminar saltos de línea y elegir una línea aleatoria
    while True:
        quote = random.choice([line.strip() for line in lines if line.strip()])
        if (len(quote) > 4):
            return quote

def post_tweet(client: tweepy.Client, text, previous_tweet = ''):
    response = ''
    if (previous_tweet != ''):
        response = client.create_tweet(
            text=f'{text} #quote',
            in_reply_to_tweet_id=previous_tweet,
        )
    else:
        response = client.create_tweet(text=f'{text} #quote')

    return response.data['id']

# Iterates over lines
def post_quote(line):
    # Authenticates to Twitter 
    client = tweepy.Client(
        consumer_key=os.getenv('API_KEY'),
        consumer_secret=os.getenv('API_KEY_SECRET'),
        access_token=os.getenv('ACCESS_TOKEN'),
        access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')
    )

    # Quote fits in one single tweet. No thread necesary    
    if (len(line) <= 273 and len(line)>4):    
        # Publicar el tweet
        post_tweet(client, line)

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
        original = post_tweet(client, tweet)
        
        # Responses to the original tweet
        old = original        
        tweet = ""        
        while i < len(words):                
            if(len(tweet+words[i])<273):                    
                tweet = tweet +" " + words[i]                    
                i += 1                
            else:                    
                reply = post_tweet(client, tweet, old)
                tweet = ""                    
                old = reply
        
        # Last tweet of the thread
        if(tweet!=""):                
            reply = post_tweet(client, tweet, old)
            tweet = ""        

def lambda_handler(event, context):
    try:
        # Obtener y publicar una cita
        quote = get_random_quote()
        post_quote(quote)
        return {"statusCode": 200, "body": "Tweet enviado correctamente."}
    except Exception as e:
        return {"statusCode": 500, "body": f"Error: {str(e)}"}