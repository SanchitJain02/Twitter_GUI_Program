#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import tkinter as tk
from tkinter import ttk,messagebox
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# In[2]:


root = Tk()
root.title("Twitter App")
root.geometry("1300x695")
root.resizable(False,False)

consumer_key = "dkJmeyfZH81HSOFfwTdSkST99"
consumer_secret = "p1iv1RpTKj7Uh2wmOwjeqTtxdYpfp28U3RURW7eweBn01DV0LK"
access_token = "1250285356487856128-dSkMsYzWvbCALvpJgj1ZH1vimPmZ3K"
access_token_secret = "n2VqtQmzdRnFGct2SOAw8v0ozsud9zIWclDkaBiVpK3rp"

def getTweets():
    try:
        username = textfield.get()
        auth = tweepy.OAuthHandler(consumer_key,consumer_secret) # Create an authentication project
        auth.set_access_token(access_token,access_token_secret)  # set the access token and ats 
        api = tweepy.API(auth,wait_on_rate_limit = True) 
        tweets = api.user_timeline(screen_name = username,count = 200,lang = "en",tweet_mode = "extended")
        recent_tweet = tweets[0].full_text
        lt.insert(END,recent_tweet)
        df = pd.DataFrame([tweet.full_text for tweet in tweets],columns = ["Tweets"])
        
        def cleantweets(text):
            text = re.sub(r"@[A-Za-z0-9]+","",text)     # remove the @mentions
            text = re.sub(r"#","",text)                 # remove the # symbol
            text = re.sub(r"RT[\s]","",text)            # removing retweets
            text = re.sub(r"https:\/\/\S+","",text)    # remove the hyperlink
        
        df["Tweets"] = df["Tweets"].apply(cleantweets)

    except Exception as e:
        messagebox.showerror("Twitter App","Invalid Entry!!!")    
        

def top_trends():
    username = textfield.get()
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret) # Create an authentication project
    auth.set_access_token(access_token,access_token_secret)  # set the access token and ats 
    api = tweepy.API(auth,wait_on_rate_limit = True) 
    country_input = textfield1.get()
    def get_woeid(place):
        '''Get woeid by location'''
        try:
            trends = api.available_trends()
            for val in trends:
                if (val['name'].lower() == place.lower()):
                    return(val['woeid']) 
            print('Location Not Found')
        except Exception as e:
            print('Exception:',e)
            return(0)

    def get_trends_by_location(loc_id,count):
        '''Get Trending Tweets by Location'''
        import iso639
        try:
            trends = api.get_place_trends(loc_id)
            df = pd.DataFrame([trending['name'],  trending['tweet_volume']] for trending in trends[0]['trends'])
            df.columns = ['Trends','Volume']
            #df = df.sort_values('Volume', ascending = False)
            return(df[:count])
        except Exception as e:
            print("An exception occurred",e)


    df_country_trends = get_trends_by_location(get_woeid(country_input), 10)
    tt.insert(END,df_country_trends.loc[:,["Trends","Volume"]])
    
    df_world_trends = get_trends_by_location(1, 10)
    wt.insert(END,df_world_trends.loc[:,["Trends","Volume"]])
    
      
def sentiment_analysis():
    username = textfield.get()
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret) # Create an authentication project
    auth.set_access_token(access_token,access_token_secret)  # set the access token and ats 
    api = tweepy.API(auth,wait_on_rate_limit = True) 
    tweets = api.user_timeline(screen_name = username,count = 200,lang = "en",tweet_mode = "extended")
    df = pd.DataFrame([tweet.full_text for tweet in tweets],columns = ["Tweets"])
    def cleantweets(text):
        text = re.sub(r"@[A-Za-z0-9]+","",text)     # remove the @mentions
        text = re.sub(r"#","",text)                 # remove the # symbol
        text = re.sub(r"RT[\s]","",text)            # removing retweets
        text = re.sub(r"https:\/\/\S+","",text)    # remove the hyperlink
        return text
    df["Tweets"] = df["Tweets"].apply(cleantweets)
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(text):
        return TextBlob(text).sentiment.polarity
    df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
    df["Polarity"] = df["Tweets"].apply(getPolarity)
    def getAnalysis(score):
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"
    df["Analysis"] = df["Polarity"].apply(getAnalysis)
    final_df = pd.DataFrame(df["Analysis"].value_counts())
    sortedDF_neg = df.sort_values(by = ["Polarity"])
    sortedDF_pos = df.sort_values(by = ["Polarity"],ascending = False)
    latest_negative_tweet = sortedDF_neg.head(1)['Tweets'].values[0]
    latest_positive_tweet = sortedDF_pos.head(1)['Tweets'].values[0]
    lpt.insert(END,latest_positive_tweet)
    lnt.insert(END,latest_negative_tweet)
    def plot():
        f = Figure(figsize=(4.8,4), dpi=100)
        ax = f.add_subplot(111)
        width = 0.5
        rects1 = ax.bar(final_df.index,final_df["Analysis"] ,width)
        canvas = FigureCanvasTkAgg(f, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x = 370,y= 240)
        
    plot()    
    
           
