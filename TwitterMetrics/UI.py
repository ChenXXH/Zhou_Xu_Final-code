from tkinter import *
from tkinter import ttk
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class twitterMatrics():

    def __init__(self, master):
        self.root = master
        self.root.geometry("800x600")
        #self.root.resizable(FALSE, FALSE)
        screennamePage(self.root)

########################################################################################################################
### Screen name page
from twitterMetrics import check_name_and_create_database

class screennamePage():

    def __init__(self, master):
        self.master = master
        self.firstFrame = Frame(master)
        self.firstFrame.grid(row=0, column=0)

        self.label0 = Label(self.firstFrame, text = "Information", font = "Helvetica 20 bold")
        self.label1 = Label(self.firstFrame, text = "Twitter screen name ")
        self.entry1 = Entry(self.firstFrame)
        self.button1 = Button(self.firstFrame, text = "Submit", command = self.button1_click)
        self.label3 = Label(self.firstFrame, text="Consumer_key ")
        self.entry3 = Entry(self.firstFrame)
        self.entry3.insert(END, '6Y95c8JmbykhyDE1YZCEpXd18')
        self.label4 = Label(self.firstFrame, text="Consumer_secret ")
        self.entry4 = Entry(self.firstFrame)
        self.entry4.insert(END, 't5DHnEGOVY51lCC5fpPzyNYuuXfVN0XLwpgqYTAJJjfn7KAuAJ')
        self.label5 = Label(self.firstFrame, text="Access_token_key ")
        self.entry5 = Entry(self.firstFrame)
        self.entry5.insert(END, '1130762546644946945-rCcXmXik4C3nXz7gbAXbzXaNnUyZAq')
        self.label6 = Label(self.firstFrame, text="Access_token_secret ")
        self.entry6 = Entry(self.firstFrame)
        self.entry6.insert(END, 'BPTpymZpYzxLo5GVlqV0BDhf3Gu0nDKqbdLxDm5GPDocW')

        self.label0.grid(row = 0, columnspan = 2, ipadx = 50, ipady = 100, padx = 250)
        self.label1.grid(row = 1, pady = 10, sticky = E)
        self.entry1.grid(row = 1,column = 1, pady = 10, sticky = W)
        self.label3.grid(row = 2, pady = 10, sticky = E)
        self.entry3.grid(row = 2,column = 1, pady = 10, sticky = W)
        self.label4.grid(row = 3, pady = 10, sticky = E)
        self.entry4.grid(row = 3,column = 1, pady = 10, sticky = W)
        self.label5.grid(row = 4, pady = 10, sticky = E)
        self.entry5.grid(row = 4,column = 1, pady = 10, sticky = W)
        self.label6.grid(row = 5, pady = 10, sticky = E)
        self.entry6.grid(row = 5,column = 1, pady = 10, sticky = W)
        self.button1.grid(row = 8, columnspan = 2,pady = 10)

    def button1_click(self,):
        self.label2 = Label(self.firstFrame, text="Loading")
        self.label2.grid(row=6, columnspan =2, pady=10)
        self.canvas = Canvas(self.firstFrame, width=465, height=22, bg="white")
        self.canvas.grid(row=7, columnspan =2)

        self.api_key = []
        self.api_key.append(self.entry3.get())
        self.api_key.append(self.entry4.get())
        self.api_key.append(self.entry5.get())
        self.api_key.append(self.entry6.get())
        name = self.entry1.get()
        check, fig1 = check_name_and_create_database(name, self.master, self.canvas, self.api_key)
        if check:
            self.firstFrame.destroy()
            friendsPage(self.master, fig1, name, self.api_key)

########################################################################################################################
### Friends analysing page
from friendsanalysis import friend_analysis

