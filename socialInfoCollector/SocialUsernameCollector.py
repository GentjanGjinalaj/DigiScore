import sys
#sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')
#sys.path.insert(0,'./socialInfoCollector')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\SocialLinkCollector.py')
import re
import pandas as pd
#from SocialLinkCollector import socialLinkCollector


def socialUsernameCollector(instagram_link, facebook_link,linkedin_link):
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

    path = "C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test.csv"
    df = pd.read_csv(path)
    df["Instagram Username"] = instagram_username
    df.to_csv(path, index=False)

    return instagram_username,facebook_username,linkedin_username


