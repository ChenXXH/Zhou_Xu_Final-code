import time
import mysql.connector
from mysql.connector import errorcode
import math
import matplotlib.pyplot as plt
import twitter
from wordcloud import WordCloud
from itertools import groupby

def get_follower(database_name, api_key):
    Consumer_key = api_key[0]
    Consumer_secret = api_key[1]
    Access_token_key = api_key[2]
    Access_token_secret = api_key[3]

    # twitter API details
    api = twitter.Api(consumer_key=Consumer_key, consumer_secret=Consumer_secret, access_token_key=Access_token_key, access_token_secret=Access_token_secret)
    # get friends information
    friends_id = api.GetFriendIDs(screen_name=database_name)  #screen_name='cremeglobal'
    # get followers' id
    followers_id = api.GetFollowerIDs(screen_name = database_name)  #screen_name='cremeglobal'

    groups=math.ceil(len(followers_id)/100)
    # API allows 300 requests per 15 mins, each request can output 100 users info
    i=1
    followers=list()
    while i<=groups:
        followers_batch=api.UsersLookup(user_id=followers_id[(i-1)*100:i*100]) # ur friends list
        followers.extend(followers_batch)
        i+=1
    len(followers)

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

    ########################################################################################################################
    ### insert all metrics into database

    mycursor = db1.cursor()
    # create table user
    mycursor.execute('create table if not exists follower(id bigint primary key, screen_name varchar(50), following tinyint, latest_tweet_time varchar(40), language varchar(6), favourites int, followers int, friends int, follower2following float, retweet_ratio float, favourite_ratio float)')
    hashtags=[]  #collect a list of followers' hashtags
    insert_s = "insert into follower (id, screen_name, following, latest_tweet_time, language, favourites, followers, friends, follower2following, retweet_ratio, favourite_ratio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for i in range(len(followers)):
        hashtag = []
        try:
            # use timeline to get user retweet, favorite information
            timeline = api.GetUserTimeline(user_id=followers[i].id, include_rts=False, exclude_replies=True, count=100)

            retweet_ratio = sum([timeline[j].retweet_count for j in range(len(timeline))]) / len(timeline)
            hashtag = [timeline[0].hashtags[j].text for j in range(len(timeline[0].hashtags))]
            print(hashtag)
            # calculate the ratio about the number of followers and following
        except IndexError:
            print('No timeline for follower',i)
            pass
        except twitter.error.TwitterError:
            time.sleep(60)
        except ZeroDivisionError:
            retweet_ratio = None
        try:
            favourite_ratio = sum([timeline[j].favorite_count for j in range(len(timeline))]) / len(timeline)
        except ZeroDivisionError:
            favourite_ratio = None
        try:
            follower_to_following = followers[i].followers_count / followers[i].friends_count
        except ZeroDivisionError:
            follower_to_following = None

        # To check the relationship status: following or not, followed back or not
        relationship_following = False
        if (followers_id[i] in friends_id):
            relationship_following = True
        print(i)
        # insert None into table if the accoutns retweet created time and languague are empty
        if (followers[i].status != None):
            param = (followers[i].id,followers[i].screen_name,
                     relationship_following,
                     followers[i].status.created_at, followers[i].status.lang,
                     followers[i].favourites_count, followers[i].followers_count, followers[i].friends_count,
                     follower_to_following, retweet_ratio, favourite_ratio)
        else:
            param = (followers[i].id, followers[i].screen_name,
                     relationship_following,
                     None, None,
                     followers[i].favourites_count, followers[i].followers_count, followers[i].friends_count,
                     follower_to_following, retweet_ratio, favourite_ratio)
        # insert all metrics into table user
        try:
            mycursor.execute(insert_s, param)
            print("insert %s",(followers[i].id))
            db1.commit()
        # Update existed users' information
        except mysql.connector.errors.IntegrityError:
            try:
                if (followers[i].status != None):
                    mycursor.execute("update follower set screen_name = %s,following = %s, latest_tweet_time = %s, language = %s, favourites = %s,followers = %s, friends = %s, follower2following=%s, retweet_ratio=%s, favourite_ratio=%s where id = %s",
                                     (followers[i].screen_name,
                                      relationship_following,
                                      followers[i].status.created_at, followers[i].status.lang,
                                      followers[i].favourites_count, followers[i].followers_count, followers[i].friends_count,
                                      follower_to_following, retweet_ratio, favourite_ratio, followers[i].id))
                    print("update follower set screen_name = %s " % (followers[i].screen_name))
                    db1.commit()
            except Exception as e:
                print(e)
                db1.rollback()
        except Exception as e:
            print(e)
            db1.rollback()
        hashtags.extend(hashtag)
        print(hashtags)
    db1.close()

    #wordcloud
    results = {value: len(list(freq)) for value, freq in groupby(sorted(hashtags))}
    wordcloud=WordCloud(background_color='white',max_words=100,scale=3,random_state=1).generate_from_frequencies(results)
    fig=plt.figure()
    plt.subplot(111)
    plt.axis('off')
    fig.suptitle('hashtag trend',fontsize=10)
    plt.imshow(wordcloud)
    return fig