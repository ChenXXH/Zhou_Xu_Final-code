import pandas as pd
import scipy.stats as sct
from datetime import date
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from time import strptime
import time


def friend_analysis(database_name):
    #use it after updating the follower sql file

    db = mysql.connector.connect(user = 'root', password = '123456',host = 'localhost', database = database_name)
    user = pd.read_sql("select * from user", db) # get all data from table user

    #preprocessing - factorizing language
    labels,unique=user['language'].factorize()
    user['lang_code']=labels
    user.head()

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
    for i in range(len(user)):
        user.loc[i, "latest_tweet_time_diff"] = CountTweetDate(user['latest_tweet_time'][i])
    #x['follow_date'] = x.apply(lambda row: CountDate(row['follow_date']), axis=1)

    #extract hour information
    user['latest_tweet_time'] = pd.to_datetime(user['latest_tweet_time'],format='%a %b %d %H:%M:%S +0000 %Y')
    user['latest_tweet_hour']=user['latest_tweet_time'].apply(lambda x: x.hour)
    user.head()

    print('If there is NaN: ',user.isnull().values.any())
    user.fillna(0,inplace=True)
    print('Do we have NaN now? ',user.isnull().values.any())

    #scale
    features=['following','favourites','followers','friends','follower2following','retweet_ratio','favourite_ratio','lang_code','latest_tweet_time_diff','latest_tweet_hour']
    user_km=user[features]

    nm_user_km=(user_km-user_km.min())/(user_km.max()-user_km.min())

    #influence metric
    user['influence']=(nm_user_km['follower2following']+nm_user_km['followers']+nm_user_km['retweet_ratio']+nm_user_km['favourite_ratio'])/4

    #engagement metric
    user['engagement']=(nm_user_km['favourites']+nm_user_km['friends'])/2
    user.head()

    high_val_user=[]
    high_influ_user=[]
    active_user=[]
    low_val_user=[]
    for i in range(len(user)):
        if user.loc[i].influence>=user['influence'].mean() and user.loc[i].engagement>=user['engagement'].mean():
            high_val_user.append(user.iloc[i])
        elif user.loc[i].influence>=user['influence'].mean() and user.loc[i].engagement<user['engagement'].mean():
            high_influ_user.append(user.iloc[i])
        elif user.loc[i].influence<user['influence'].mean() and user.loc[i].engagement>=user['engagement'].mean():
            active_user.append(user.iloc[i])
        else:
            low_val_user.append(user.iloc[i])

    high_val_user=pd.DataFrame(data=high_val_user)[["screen_name", "influence", "engagement"]]
    high_influ_user=pd.DataFrame(data=high_influ_user)[["screen_name", "influence", "engagement"]]
    active_user=pd.DataFrame(data=active_user)[["screen_name", "influence", "engagement"]]
    low_val_user=pd.DataFrame(data=low_val_user)[["screen_name", "influence", "engagement"]]

    nm_user_km.head()
    print('high value engagement mean: ',high_val_user.engagement.mean(),'; ','high value influence mean ',high_val_user.influence.mean())
    print('high influ engagement mean: ',high_influ_user.engagement.mean(),'; ','high influ influence mean ',high_influ_user.influence.mean())
    print('active engagement mean: ',active_user.engagement.mean(),'; ','active influence mean ',active_user.influence.mean())
    print('low value engagement mean: ',low_val_user.engagement.mean(),'; ','low value influence mean ',low_val_user.influence.mean())

    high_val_user.sort_values(by=['influence'],axis=0,ascending=False)[['screen_name','influence','engagement']].head(20)
    high_val_user.sort_values(by=['engagement'],axis=0,ascending=False)[['screen_name','influence','engagement']].head(20)

    fig1 = plt.figure()
    plt.subplot(111)
    user.groupby(user.latest_tweet_hour).latest_tweet_hour.count().plot()
    plt.ylabel('frequency')
    plt.title('When do friends tweet')

    fig2 = plt.figure()
    plt.subplot(111)
    labels = 'high\nvalue', 'high\nengagement', 'high\ninfluence', 'low\nvalue'
    size = [len(high_val_user), len(active_user), len(high_influ_user), len(low_val_user)]
    plt.pie(size, labels=labels, autopct='%1.1f%%')

    return fig1, fig2, high_val_user, high_influ_user, active_user, low_val_user

def get_friends_name(database_name, metric_list):
    print(metric_list)
    db = mysql.connector.connect(user='root', password='123456', host='localhost', database=database_name)
    users = pd.read_sql("select * from user", db)  # get all data from table user
    followed_by = []
    language = []
    favourites = [] #"0 - 199", "200 - 999", "1000 - 2999", "3000 - 7999", "8000 - 20000", "over 20000"
    followers = [] #"0 - 199", "200 - 399", "400 - 799", "800 - 1599", "1600 - 4000", "4000 - 20000", "over 20000"
    friends = []
    for i in users.columns:
        if (i == "followed_by"):
            for j in users[i]:
                user_choice = None
                if (metric_list[0] == "Yes"):
                    user_choice = 1
                elif (metric_list[0] == "No"):
                    user_choice = 0
                else:
                    user_choice = None
                if (user_choice == None):
                    followed_by.append(True)
                else:
                    if (j == user_choice):
                        followed_by.append(True)
                    else:
                        followed_by.append(False)
        elif (i == "language"):
            for j in users[i]:
                if (metric_list[1] == ""):
                    language.append(True)
                else:
                    if (j == metric_list[1]):
                        language.append(True)
                    else:
                        language.append(False)
        elif (i == "favourites"):
            for j in users[i]:
                if (metric_list[2] != "" and metric_list[3] != ""):
                    if (int(metric_list[2])<= j < int(metric_list[3])):
                        favourites.append(True)
                    else:
                        favourites.append(False)
                else:
                    favourites.append(True)
        elif (i == "followers"):
            for j in users[i]:
                if (metric_list[4] != "" and metric_list[5] != ""):
                    if (int(metric_list[4])<= j < int(metric_list[5])):
                        followers.append(True)
                    else:
                        followers.append(False)
                else:
                    followers.append(True)
        elif (i == "friends"):
            for j in users[i]:
                if (metric_list[6] != "" and metric_list[7] != ""):
                    if (int(metric_list[6])<= j < int(metric_list[7])):
                        friends.append(True)
                    else:
                        friends.append(False)
                else:
                    friends.append(True)
    print(followed_by)
    print(language)
    print(favourites)
    print(followers)
    print(friends)

    select_name = []
    for i in range(0, len(users)):
        if (followed_by[i] and language[i] and favourites[i] and followers[i] and friends[i]):
            select_name.append(users.loc[i]["screen_name"])

    return select_name