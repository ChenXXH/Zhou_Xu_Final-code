from tkinter import *
import tkinter.messagebox
from TwitterFollowBot import TwitterBot

class twitterBot():

    def __init__(self, master):
        self.master = master
        self.fourthFrame = Frame(master)
        self.fourthFrame.grid()

        self.label0 = Label(self.fourthFrame, text = "Twitter Robot", font = "Helvetica 20 bold")
        self.label1 = Label(self.fourthFrame, text = "Please enter the keyword: ")
        self.entry1 = Entry(self.fourthFrame)
        self.label2 = Label(self.fourthFrame, text = "Please enter the number of friends you want to follow: ")
        self.entry2 = Entry(self.fourthFrame)
        self.button1 = Button(self.fourthFrame, text = "Follow", command = self.auto_follow)

        self.label0.grid(row=0, ipadx=50, ipady=100, padx = 250)
        self.label1.grid(row = 1, pady =10)
        self.entry1.grid(row = 2, pady =10)
        self.label2.grid(row = 3, pady =10)
        self.entry2.grid(row = 4, pady =10)
        self.button1.grid(row = 5, pady =10)

    def auto_follow(self):
        self.label2 = Label(self.fourthFrame, text="Loading")
        self.label2.grid(row=6, columnspan=2, pady=10)
        self.canvas = Canvas(self.fourthFrame, width=465, height=22, bg="white")
        self.canvas.grid(row=7, columnspan=2)
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")

        tkinter.messagebox.showinfo(title="Information", message="Processing, it takes around 10s - 60s to follow one account. Please wait unitl it finishes!")
        keyword = self.entry1.get()
        num = self.entry2.get()
        my_bot = TwitterBot("config2.txt")

        my_bot.sync_follows()
        my_bot.auto_follow(keyword, self.canvas, self.master, fill_line, count = num)
        tkinter.messagebox.showinfo(title="Information", message="Done!")

root = Tk()
root.geometry("800x600")
tm = twitterBot(root)
root.mainloop()