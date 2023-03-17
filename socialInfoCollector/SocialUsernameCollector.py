import requests
from bs4 import BeautifulSoup
import re
import instaloader
import pandas as pd
from instagramy import InstagramUser
from socialInfoCollector.SocialLinkCollector import socialPlatformsUrl


def socialUsernameCollector(url):
    instagram_link, facebook_link,linkedin_link = socialPlatformsUrl(url)
    
    if instagram_link:
        # Extract the username from the link using regular expressions
            instagram_username = re.search('instagram.com/([^/]+)/?', instagram_link).group(1)
            print('Instagram Username:', instagram_username)
    else:
            print("No Instagram username found.")
        # Extract the username from the link using regular expressions
    if facebook_link:
            facebook_username = re.search('facebook.com/([^/]+)/?', facebook_link).group(1)
            print('Facebook Username:', facebook_username)
    else:
            print("No Facebook username found.")
        # Extract the username from the link using regular expressions
    if linkedin_link:
            linkedin_username = re.search('linkedin.com/([^/]+)/?', linkedin_link).group(1)
            print('LinkedIn Username:', linkedin_username)
    else:
        print("No LinkedIn username found.")

    return instagram_username,facebook_username,linkedin_username


