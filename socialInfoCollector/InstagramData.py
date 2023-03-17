import requests
from bs4 import BeautifulSoup
import re
import instaloader
import pandas as pd
from instagramy import InstagramUser
from socialInfoCollector.SocialUsernameCollector import socialUsernameCollector
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
    # Connecting the profile