class friendsPage():

    def __init__(self, master, fig1, user_name, api_key):
        self.fig2, self.fig3, high_val_user, high_influ_user, active_user, low_val_user = friend_analysis(user_name)
        self.api_key = api_key
        self.user_name = user_name
        self.master = master
        self.fig1 = fig1
        self.secondFrame = Frame(master)
        self.secondFrame.grid()

        self.label0 = Label(self.secondFrame, text = "Visualisation - Friends", font = "Helvetica 20 bold")
        self.button1 = Button(self.secondFrame, text = "Next", command = self.changeFrame)
        self.button2 = Button(self.secondFrame, text = "Back", command = self.goBack)

        self.label0.grid(row = 0, ipadx=50, ipady=10, padx = 220)
        self.button1.grid(row = 3, padx = 50, sticky = E)
        self.button2.grid(row = 3, padx = 50, sticky = W)

        self.frame_canvas = Frame(self.secondFrame)
        self.frame_canvas.grid(row=1, column=0)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas,  width = 640, height = 400)
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.frame_figures = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_figures, anchor='nw')

        self.text = Text(self.frame_figures)
        self.text.insert(END, "High value user:\n")
        self.text.insert(END, high_val_user)
        self.text.insert(END, "\n\nHigh influence user:\n")
        self.text.insert(END, high_influ_user)
        self.text.insert(END, "\n\nActive user:\n")
        self.text.insert(END, active_user)
        self.text.insert(END, "\n\nLow value user:\n")
        self.text.insert(END, low_val_user)
        self.text.grid(row=0)

        self.canvas0 = FigureCanvasTkAgg(self.fig1, self.frame_figures)
        self.canvas0.draw()
        self.canvas0.get_tk_widget().grid(row=1)

        self.canvas1 = FigureCanvasTkAgg(self.fig2, self.frame_figures)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=2)

        self.canvas1 = FigureCanvasTkAgg(self.fig3, self.frame_figures)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=3)

        self.frame_figures.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def goBack(self,):
        self.secondFrame.destroy()
        screennamePage(self.master)

    def changeFrame(self,):
        self.secondFrame.destroy()
        metricsPage(self.master, self.fig1, self.user_name, self.api_key)

########################################################################################################################
### Select the friends they want to unfollow

