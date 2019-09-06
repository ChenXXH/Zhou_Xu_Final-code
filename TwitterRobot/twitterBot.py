from TwitterFollowBot import TwitterBot
import threading
from threading import Thread

def bot1(keyword, count):
    my_bot = TwitterBot("config.txt")
    my_bot.sync_follows()
    my_bot.auto_follow(keyword, count = count)

def bot2(keyword, count):
    my_bot = TwitterBot("config2.txt")
    my_bot.sync_follows()
    my_bot.auto_follow(keyword, count = count)

def bot3(keyword, count):
    my_bot = TwitterBot("config3.txt")
    my_bot.sync_follows()
    my_bot.auto_follow(keyword, count = count)

def bot4(keyword, count):
    my_bot = TwitterBot("config4.txt")
    my_bot.sync_follows()
    my_bot.auto_follow(keyword, count = count)

if __name__ == '__main__':
    '''
    keyword1 = input("Bot 1, enter keyword:")
    count1 = input("Bot 1, enter target number:")
    
    keyword2 = input("Bot 2, enter keyword:")
    count2 = input("Bot 2, enter target number:")
    '''
    keyword3 = input("Bot 3, enter keyword:")
    count3 = input("Bot 3, enter target number:")
    '''
    keyword4 = input("Bot 4, enter keyword:")
    count4 = input("Bot 4, enter target number:")
    '''
    #Thread(target = bot1, args = (keyword1, count1)).start()
    #Thread(target = bot2, args = (keyword2, count2)).start()
    Thread(target = bot3, args = (keyword3, count3)).start()
    #Thread(target = bot4, args = (keyword4, count4)).start()
