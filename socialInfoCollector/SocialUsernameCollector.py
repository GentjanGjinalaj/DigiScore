import time
import re
import pandas as pd


def socialUsernameCollector(instagram_link, facebook_link,linkedin_link,twitter_link):
    st=time.time()
    #path = "DigiScore\\test.csv"
    path = "test.csv"

    if instagram_link:
        # Extract the username from the link using regular expressions
            instagram_username = re.search('instagram.com/([^/]+)/?', instagram_link).group(1)
            print('Instagram Username:', instagram_username)
    else:
            print("No Instagram username found.")
            instagram_username=None
        # Extract the username from the link using regular expressions
    if facebook_link:
            facebook_username = re.search('facebook.com/([^/]+)/?', facebook_link).group(1)
            print('Facebook Username:', facebook_username)
    else:
            print("No Facebook username found.")
            facebook_username=None
        # Extract the username from the link using regular expressions
    if linkedin_link:
        pattern = 'https:\/\/www\.linkedin\.com\/.+?\/(.+?)\/'
        match = re.search(pattern, linkedin_link)
        if match:
            linkedin_username = match.group(1)
            print('LinkedIn Username:', linkedin_username)
        else:
            linkedin_username=None
    else:
        print("No LinkedIn username found.")
        linkedin_username=None
    if twitter_link:
        # extract the username/handle from the link using regex
        username_regex = r"https?://(?:www\.)?twitter\.com/([A-Za-z0-9_]+)"
        username_match = re.match(username_regex, twitter_link)
        twitter_username = username_match.group(1)
        print('Twitter Username:', twitter_username)
    else:
        print("No Twitter Username Found.")
        twitter_username=None

    df = pd.read_csv(path)
    df["Social Platform Username"] = instagram_username
    df.to_csv(path, index=False)
    et=time.time()
    username_time=et-st
    print('Total execution time of SocialUsernameCollector.py is:',username_time)

    return instagram_username,facebook_username,linkedin_username,twitter_username,username_time