class metricsPage():

    def __init__(self, master, fig1, user_name, api_key):
        self.user_name = user_name
        self.api_key =api_key
        self.master = master
        self.fig1 = fig1
        self.thirdFrame = Frame(master)
        self.thirdFrame.grid()

        self.label0 = Label(self.thirdFrame, text = "Select accounts you want to unfollow", font = "Helvetica 20 bold")

        self.var1 = StringVar()
        self.label1 = Label(self.thirdFrame, text = "Followed by: ")
        self.comboxlist1 = ttk.Combobox(self.thirdFrame, textvariable = self.var1)
        self.comboxlist1["values"] = ("Yes", "No")
        self.comboxlist1.bind("<<ComboboxSelected>>", self.go)

        self.var3 = StringVar()
        self.label3 = Label(self.thirdFrame, text="Languages: ")
        self.comboxlist3 = ttk.Combobox(self.thirdFrame, textvariable=self.var3)
        self.comboxlist3["values"] = ("en", "pt", "nl", "ja", "und", "es", "da", "de", "it", "tl", "fr", "in", "ca", "zh", "sr", "sl", "sv", "ht", "ar", "ro", "ko" ,"hu", "pl", "ur", "iw", "fa", "el", "cs", "eu", "ta")
        self.comboxlist3.bind("<<ComboboxSelected>>", self.go)

        self.label4 = Label(self.thirdFrame, text="Number of favourites: ")
        self.label4_5 = Label(self.thirdFrame, text="-")
        self.entry1 = Entry(self.thirdFrame)
        self.entry2 = Entry(self.thirdFrame)

        self.label5 = Label(self.thirdFrame, text="Number of followers: ")
        self.label5_5 = Label(self.thirdFrame, text="-")
        self.entry3 = Entry(self.thirdFrame)
        self.entry4 = Entry(self.thirdFrame)

        self.label6 = Label(self.thirdFrame, text="Number of friends: ")
        self.label6_5 = Label(self.thirdFrame, text="-")
        self.entry5 = Entry(self.thirdFrame)
        self.entry6 = Entry(self.thirdFrame)

        self.button1 = Button(self.thirdFrame, text = "Search", command = self.changeFrame)
        self.button2 = Button(self.thirdFrame, text = "Back", command = self.goBack)

        self.label0.grid(row = 0, columnspan = 4, ipadx=50, ipady=100, padx = 100)
        self.label1.grid(row = 1,sticky = E)
        self.comboxlist1.grid(row = 1,column = 1)
        self.label3.grid(row = 3,pady = 10, sticky = E)
        self.comboxlist3.grid(row = 3, column = 1, pady = 10)

        self.label4.grid(row = 4, pady = 1, sticky = E)
        self.label4_5.grid(row = 4, column = 2,pady = 10)
        self.entry1.grid(row = 4, column = 1, pady = 10)
        self.entry2.grid(row = 4, column = 3, pady = 10)

        self.label5.grid(row=5, pady=1, sticky=E)
        self.label5_5.grid(row=5, column=2, pady=10)
        self.entry3.grid(row=5, column=1, pady=10)
        self.entry4.grid(row=5, column=3, pady=10)

        self.label6.grid(row=6, pady=1, sticky=E)
        self.label6_5.grid(row=6, column=2, pady=10)
        self.entry5.grid(row=6, column=1, pady=10)
        self.entry6.grid(row=6, column=3, pady=10)

        self.button1.grid(row = 7, column = 1, pady = 10)
        self.button2.grid(row = 7, column = 0, padx = 10)

        self.metric_list = []

    def go(self, *args):
        print(self.comboxlist1.get())
        print(args)

    def goBack(self,):
        self.thirdFrame.destroy()
        friendsPage(self.master, self.fig1, self.user_name, self.api_key)

    def changeFrame(self,):
        self.metric_list.append(self.comboxlist1.get())
        self.metric_list.append(self.comboxlist3.get())
        self.metric_list.append(self.entry1.get())
        self.metric_list.append(self.entry2.get())
        self.metric_list.append(self.entry3.get())
        self.metric_list.append(self.entry4.get())
        self.metric_list.append(self.entry5.get())
        self.metric_list.append(self.entry6.get())
        print(self.metric_list)
        self.thirdFrame.destroy()
        metricsNextPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

########################################################################################################################
###  return the unfollowing list

from twitterMetrics import unfollow_the_select

class metricsNextPage():

    def __init__(self, master, fig1, user_name, metric_list, api_key):
        self.master = master
        self.fig1 = fig1
        self.user_name = user_name
        self.metric_list = metric_list
        self.api_key = api_key
        self.ThirdFrame2 = Frame(master)
        self.ThirdFrame2.grid()

        self.label0 = Label(self.ThirdFrame2, text = "Select accounts you want to unfollow", font = "Helvetica 20 bold")
        self.button1 = Button(self.ThirdFrame2, text="Next", command=self.changeFrame)
        self.button2 = Button(self.ThirdFrame2, text = "Back", command = self.goBack)

        self.label0.grid(row=0, ipadx=50, ipady=10, padx=100)
        self.button1.grid(row=2, padx=50, sticky=E)
        self.button2.grid(row = 2, padx = 50, sticky = W)

        self.frame_canvas = Frame(self.ThirdFrame2)
        self.frame_canvas.grid(row=1, column=0)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.frame_figures = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_figures, anchor='nw')

        self.select_name = get_friends_name(self.user_name, metric_list)

        #here
        self.checkbuttons = [Checkbutton() for j in range(len(self.select_name))]
        self.vals = [IntVar() for j in range(len(self.select_name))]
        for i in range(0, len(self.select_name)):
            print(i)
            self.checkbuttons[i] = Checkbutton(self.frame_figures, text = self.select_name[i], variable = self.vals[i])
            self.checkbuttons[i].grid(row=i, sticky='news')

        self.frame_figures.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def goBack(self,):
        self.ThirdFrame2.destroy()
        metricsPage(self.master, self.fig1, self.user_name, self.api_key)

    def changeFrame(self,):
        name_list = []
        for i in range(0, len(self.vals)):
            if (self.vals[i].get() == 1):
                name_list.append(self.select_name[i])
        unfollow_the_select(self.user_name, name_list, self.api_key)
        self.ThirdFrame2.destroy()
        remainfollowPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

