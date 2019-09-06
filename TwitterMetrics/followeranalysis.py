import pandas as pd
import scipy.stats as sct
from datetime import date
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from time import strptime
import time

#use it after updating the follower sql file

def follower_analy(database_name):
    db = mysql.connector.connect(user = 'root', password = '123456',host = 'localhost', database = database_name)
    follower = pd.read_sql("select * from follower", db) # get all data from table user

    #preprocessing - factorizing language
    labels,unique=follower['language'].factorize()
    follower['lang_code']=labels
    follower.head()

    #preprocessing - date
    # get the date difference of lastest tweet time
    def CountTweetDate(follow_date):
        try:
            follow_date = date(*map(int, [follow_date.split(' ')[5], strptime(follow_date.split(' ')[1],'%b').tm_mon, follow_date.split(' ')[2]]))
            now_date = date(*map(int, time.strftime('%Y-%m-%d').split('-')))
            date_difference = now_date - follow_date
            return date_difference.days
        except AttributeError:
            pass

    # change the date columns' content to date difference - integer
    for i in range(len(follower)):
        follower.loc[i, "latest_tweet_time_diff"] = CountTweetDate(follower['latest_tweet_time'][i])

    #extract hour information
    follower['latest_tweet_time'] = pd.to_datetime(follower['latest_tweet_time'],format='%a %b %d %H:%M:%S +0000 %Y')
    follower['latest_tweet_hour']=follower['latest_tweet_time'].apply(lambda x: x.hour)

    print('If there is NaN: ',follower.isnull().values.any())
    follower.fillna(0,inplace=True)
    print('Do we have NaN now? ',follower.isnull().values.any())

    #scale
    features=['following','favourites','followers','friends','follower2following','retweet_ratio','favourite_ratio','lang_code','latest_tweet_time_diff','latest_tweet_hour']
    follower_km=follower[features]
    nm_follower_km=(follower_km-follower_km.min())/(follower_km.max()-follower_km.min())

    #influence metric
    follower['influence']=(nm_follower_km['follower2following']+nm_follower_km['followers']+nm_follower_km['retweet_ratio']+nm_follower_km['favourite_ratio'])/4
    #engagement metric
    follower['engagement']=(nm_follower_km['favourites']+nm_follower_km['friends'])/2

    high_val_user=[]
    high_influ_user=[]
    active_user=[]
    low_val_user=[]
    for i in range(len(follower)):
        if follower.loc[i].influence>=follower['influence'].mean() and follower.loc[i].engagement>=follower['engagement'].mean():
            high_val_user.append(follower.iloc[i])
        elif follower.loc[i].influence>=follower['influence'].mean() and follower.loc[i].engagement<follower['engagement'].mean():
            high_influ_user.append(follower.iloc[i])
        elif follower.loc[i].influence<follower['influence'].mean() and follower.loc[i].engagement>=follower['engagement'].mean():
            active_user.append(follower.iloc[i])
        else:
            low_val_user.append(follower.iloc[i])

    high_val_user=pd.DataFrame(data=high_val_user)[["screen_name", "influence", "engagement"]]
    try:
        high_influ_user=pd.DataFrame(data=high_influ_user)[["screen_name", "influence", "engagement"]]
    except:
        high_influ_user=[]
    active_user=pd.DataFrame(data=active_user)[["screen_name", "influence", "engagement"]]
    low_val_user=pd.DataFrame(data=low_val_user)[["screen_name", "influence", "engagement"]]
    nm_follower_km.head()

    print('high value engagement mean: ',high_val_user.engagement.mean(),'; ','high value influence mean ',high_val_user.influence.mean())
    #print('high influ engagement mean: ',high_influ_user.engagement.mean(),'; ','high influ influence mean ',high_influ_user.influence.mean())
    print('active engagement mean: ',active_user.engagement.mean(),'; ','active influence mean ',active_user.influence.mean())
    print('low value engagement mean: ',low_val_user.engagement.mean(),'; ','low value influence mean ',low_val_user.influence.mean())

    high_val_user.sort_values(by=['influence'],axis=0,ascending=False)[['screen_name','influence','engagement']].head(20)
    high_val_user.sort_values(by=['engagement'],axis=0,ascending=False)[['screen_name','influence','engagement']].head(20)

    fig1 = plt.figure()
    plt.subplot(111)
    follower.groupby(follower.latest_tweet_hour).latest_tweet_hour.count().plot()
    plt.ylabel('frequency')
    plt.title('When do followers tweet')

    fig2 = plt.figure()
    plt.subplot(111)
    labels = 'high\nvalue', 'high\nengagement', 'high\ninfluence', 'low\nvalue'
    size = [len(high_val_user), len(active_user), len(high_influ_user), len(low_val_user)]
    plt.pie(size, labels=labels, autopct='%1.1f%%')

    return fig1, fig2, high_val_user, high_influ_user, active_user, low_val_user
