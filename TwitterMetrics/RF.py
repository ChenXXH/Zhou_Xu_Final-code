import mysql.connector
import pandas as pd
import time
from datetime import date
from time import strptime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE,ADASYN

def rf(user_name):
    # Connect with database
    db = mysql.connector.connect(user = 'root', password = '123456',host = 'localhost', database = "cremeglobal2")

    data1 = pd.read_sql("select * from friends", db) # get all data from table user
    data2 = pd.read_sql("select * from unfollow", db) # get all data from table unfollow
    data3 = pd.read_sql("select * from user", db) # get all data from table unfollow
    data = pd.concat( [data1, data2], axis=0, ignore_index = True) # merge two table into one dataframe
    print(data)

    get_rid = ['id', 'screen_name', 'language', 'following'] # the unused column names
    x_columns = [x for x in data.columns if x not in get_rid]

    x = data[x_columns] # the dataframe only include the metrics we used
    y = data["following"] # target variable
    origin_x = data3[x_columns]

    # get the date difference of follow_date
    def CountDate(follow_date):
        follow_date = date(*map(int, follow_date.split('-')))
        now_date = date(*map(int, time.strftime('%Y-%m-%d').split('-')))
        date_difference = now_date - follow_date
        return date_difference.days

    # get the date difference of lastest tweet time
    def CountTweetDate(follow_date):
        follow_date = date(*map(int, [follow_date.split(' ')[5], strptime(follow_date.split(' ')[1],'%b').tm_mon, follow_date.split(' ')[2]]))
        now_date = date(*map(int, time.strftime('%Y-%m-%d').split('-')))
        date_difference = now_date - follow_date
        return date_difference.days

    # change the date columns' content to date difference - integer
    for i in range(len(x)):
        x.loc[i, "follow_date"] = CountDate(x['follow_date'][i])
        x.loc[i, "latest_tweet_time"] = CountTweetDate(x['latest_tweet_time'][i])

    for i in range(len(origin_x)):
        origin_x.loc[i, "follow_date"] = CountDate(origin_x['follow_date'][i])
        origin_x.loc[i, "latest_tweet_time"] = CountTweetDate(origin_x['latest_tweet_time'][i])
    print(x["latest_tweet_time"])

    # split dataset into training set and testing set
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    print('X_train Shape:', X_train.shape)
    print('X_test Shape:', X_test.shape)
    print('y_train Shape:', y_train.shape)
    print('y_test Shape:', y_test.shape)

    # Random forest algorithm
    clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
    X_resample, y_resample = SMOTE().fit_resample(X_train, y_train)
    clf.fit(X_resample, y_resample)
    print(clf.feature_importances_) # feature importance

    y_pred = clf.predict(X_test)
    from sklearn.metrics import classification_report
    print(classification_report(y_test,y_pred))

    recommend = clf.predict(origin_x)
    print(recommend)

    recommend_list = []
    for i in range(0, len(recommend)):
        if (recommend[i] == 0):
            recommend_list.append(data3.loc[i, "screen_name"])
    # Close the database
    db.close()
    return recommend_list