########################################################################################################################
### Select the friends they don't want to unfollow

class remainfollowPage():

    def __init__(self, master, fig1, user_name, metric_list_1, api_key):
        self.master = master
        self.fig1 = fig1
        self.user_name = user_name
        self.metric_list_1 = metric_list_1
        self.api_key = api_key
        self.fourthFrame = Frame(master)
        self.fourthFrame.grid()

        self.label0 = Label(self.fourthFrame, text = "Select accounts you want to remain", font = "Helvetica 20 bold")

        self.var1 = StringVar()
        self.label1 = Label(self.fourthFrame, text = "Followed by: ")
        self.comboxlist1 = ttk.Combobox(self.fourthFrame, textvariable = self.var1)
        self.comboxlist1["values"] = ("Yes", "No")
        self.comboxlist1.bind("<<ComboboxSelected>>", self.go)

        self.var3 = StringVar()
        self.label3 = Label(self.fourthFrame, text="Languages: ")
        self.comboxlist3 = ttk.Combobox(self.fourthFrame, textvariable=self.var3)
        self.comboxlist3["values"] = ("en", "pt", "nl", "ja", "und", "es", "da", "de", "it", "tl", "fr", "in", "ca", "zh", "sr", "sl", "sv", "ht", "ar", "ro", "ko" ,"hu", "pl", "ur", "iw", "fa", "el", "cs", "eu", "ta")
        self.comboxlist3.bind("<<ComboboxSelected>>", self.go)

        self.label4 = Label(self.fourthFrame, text="Number of favourites: ")
        self.label4_5 = Label(self.fourthFrame, text="-")
        self.entry1 = Entry(self.fourthFrame)
        self.entry2 = Entry(self.fourthFrame)

        self.label5 = Label(self.fourthFrame, text="Number of followers: ")
        self.label5_5 = Label(self.fourthFrame, text="-")
        self.entry3 = Entry(self.fourthFrame)
        self.entry4 = Entry(self.fourthFrame)

        self.label6 = Label(self.fourthFrame, text="Number of friends: ")
        self.label6_5 = Label(self.fourthFrame, text="-")
        self.entry5 = Entry(self.fourthFrame)
        self.entry6 = Entry(self.fourthFrame)

        self.button1 = Button(self.fourthFrame, text="Search", command=self.changeFrame)
        self.button2 = Button(self.fourthFrame, text="Back", command=self.goBack)

        self.label0.grid(row=0, columnspan=4, ipadx=50, ipady=100, padx=100)
        self.label1.grid(row=1, sticky=E)
        self.comboxlist1.grid(row=1, column=1)
        self.label3.grid(row=3, pady=10, sticky=E)
        self.comboxlist3.grid(row=3, column=1, pady=10)

        self.label4.grid(row=4, pady=1, sticky=E)
        self.label4_5.grid(row=4, column=2, pady=10)
        self.entry1.grid(row=4, column=1, pady=10)
        self.entry2.grid(row=4, column=3, pady=10)

        self.label5.grid(row=5, pady=1, sticky=E)
        self.label5_5.grid(row=5, column=2, pady=10)
        self.entry3.grid(row=5, column=1, pady=10)
        self.entry4.grid(row=5, column=3, pady=10)

        self.label6.grid(row=6, pady=1, sticky=E)
        self.label6_5.grid(row=6, column=2, pady=10)
        self.entry5.grid(row=6, column=1, pady=10)
        self.entry6.grid(row=6, column=3, pady=10)

        self.button1.grid(row = 7, column = 1, pady = 10)
        self.button2.grid(row = 7)

        self.metric_list = []

    def go(self, *args):
        print(self.comboxlist1.get())
        print(args)

    def goBack(self,):
        self.fourthFrame.destroy()
        metricsNextPage(self.master, self.fig1, self.user_name, self.metric_list_1, self.api_key)

    def changeFrame(self,):
        self.metric_list.append(self.comboxlist1.get())
        self.metric_list.append(self.comboxlist3.get())
        self.metric_list.append(self.entry1.get())
        self.metric_list.append(self.entry2.get())
        self.metric_list.append(self.entry3.get())
        self.metric_list.append(self.entry4.get())
        self.metric_list.append(self.entry5.get())
        self.metric_list.append(self.entry6.get())
        print(self.metric_list)
        self.fourthFrame.destroy()
        remainNextPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

