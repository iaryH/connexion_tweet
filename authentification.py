# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 11:00:50 2022

@author: zo11
"""

import tweepy
import json
 
# API keyws that yous saved earlier
def authent():
    
    with open('twit.json', 'r') as j:
         json_ = json.loads(j.read())
    api_key = json_["api_key"]
    api_secrets = json_["secret_key"]
    access_token = json_["access_token"]
    access_secret = json_["access_token_secret"]
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secrets)
    auth.set_access_token(access_token,access_secret)
     
    api = tweepy.API(auth)
     
    try:
        api.verify_credentials()
        print('Successful Authentication')
        return api
    except:
        print('Failed authentication')
        raise "Fin du script"
        
if __name__=="__main__":
    print(authent())