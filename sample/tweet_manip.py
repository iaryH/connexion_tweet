# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:06:38 2022

@author: zo11
"""

import authentification as aut
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from datetime import date

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
        raise "merci d'identifier le compte à explorer"
    df_ret = pd.DataFrame(columns=ls_output)
    for i in tqdm(trump_tweets):
        js = i._json
        print(js.keys())
        js_new = {key:js[key] for key in ls_output}
        js_farany = transform_time(js_new)
        del js, js_new
        df_ret = pd.concat([df_ret,pd.DataFrame(js_farany, index = [0])])
    return df_ret.reset_index(drop=True)


def get_text(id):
    a = aut.authent()
    status = a.get_status(id, tweet_mode='extended') 
    return status.full_text

def geo(nom):
    geolocator = Nominatim(user_agent="your_app_name")
    loc = geolocator.geocode(nom)
    return loc.latitude,loc.longitude

def search():
    api = aut.authent()
    for tanana in ["Madagascar"]:
        
        lat, long = geo(tanana)
        # places = api.geo_search(query=tanana, granularity="city")
        # place_id = places[0].id
        g = str(lat) + ',' + str(long) + ',' + '40mi'
        print(g)
        tweets = api.search_tweets(q="telma", count=100)
        print(tweets)
        for tweet in tweets:
            print (tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")

if __name__=="__main__":
    res = pd.DataFrame()
    ls = ['airtel_mdg', 'orange_mg','blueline_MG']
    filtre = ['voix','sms','data','mo','minute','second','heur','mn','4G','5G','ar','ariary','ttc','bonus','go','profitez']
    #name = input("entrer le nom du personne ou page à lire son tweet\n")
    for l in ls:
        data = lire_tweet(id=l)
        data['operateur']=l
        res = res.append(data, ignore_index=True)
    da = str(date.today())
    res1 = res[res['full_text'].str.contains('|'.join(filtre))]
    res2 = res1[res1['created_at'].apply(lambda x : x.year)>=2022]
    res2.to_excel(r'D:\Utilisateurs\Zo11\Desktop\tweet_'+da+'.xlsx')
    search()
    