########################################################################################################################
###  return the unfollowing list

from friendsanalysis import get_friends_name
from twitterMetrics import remain_the_select


class remainNextPage():

    def __init__(self, master, fig1, user_name, metric_list, api_key):
        self.master = master
        self.fig1 = fig1
        self.user_name = user_name
        self.metric_list = metric_list
        self.api_key = api_key
        self.fourthFrame2 = Frame(master)
        self.fourthFrame2.grid()

        self.label0 = Label(self.fourthFrame2, text = "Select accounts you want to remain", font = "Helvetica 20 bold")
        self.button1 = Button(self.fourthFrame2, text="Next", command=self.changeFrame)
        self.button2 = Button(self.fourthFrame2, text = "Back", command = self.goBack)

        self.label0.grid(row=0, ipadx=50, ipady=10, padx=100)
        self.button1.grid(row=2, padx=50, sticky=E)
        self.button2.grid(row = 2, padx = 50, sticky = W)

        self.frame_canvas = Frame(self.fourthFrame2)
        self.frame_canvas.grid(row=1, column=0)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.frame_figures = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_figures, anchor='nw')

        self.select_name = get_friends_name(self.user_name, metric_list)

        #here
        self.checkbuttons = [Checkbutton() for j in range(len(self.select_name))]
        self.vals = [IntVar() for j in range(len(self.select_name))]
        for i in range(0, len(self.select_name)):
            print(i)
            self.checkbuttons[i] = Checkbutton(self.frame_figures, text = self.select_name[i], variable = self.vals[i])
            self.checkbuttons[i].grid(row=i, sticky='news')

        self.frame_figures.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def goBack(self,):
        self.fourthFrame2.destroy()
        remainfollowPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

    def changeFrame(self,):
        name_list = []
        for i in range(0, len(self.vals)):
            if (self.vals[i].get() == 1):
                name_list.append(self.select_name[i])
        remain_the_select(self.user_name, name_list, self.api_key)
        self.fourthFrame2.destroy()
        mlPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

########################################################################################################################
### Machine learning page

from RF import rf