def delete():
    lt.delete("1.0","end")
    tt.delete("1.0","end")
    wt.delete("1.0","end")
    lnt.delete("1.0","end")
    lpt.delete("1.0","end")
    

    
    
label0 = Label(root,text = "Enter the name of Personality: ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label0.place(x = 20,y = 10)

Search_image = PhotoImage(file = "search.png")
myimage = Label(image = Search_image)
myimage.place(x = 0,y=38)

textfield = tk.Entry(root,justify = "center",width = 17,font = ("poopins",25,"bold"),bg = "#404040",border = 0,fg = "white")
textfield.place(x = 30,y = 58)
textfield.focus()        

Search_icon = PhotoImage(file = "search_icon.png")
myimage_icon = Button(image = Search_icon,borderwidth = 0,cursor = "hand2",bg = "#404040",command = getTweets)
myimage_icon.place(x = 380,y = 52)

#Logo_image = PhotoImage(file = "logo.png")
#logo = Label(image = Logo_image)
#logo.place(x = 100,y = 130)

label1 = Label(root,text = "Latest Tweet: ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label1.place(x = 20,y = 120)

lt = Text(root, borderwidth = 2,wrap = "word",width =42,height = 8)
lt.place(x = 20,y = 160)

label5 = Label(root,text = "Highest Positive Tweet: ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label5.place(x = 20,y = 300)

lpt = Text(root, borderwidth = 2,wrap = "word",width =42,height = 8)
lpt.place(x = 20,y = 340)

label6 = Label(root,text = "Highest Negative Tweet: ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label6.place(x = 20,y = 480)

lnt = Text(root, borderwidth = 2,wrap = "word",width =42,height = 8)
lnt.place(x = 20,y = 520)

b1 = Button(root,height=2,width=10, text = "Clear All",font= ('Helvetica 20 bold'),  command = delete)
b1.pack()

b2 = Button(root,height=3,width=10, text = "Sentiment \n Analysis",font= ('Helvetica 20 bold'),  command = sentiment_analysis)
b2.place(x = 560,y = 120)


label2 = Label(root,text = "Enter the name of Country: ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label2.place(x = 850,y = 10)

Search_image1 = PhotoImage(file = "search.png")
myimage1 = Label(image = Search_image1)
myimage1.place(x = 825,y=38)

textfield1 = tk.Entry(root,justify = "center",width = 17,font = ("poopins",25,"bold"),bg = "#404040",border = 0,fg = "white")
textfield1.place(x = 855,y = 58)
textfield1.focus()        

Search_icon1 = PhotoImage(file = "search_icon.png")
myimage_icon1 = Button(image = Search_icon1,borderwidth = 0,cursor = "hand2",bg = "#404040",command = top_trends)
myimage_icon1.place(x = 1205,y = 52)

label3 = Label(root,text = "Top 10 Trending Topics : ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label3.place(x = 850,y = 120)

tt = Text(root, borderwidth = 2,wrap = "word",width =50,height = 11)
tt.place(x = 850,y = 160)

label4 = Label(root,text = "Top 10 Trending Topics of World : ",font=("Helvetica",15,"bold"),fg = "white",bg = "#157DEC")
label4.place(x = 850,y = 360)

wt = Text(root, borderwidth = 2,wrap = "word",width =50,height = 11)
wt.place(x = 850,y = 408)

root.mainloop()


# In[ ]:




