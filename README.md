# Zhou_Xu_final-code
 
Instructions

There are two models in this project, which are Twitter Robot and Twitter Metrics. The user manual is below. Please follow the instructions.

Twitter Robot

There are six files in this model – twitterBot.py, UI.py and four config.txt. twitterBot.py and UI.py are both used to follow other accounts. The differences are that twitterBot.py can used to follow others for four accounts (cremeglobal1, cremeglobal2, cremeglobal3 and cremeglobal4) simultaneously, but UI.py only can follow others for one account with user interface. config.txt contains API keys. In this model, two inputs are required: the keywords that users are concerned about and the number of accounts that users want to follow. To run this model, you need to install two packages – TwitterFollowBot and twitter via the command line by entering:
pip install “package name”

e.g. pip install TwitterFollowBot

Twitter Metrics
Twitter Metrics is used to display the descriptive tools, unfollow accounts according to users’ preference (including the preference to unfollow and remain), and auto-unfollow accounts by machine learning algorithm. There are 7 .py files in this model, which are twitterMetrics.py, friendsanalysis.py, getfollower.py, time_series.py, unfollow.py, RF.py and UI.py.

twitterMetrics.py
The functions of twitterMetrics.py are to create database (including table user, table unfollow and table friends), get data (including users’ basic information, relationship and timeline) though Twitter API, insert data into database, and the descriptive tool friends’ word cloud according to hashtag. The packages required to install are python-twitter, time, mysql-connector-python, matplotlib, wordcloud and itertools (intertools_s?).
friendsanalysis.py & followeranalysis.py
friendsanalysis.py and followeranalysis.py contains two descriptive tools that are high-value user identification (pie chart) and when do friends/follower tweet (line chart). The packages required to install are pandas, scipy, DateTime, mysql-connector-python, matplotlib, numpy and time.

getfollower.py
getfollower.py creates table follower and displays followers’ word cloud picture. The packages required to install are time, mysql-connector-python, matplotlib, python-twitter, wordcloud and itertools.

time-series.py
time-series.py presents the number of your account’ follower in line chart. The packages required to install are time, mysql-connector-python and python-twitter.

unfollow.py
unfollow.py contains three machine learning algorithms, including Random Forest, K-nearest neighbours and Logistic Regression and shows the evaluation of these three algorithms. The packages required to install are python-twitter, mysql-connector-python, SQLAlchemy, pandas, sklearn, numpy, time, DateTime.

RF.py
RF.py is the Random Forest algorithm that are finally used. The packages required to install are mysql-connector-python, pandas, time, DateTime, sklearn and imblearn.

UI.py
UI.py is the user interface for Twitter Metrics. There are mainly six pages which are Information page, Visualisation of Friends page, Select Accounts You Want to Unfollow page, Select Accounts You Want to Remain page, Auto-unfollow page and Visualisation of Followers page. Information page collects users’ screen name and their API keys (including consumer key, consumer secret, access token key and access token secret). Visualisation of Friends/Followers page present all the descriptive analysis on friends and followers, such as word cloud, pie chart, etc. Select Accounts You Want to Unfollow/Remain let users select twitter metrics to find out their preference on unfollowing and remaining. In Auto-unfollow page, users can run the Random Forest algorithm and get a list of accounts that they might want to unfollow. The package required to install is matplotlib.
