import csv
import requests
from bs4 import BeautifulSoup
import re
import instaloader
import pandas as pd
from instagramy import InstagramUser
from socialInfoCollector.SocialUsernameCollector import socialUsernameCollector
import instaloader
import itertools


def instaData(url):
    instagram_username,facebook_username,linkedin_username = socialUsernameCollector(url)
# Creating an instance of the Instaloader class
    bot = instaloader.Instaloader()
    #outlook email = datadigitest@hotmail.com
    #outlook password = Digitalized1243
    #Instagram username=data_digi_test
    #Instagram password=Digitalized1243
    # Loading the profile from an Instagram handle
    profile = instaloader.Profile.from_username(bot.context, instagram_username)
    print("Username: ", profile.username)
    print("User ID: ", profile.userid)
    print("Number of Posts: ", profile.mediacount)
    print("Followers Count: ", profile.followers)
    print("Following Count: ", profile.followees)
    print("Bio: ", profile.biography)
    print("External URL: ", profile.external_url)

    # Create an instance of Instaloader class
    L = instaloader.Instaloader()

    # Login to Instagram (if required)
    # L.load_session_from_file(username) # load session if previously saved

    # Retrieve the profile of the user
    profile = instaloader.Profile.from_username(L.context, instagram_username)

    # Get the posts of the user
    posts = itertools.islice(profile.get_posts(),5)
    likess=[]
    commentss=[]
    # Iterate over the last 5 posts and collect the likes and comments count
    for post in posts:

    # Get the number of likes and comments
        likes = post.likes
        comments = post.comments

        # Print the number of likes and comments
        print(f"Post {post.shortcode} has {likes} likes and {comments} comments")
        likess.append(likes)
        commentss.append(comments)
        # Connecting the profile

    '''data={'Username':profile.username,"Followers Count":profile.followers,'Following Count':profile.followees}
    df=pd.DataFrame(data)
    df.to_csv('data.csv',index=False)'''

    '''headers=['Username','Followers Count','Following Count']
    data=pd.DataFrame({'Followers Count':[profile.followers],'Following Count':[profile.followees],'Post 1 Likes':[likess[0]],"Post 1 Comments":[commentss[0]],
                       'Post 2 Likes':[likess[1]],"Post 2 Comments":[commentss[1]],'Post 3 Likes':[likess[2]],"Post 3 Comments":[commentss[2]],'Post 4 Likes':[likess[3]],"Post 4 Comments":[commentss[3]]
                       ,'Post 5 Likes':[likess[4]],"Post 5 Comments":[commentss[4]]})
    #with open('students.csv', 'w') as file:
    #writer = csv.DictWriter(file,fieldnames=headers)
     #writer.writerow(data)'''
    
    
    #data.to_csv("test.csv",index=False, index_label=None)
    #print(data)

    #with open('test.csv', 'a') as f:
       # data.to_csv(f,index=False, index_label=None,header=True)

    df = pd.read_csv("test.csv")
    df["Followers Count"] = profile.followers
    df['Following Count']=profile.followees
    df['Post 1 Likes']=likess[0]
    df['Post 1 Comments']=commentss[0]
    df['Post 2 Likes']=likess[1]
    df['Post 2 Comments']=commentss[1]
    df['Post 3 Likes']=likess[2]
    df['Post 3 Comments']=commentss[2]
    df['Post 4 Likes']=likess[3]
    df['Post 4 Comments']=commentss[3]
    df['Post 5 Likes']=likess[4]
    df['Post 5 Comments']=commentss[4]
    df.to_csv("test.csv", index=False,index_label=None)