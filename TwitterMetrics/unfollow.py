import twitter
import mysql.connector
from mysql.connector import errorcode
import sqlalchemy as sqla
import pandas as pd
from sklearn import preprocessing
import numpy as np
import time
from datetime import date
from time import strptime
from sklearn.ensemble import RandomForestClassifier

account_num = input("Running account number:")
Consumer_key = None
Consumer_secret = None
access_token_key = None
access_token_secret = None
database_name = None
if account_num == "1":
    Consumer_key="6Y95c8JmbykhyDE1YZCEpXd18"
    Consumer_secret="t5DHnEGOVY51lCC5fpPzyNYuuXfVN0XLwpgqYTAJJjfn7KAuAJ"
    Access_token_key="1130762546644946945-rCcXmXik4C3nXz7gbAXbzXaNnUyZAq"
    Access_token_secret="BPTpymZpYzxLo5GVlqV0BDhf3Gu0nDKqbdLxDm5GPDocW"
    database_name = "cremeglobal1"
elif account_num == "2":
    Consumer_key="lPa0D8CRB0LMs65VI3llj8HZW"
    Consumer_secret="hl0P1cZmeO7HCAEalTIEL5ajJUTj5KtHBaw7YAPdyUimw6WKY0"
    Access_token_key="1132206438670098432-a6UrbqVldW2BI2QsfUWj6BhAASsR1B"
    Access_token_secret="1VRC0NdnN4e5RgOL7yAePSHyqvC7Ti7h92jZUR6AXnvdF"
    database_name = "cremeglobal2"
elif account_num == "3":
    Consumer_key="osJ56PDWF1qeR2gybfggWsCf3"
    Consumer_secret="aakHnRLoM7IqywrhaDL3KQxjVePHtTXB3aBESmWgUkgHCwYX3Q"
    Access_token_key="1132626333497024512-XJflr9L7EiPxjIgu0WQMhzxqn7qUmN"
    Access_token_secret="j4tKzT71op4yUL8PcwVlbVx8utINhX56lyTTQw7oFP1Td"
    database_name = "cremeglobal3"
elif account_num == "4":
    Consumer_key="j6UILpir0E2qw84lA1a8kNBKU"
    Consumer_secret="lgNKLiDbAJpfZsX1ZyMeLFRru3SWLTmskJIvfERT0pbtAyCQpN"
    Access_token_key="1132630055471996928-JoAfFoB9UyvKvpx1roxpjxMFHltOnc"
    Access_token_secret="F9wzfm90k4G5pnlG6qpOl2MoNWc7BvA5XrHjKFB3A7VLo"
    database_name = "cremeglobal4"

# twitter API details
api = twitter.Api(consumer_key=Consumer_key, consumer_secret=Consumer_secret, access_token_key=Access_token_key, access_token_secret=Access_token_secret)

########################################################################################################################
### All details about database
config = {
        'user': 'root',
        'password': '123456',
        'host': 'localhost',
        'database': database_name,
        'auth_plugin':'mysql_native_password'
    }

# To handle different connection errors
try:
    # Connect the cremeglobal1 database
    db1 = mysql.connector.connect(**config)
except mysql.connector.Error as e:
    if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your username or password")
    elif e.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(e)

'''
mycursor = db1.cursor()

mycursor.execute("select screen_name,followers,follower2following,retweet_ratio,favourite_ratio from user where retweet_ratio is null or follower2following is null")

myresult=mycursor.fetchall()

for x in myresult:
    print(x)
print(len(myresult))

for i in myresult:
    api.DestroyFriendship(screen_name=i)
#unfollow those whose one of ratios is null

mycursor.execute("select screen_name from user where retweet_ratio=0 or follower2following=0 or favourite_ratio=0")

myresult2=mycursor.fetchall()

for x in myresult2:
    print(x)
len(myresult2)

for i in myresult2[:80]:
    api.DestroyFriendship(screen_name=i)
#unfollow those whose one of ratios is 0

'''

engine=sqla.create_engine('mysql+pymysql://root:123456@localhost:3306/cremeglobal1')
user=pd.read_sql_table('user',engine)
unfollow=pd.read_sql_table('unfollow',engine)

all_data=pd.concat([user,unfollow],axis=0,ignore_index=True)
all_data.shape

# this is one way of factorizing
labels,unique=all_data['language'].factorize()
all_data['lang_code']=labels
all_data.head()

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
for i in range(len(all_data)):
    all_data.loc[i, "follow_datediff"] = CountDate(all_data['follow_date'][i])
    all_data.loc[i, "latest_tweet_daydiff"] = CountTweetDate(all_data['latest_tweet_time'][i])

def downcast(df):
    l1=[col for col in df if df[col].dtype == 'float64']
    l2=[col for col in df if df[col].dtype == 'int64']
    df[l1]=df[l1].astype(np.float32)
    df[l2]=df[l2].astype(np.int32)
downcast(all_data)

count_1=len(all_data.loc[all_data.following==1,'following'])
count_0=len(all_data.loc[all_data.following==0,'following'])

#compute imbalanced ratio
IR=count_1/count_0
if IR>=9:
    all_data0=all_data[all_data.following==0]
    all_data1=all_data[all_data.following==1]
    all_data0_over=all_data0.sample(count_1)
    all_data=pd.concat([all_data0_over,all_data1],axis=0)
    print(len(all_data.loc[all_data.following==1,'following']))
    print(len(all_data.loc[all_data.following==0,'following']))

feature=['follow_datediff','latest_tweet_daydiff','following','favourites','followers','friends','follower2following','retweet_ratio','favourite_ratio']
all_data=all_data[feature]
all_data.fillna(value=0,inplace=True)

x=all_data.drop(['following'],axis=1)
y=all_data['following']

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.1,random_state=22)

nm_xtrain=(xtrain-xtrain.mean())/xtrain.std()
nm_xtest=(xtest-xtest.mean())/xtest.std()

#KNN
from sklearn.neighbors import KNeighborsClassifier
neigh=KNeighborsClassifier(n_neighbors=33)
neigh.fit(nm_xtrain,ytrain)
ypred_knn=neigh.predict(nm_xtest)
ypred_knn

# Random forest algorithm
clf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=0)
clf.fit(xtrain, ytrain)
ypred_rf=clf.predict(xtest)
rf_feature_importance=pd.DataFrame(clf.feature_importances_,index=xtrain.columns,columns=['importance']).sort_values('importance', ascending=False)
rf_feature_importance.plot.bar()

# Logistics Regression algorithm
from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='ovr', max_iter = 500)
clf.fit(nm_xtrain, ytrain)
ypred_lr = clf.predict(nm_xtest)

#performance evaluation - accuracy
from sklearn.metrics import accuracy_score
print('---------KNN accuracy-------------')
print(accuracy_score(ypred_knn,ytest))
print('---------random forest accuracy----------')
print(accuracy_score(ypred_rf,ytest))
print('---------logistic regression accuracy----------')
print(accuracy_score(ypred_lr,ytest))

from sklearn.metrics import classification_report
print('---------KNN accuracy-------------')
print(classification_report(ytest,ypred_knn))
print('---------random forest accuracy----------')
print(classification_report(ytest,ypred_rf))
print('---------logistic regression accuracy----------')
print(classification_report(ytest,ypred_lr))

