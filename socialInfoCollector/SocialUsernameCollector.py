import sys
import time
#sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')
#sys.path.insert(0,'./socialInfoCollector')
#sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector')
#sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')
#sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\SocialLinkCollector.py')
import re
import pandas as pd
#from SocialLinkCollector import socialLinkCollector


def socialUsernameCollector(instagram_link, facebook_link,linkedin_link,twitter_link):
    st=time.time()
    path = "DigiScore\\test.csv"
    #instagram_link, facebook_link,linkedin_link = socialLinkCollector(url)
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
            linkedin_username = re.search('linkedin.com/([^/]+)/?', linkedin_link).group(1)
            print('LinkedIn Username:', linkedin_username)
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


