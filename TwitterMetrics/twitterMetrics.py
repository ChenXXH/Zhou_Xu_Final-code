import twitter
import time
import mysql.connector
import math
import tkinter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from itertools import groupby


def check_name_and_create_database(twitter_user_name, window, canvas, api_key):
    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")

    database_name = twitter_user_name.replace(" ","")
    print(database_name)

    Consumer_key = api_key[0]
    Consumer_secret = api_key[1]
    Access_token_key = api_key[2]
    Access_token_secret = api_key[3]

    # twitter API details
    try:
        api = twitter.Api(consumer_key=Consumer_key, consumer_secret=Consumer_secret, access_token_key=Access_token_key, access_token_secret=Access_token_secret)
    except twitter.error.TwitterError as e:
        tkinter.messagebox.showerror(title="Error!", message="You might enter a API key. Please try agian!")
        return False, None

    # get friends information
    try:
        friends_id = api.GetFriendIDs(screen_name = twitter_user_name)
    except twitter.error.TwitterError as e:
        tkinter.messagebox.showerror(title="Error!", message="You might enter a wrong screen name. Please try agian!")
        return False, None
    # get followers' id
    followers_id = api.GetFollowerIDs(screen_name = twitter_user_name)


    #look up followers/friends' information,replace getfriends/getfollowers - time consuming
    groups=math.ceil(len(friends_id)/100)
    # API allows 300 requests per 15 mins, each request can output 100 users info
    i=1
    friends=list()
    while i<=groups:
        friend_batch=api.UsersLookup(user_id=friends_id[(i-1)*100:i*100]) # ur friends list
        friends.extend(friend_batch)
        i+=1
    friends
    ########################################################################################################################
    ### All details about database
    config = {
            'user': 'root',
            'password': '123456',
            'host': 'localhost',
            'auth_plugin':'mysql_native_password'
        }

    # To handle different connection errors
    db1 = mysql.connector.connect(**config)
    mycursor = db1.cursor()

    try:
        mycursor.execute("use " + database_name)
    except mysql.connector.errors.ProgrammingError as e:
        mycursor.execute("create database " + database_name)
        mycursor.execute("use " + database_name)

    ########################################################################################################################
    ### insert all metrics into database


    # create table user
    mycursor.execute('create table if not exists user(id bigint primary key, screen_name varchar(50), follow_date varchar(20), followed_by tinyint, following tinyint, latest_tweet_time varchar(40), language varchar(6), favourites int, followers int, friends int, follower2following float, retweet_ratio float, favourite_ratio float)')
    mycursor.execute( 'create table if not exists follower(id bigint primary key, screen_name varchar(50), following tinyint, latest_tweet_time varchar(40), language varchar(6), favourites int, followers int, friends int, follower2following float, retweet_ratio float, favourite_ratio float)')
    mycursor.execute("select * from user")
    data = mycursor.fetchall() # get data from database
    origin_id_list = []
    new_id_list = []
    # get the original friends' IDs
    for user in data:
        origin_id_list.append(user[0])
    # get the updated friend list ID
    for user in friends:
        new_id_list.append(user.id)
    # Find the unfollow accounts' IDs
    difference_id = list(set(origin_id_list).difference(set(new_id_list)))

    hashtags=[]  #collect a list of followers' hashtags

    insert_s = "insert into user (id, screen_name, follow_date, followed_by, following, latest_tweet_time, language, favourites, followers, friends, follower2following, retweet_ratio, favourite_ratio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    n = 465 / len(friends)

    for i in range(len(friends)):
        n = n + 465 / len(friends)
        canvas.coords(fill_line, (0, 0, n, 60))
        window.update()
        hashtag = []
        try:
            # use timeline to get user retweet, favorite information
            #count=100, if count is 20 or too small, it might exclude some users that reply a lot and still influential, like replying indicate high engagemnet
            timeline = api.GetUserTimeline(user_id=friends[i].id, include_rts=False, exclude_replies=True, count=100)
            retweet_ratio = sum([timeline[j].retweet_count for j in range(len(timeline))]) / len(timeline)
            hashtag = [timeline[0].hashtags[j].text for j in range(len(timeline[0].hashtags))]
            # calculate the ratio about the number of followers and following
        except IndexError:
            print('No timeline for follower ',i)
            pass
        except twitter.error.TwitterError:
            time.sleep(60)

        except ZeroDivisionError:
            retweet_ratio = 0
        try:
            favourite_ratio = sum([timeline[j].favorite_count for j in range(len(timeline))]) / len(timeline)
        except ZeroDivisionError:
            favourite_ratio = 0
        try:
            follower_to_following = friends[i].followers_count / friends[i].friends_count
        except ZeroDivisionError:
            follower_to_following = 0

        # To check the relationship status: following or not, followed back or not
        relationship_followedby = False
        relationship_following = True
        if (friends[i].id in followers_id):
            relationship_followedby = True

        # insert None into table if the accoutns retweet created time and languague are empty
        if (friends[i].status != None):
            param = (friends[i].id, friends[i].screen_name, time.strftime('%Y-%m-%d'),
                     relationship_followedby, relationship_following,
                     friends[i].status.created_at, friends[i].status.lang,
                     friends[i].favourites_count, friends[i].followers_count, friends[i].friends_count,
                     follower_to_following, retweet_ratio, favourite_ratio)
        else:
            param = (friends[i].id, friends[i].screen_name, time.strftime('%Y-%m-%d'),
                     relationship_followedby, relationship_following,
                     None, None,
                     friends[i].favourites_count, friends[i].followers_count, friends[i].friends_count,
                     follower_to_following, retweet_ratio, favourite_ratio)
        # insert all metrics into table user
        try:
            mycursor.execute(insert_s, param)
            print("insert %s",(friends[i].id))
            db1.commit()
        # Update existed users' information
        except mysql.connector.errors.IntegrityError:
            try:
                mycursor.execute("update user set screen_name = %s,followed_by = %s, following = %s, latest_tweet_time = %s, language = %s, favourites = %s,followers = %s, friends = %s, follower2following=%s, retweet_ratio=%s, favourite_ratio=%s where id = %s",
                                 (friends[i].screen_name,
                                  relationship_followedby, relationship_following,
                                  friends[i].status.created_at, friends[i].status.lang,
                                  friends[i].favourites_count, friends[i].followers_count, friends[i].friends_count,
                                  follower_to_following, retweet_ratio, favourite_ratio, friends[i].id))
                print("update user set screen_name = %s, followed_by = %s" % (friends[i].screen_name, relationship_followedby))
                db1.commit()
            except Exception as e:
                print(e)
                db1.rollback()
        except Exception as e:
            print(e)
            db1.rollback()
        hashtags.extend(hashtag)

    # update unfollow user relationship status
    for unfollow_user in difference_id:
        try:
            mycursor.execute('''update user set following = %s where id = %s''', (0, unfollow_user))
            db1.commit()
        except Exception as e:
            print(e)
            db1.rollback()

    ########################################################################################################################
    ### Get unfollow id list and create the unfollow table

    mycursor.execute("create table if not exists unfollow(id bigint primary key, screen_name varchar(50), follow_date varchar(20), followed_by tinyint,following tinyint, latest_tweet_time varchar(40), language varchar(6), favourites int,followers int,friends int,follower2following float, retweet_ratio float, favourite_ratio float)")
    insert_u = "insert into unfollow (id, screen_name, follow_date, followed_by, following, latest_tweet_time, language, favourites, followers, friends, follower2following,retweet_ratio, favourite_ratio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute("select * from user")
    data = mycursor.fetchall() # get data from database
    # delete the accounts inforamtion that we unfollow from table user
    for user in data:
        if (user[4] == 0):
            print("get an unfollow")
            try:
                mycursor.execute(insert_u, user)
                mycursor.execute("delete from user where following = 0")
                db1.commit()
            except Exception as e:
                print(e)
                db1.rollback()

    ### create the friends table for machine learning
    mycursor.execute("create table if not exists friends(id bigint primary key, screen_name varchar(50), follow_date varchar(20), followed_by tinyint,following tinyint, latest_tweet_time varchar(40), language varchar(6), favourites int,followers int,friends int,follower2following float, retweet_ratio float, favourite_ratio float)")

    # wordcloud
    results = {value: len(list(freq)) for value, freq in groupby(sorted(hashtags))}
    wordcloud = WordCloud(
        background_color='white',
        max_words=100,
        scale=3,
        random_state=1).generate_from_frequencies(results)

    fig = plt.figure()
    plt.subplot(111)
    plt.axis('off')
    fig.suptitle('hashtag trend', fontsize=10)
    plt.imshow(wordcloud)
    #plt.show()

    sorted(results.items(), key=lambda item: item[1], reverse=True)
    # Close the database
    db1.close()

    return True, fig

