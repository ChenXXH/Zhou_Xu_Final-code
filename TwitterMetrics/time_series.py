import twitter
import time
import mysql.connector
from mysql.connector import errorcode

def time_series(database_name, api_key):
    Consumer_key = api_key[0]
    Consumer_secret = api_key[1]
    Access_token_key = api_key[2]
    Access_token_secret = api_key[3]

    # twitter API details
    api = twitter.Api(consumer_key=Consumer_key, consumer_secret=Consumer_secret, access_token_key=Access_token_key, access_token_secret=Access_token_secret)

    ######track followers number table
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
    followers=api.GetUser(screen_name= database_name).followers_count
    date=time.strftime('%Y-%m-%d')

    mycursor = db1.cursor()

    mycursor.execute('select * from user where followed_by=1')
    row=mycursor.fetchall()
    mutual_follow=len(row)

    # create table
    mycursor.execute("create table if not exists info(date varchar(10) primary key, followers_count int,mutual_follow int)")
    try:
        insert_s="insert into info (date,followers_count,mutual_follow) values (%s,%s,%s)"
        param=(date,followers,mutual_follow)
    except mysql.connector.errors.IntegrityError:
        print("You've already updated")

    mycursor.execute(insert_s, param)
    db1.commit()
    db1.close()

    return