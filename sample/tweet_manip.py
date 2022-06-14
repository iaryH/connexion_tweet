# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:06:38 2022

@author: zo11
"""

import authentification as aut
import pandas as pd
from tqdm import tqdm
from datetime import datetime

def transform_time(dic):
    dic['created_at'] = datetime.strptime(dic['created_at'],
                                          '%a %b %d %H:%M:%S +0000 %Y')
    return dic

def lire_tweet(name=None, screen_name=None, id = None):
    ls_output = ['id_str', 'full_text', 'favorite_count', 'retweet_count',
                 'created_at']
    a = aut.authent()
    if screen_name:
        trump_tweets = a.user_timeline(screen_name=screen_name,tweet_mode='extended')
    elif name:
        trump_tweets = a.user_timeline(name=name,tweet_mode='extended')
    elif id:
        trump_tweets = a.user_timeline(id=id,tweet_mode='extended')
    else:
        raise "merci d'identifier"
    df_ret = pd.DataFrame(columns=ls_output)
    for i in tqdm(trump_tweets):
        js = i._json
        js_new = {key:js[key] for key in ls_output}
        js_farany = transform_time(js_new)
        del js, js_new
        df_ret = pd.concat([df_ret,pd.DataFrame(js_farany, index = [0])])
    return df_ret.reset_index(drop=True)


def get_text(id):
    a = aut.authent()
    status = a.get_status(id, tweet_mode='extended') 
    return status.full_text

if __name__=="__main__":
    name = input("entrer le nom du personne ou page à lire son tweet\n")
    data = lire_tweet(screen_name=name).head(8)
    