class mlPage():

    def __init__(self, master, fig1, user_name, metric_list, api_key):
        self.master = master
        self.fig1 = fig1
        self.user_name = user_name
        self.metric_list = metric_list
        self.api_key = api_key
        self.fifthFrame = Frame(master)
        self.fifthFrame.grid()

        self.label0 = Label(self.fifthFrame, text = "Auto-unfollow Friends", font = "Helvetica 20 bold")
        self.button1 = Button(self.fifthFrame, text = "Run", command = self.run_ml)
        self.button2 = Button(self.fifthFrame, text = "Next", command = self.changeFrame)
        self.button4 = Button(self.fifthFrame, text = "Back", command = self.goBack)

        self.label0.grid(row = 0, ipadx=50, ipady=50, padx = 150)
        self.button1.grid(row = 2, pady = 50)
        self.button2.grid(row = 3, padx = 50, sticky = E)
        self.button4.grid(row = 3, padx = 50, sticky = W)

    def run_ml(self,):
        self.recommend_unfollow_list = rf(self.user_name)

        self.button3 = Button(self.fifthFrame, text = "Unfollow", command = self.unfollow_select)
        self.button3.grid(row = 2, padx = 10,pady = 50)

        self.frame_canvas = Frame(self.fifthFrame)
        self.frame_canvas.grid(row=1, column=0)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, width=400, height=200)
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.frame_figures = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_figures, anchor='nw')

        # here
        self.checkbuttons = [Checkbutton() for j in range(len(self.recommend_unfollow_list))]
        self.vals = [IntVar() for j in range(len(self.recommend_unfollow_list))]
        for i in range(0, len(self.recommend_unfollow_list)):
            print(i)
            self.checkbuttons[i] = Checkbutton(self.frame_figures, text=self.recommend_unfollow_list[i], variable=self.vals[i])
            self.checkbuttons[i].grid(row=i, sticky='news')

        self.frame_figures.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def unfollow_select(self):
        self.name_list = []
        for i in range(0, len(self.vals)):
            if (self.vals[i].get() == 1):
                self.name_list.append(self.recommend_unfollow_list[i])
        unfollow_the_select(self.user_name, self.name_list, self.api_key)
        self.fifthFrame.destroy()
        followerPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

    def goBack(self,):
        self.fifthFrame.destroy()
        remainNextPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

    def changeFrame(self, ):
        self.fifthFrame.destroy()
        followerPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

########################################################################################################################
### Follower analysing page
from getfollower import get_follower
from followeranalysis import follower_analy

class followerPage():

    def __init__(self, master, fig, user_name, metric_list, api_key):
        self.master = master
        self.fig = fig
        self.user_name = user_name
        self.metric_list = metric_list
        self.api_key = api_key
        self.sixthFrame = Frame(master)
        self.sixthFrame.grid()

        self.fig1 = get_follower(self.user_name, self.api_key)
        #time_series(self.user_name)
        self.fig2, self.fig3, high_val_user, high_influ_user, active_user, low_val_user = follower_analy(self.user_name)

        self.label0 = Label(self.sixthFrame, text = "Visualisation - Followers", font = "Helvetica 20 bold")
        self.label0.grid(row = 0, ipadx=50, ipady=20, padx = 220)
        self.button1 = Button(self.sixthFrame, text = "Back", command = self.goBack)
        self.button1.grid(row = 2, padx = 50, sticky = W)

        self.frame_canvas = Frame(self.sixthFrame)
        self.frame_canvas.grid(row=1, column=0)

        # Add a canvas in that frame
        self.canvas = Canvas(self.frame_canvas, width=640, height=400)
        self.canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        self.vsb = Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.frame_figures = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_figures, anchor='nw')

        self.text = Text(self.frame_figures)
        self.text.insert(END, "High value user:\n")
        self.text.insert(END, high_val_user)
        self.text.insert(END, "\n\nHigh influence user:\n")
        self.text.insert(END, high_influ_user)
        self.text.insert(END, "\n\nActive user:\n")
        self.text.insert(END, active_user)
        self.text.insert(END, "\n\nLow value user:\n")
        self.text.insert(END, low_val_user)
        self.text.grid(row=0)

        self.canvas0 = FigureCanvasTkAgg(self.fig1, self.frame_figures)
        self.canvas0.draw()
        self.canvas0.get_tk_widget().grid(row=1, ipady=50)

        self.canvas1 = FigureCanvasTkAgg(self.fig2, self.frame_figures)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=2, ipady=50)


        self.canvas1 = FigureCanvasTkAgg(self.fig3, self.frame_figures)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().grid(row=3, ipady=50)

        self.frame_figures.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def goBack(self,):
        self.sixthFrame.destroy()
        mlPage(self.master, self.fig1, self.user_name, self.metric_list, self.api_key)

# create a blank window
root = Tk()
tm = twitterMatrics(root)
root.mainloop()