def unfollow_the_select(user_name, select_list, api_key):
    Consumer_key = api_key[0]
    Consumer_secret = api_key[1]
    Access_token_key = api_key[2]
    Access_token_secret = api_key[3]

    # twitter API details
    api = twitter.Api(consumer_key=Consumer_key, consumer_secret=Consumer_secret, access_token_key=Access_token_key,
                      access_token_secret=Access_token_secret)

    for name in select_list:
        api.DestroyFriendship(screen_name=name)

    config = {
        'user': 'root',
        'password': '123456',
        'host': 'localhost',
        'database': user_name,
        'auth_plugin': 'mysql_native_password'
    }

    db1 = mysql.connector.connect(**config)
    mycursor = db1.cursor()

    insert_u = "insert into unfollow (id, screen_name, follow_date, followed_by, following, latest_tweet_time, language, favourites, followers, friends, follower2following,retweet_ratio, favourite_ratio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute("select * from user")
    data = mycursor.fetchall()  # get data from database
    # delete the accounts inforamtion that we unfollow from table user
    for user in data:
        if (user[1] in select_list):
            try:
                say = "delete from user where screen_name = \'" + user[1] + "\'"
                print(say)
                mycursor.execute(say)
                mycursor.execute(insert_u, user)
                mycursor.execute("update unfollow set following = 0 where following = 1")
                db1.commit()
            except Exception as e:
                print(e)
                db1.rollback()
    return

def remain_the_select(user_name, select_list, api_key):
    Consumer_key = api_key[0]
    Consumer_secret = api_key[1]
    Access_token_key = api_key[2]
    Access_token_secret = api_key[3]

    # twitter API details
    api = twitter.Api(consumer_key=Consumer_key, consumer_secret=Consumer_secret, access_token_key=Access_token_key,
                      access_token_secret=Access_token_secret)

    config = {
        'user': 'root',
        'password': '123456',
        'host': 'localhost',
        'database': user_name,
        'auth_plugin': 'mysql_native_password'
    }

    db1 = mysql.connector.connect(**config)
    mycursor = db1.cursor()

    insert_u = "insert into friends (id, screen_name, follow_date, followed_by, following, latest_tweet_time, language, favourites, followers, friends, follower2following,retweet_ratio, favourite_ratio) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute("select * from user")
    data = mycursor.fetchall()  # get data from database
    # delete the accounts inforamtion that we unfollow from table user
    for user in data:
        if (user[1] in select_list):
            try:
                say = "delete from user where screen_name = \'" + user[1] + "\'"
                print(say)
                mycursor.execute(say)
                mycursor.execute(insert_u, user)
                db1.commit()
            except Exception as e:
                print(e)
                db1.rollback()
    return