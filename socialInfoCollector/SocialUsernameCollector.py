import time
import re
import pandas as pd


def socialUsernameCollector(instagram_link, facebook_link,linkedin_link,twitter_link):
    st=time.time()
    #return None,None,None,None,0
    print('Started executing SocialUsernameCollector.py')

    #path = "DigiScore\\test.csv"
    path = "test.csv"

    # Helper function to add 'https' if missing
    def add_https_if_missing(link):
        if link and link.startswith('//'):
            link = 'https:' + link
        elif link and link.startswith('www.'):
            link = 'https://' + link
        return link

    # Helper function to extract username from the link
    def extract_username(link, platform):
        try:
            link = add_https_if_missing(link)
            username = re.search(f'{platform}.com/([^/?]+)', link)
            if username is not None:
                return username.group(1)
            return None
        except Exception as e:
            print(f'Error occurred while extracting username for {platform}: {e}')
            return None

    # Function to handle different types of LinkedIn usernames
    def get_linkedin_username(link):
        try:
            link = add_https_if_missing(link)
            personal_profile = re.search("linkedin.com/in/([^/?]+)", link)
            school_profile = re.search("linkedin.com/school/([^/?]+)", link)
            company_page = re.search("linkedin.com/company/([^/?]+)", link)
            showcase_page = re.search("linkedin.com/showcase/([^/?]+)", link)
            group_page = re.search("linkedin.com/groups/([^/?]+)", link)

            if personal_profile is not None:
                return personal_profile.group(1)
            elif school_profile is not None:
                return school_profile.group(1)
            elif company_page is not None:
                return company_page.group(1)
            elif showcase_page is not None:
                return showcase_page.group(1)
            elif group_page is not None:
                return group_page.group(1)
            else:
                return None
        except Exception as e:
            print(f'Error occurred while extracting LinkedIn username: {e}')
            return None

    instagram_username = extract_username(instagram_link, 'instagram') if instagram_link else None
    print('Instagram Username:', instagram_username)

    facebook_username = extract_username(facebook_link, 'facebook') if facebook_link else None
    print('Facebook Username:', facebook_username)

    linkedin_username = get_linkedin_username(linkedin_link) if linkedin_link else None
    print('LinkedIn Username:', linkedin_username)

    twitter_username = extract_username(twitter_link, 'twitter') if twitter_link else None
    print('Twitter Username:', twitter_username)

    try:
        df = pd.read_csv(path)
        df["Social Platform Username"] = instagram_username
        df.to_csv(path, index=False)

    except Exception as e:
        print(f'Error occurred while working with DataFrame: {e}')

    et = time.time()
    username_time = et-st
    print('Total execution time of SocialUsernameCollector.py is:', username_time)

    return instagram_username, facebook_username, linkedin_username, twitter_username, username_time

#socialUsernameCollector('https://www.instagram.com/icdparis/?hl=fr/', 'https://www.facebook.com/icd.paris/', 'https://www.linkedin.com/school/icd-internationalbusinessschool/', '/twitter.com/icd.paris/')



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################



def socialUsernameCollectorCompetitor(instagram_link, facebook_link,linkedin_link,twitter_link,competitor_num):
    st=time.time()
    #return None,None,None,None,0
    print('Started executing SocialUsernameCollectorCompetitor.py')

    #path = "DigiScore\\DataML\\Competitors\\socialCompetitor_{competitor_num}.csv"
    path = f"DataML\\Competitors\\socialCompetitor_{competitor_num}.csv"

    # Helper function to add 'https' if missing
    def add_https_if_missing(link):
        if link and link.startswith('//'):
            link = 'https:' + link
        elif link and link.startswith('www.'):
            link = 'https://' + link
        return link

    # Helper function to extract username from the link
    def extract_username(link, platform):
        try:
            link = add_https_if_missing(link)
            username = re.search(f'{platform}.com/([^/?]+)', link)
            if username is not None:
                return username.group(1)
            return None
        except Exception as e:
            print(f'Error occurred while extracting username for {platform}: {e}')
            return None

    # Function to handle different types of LinkedIn usernames
    def get_linkedin_username(link):
        try:
            link = add_https_if_missing(link)
            personal_profile = re.search("linkedin.com/in/([^/?]+)", link)
            school_profile = re.search("linkedin.com/school/([^/?]+)", link)
            company_page = re.search("linkedin.com/company/([^/?]+)", link)
            showcase_page = re.search("linkedin.com/showcase/([^/?]+)", link)
            group_page = re.search("linkedin.com/groups/([^/?]+)", link)

            if personal_profile is not None:
                return personal_profile.group(1)
            elif school_profile is not None:
                return school_profile.group(1)
            elif company_page is not None:
                return company_page.group(1)
            elif showcase_page is not None:
                return showcase_page.group(1)
            elif group_page is not None:
                return group_page.group(1)
            else:
                return None
        except Exception as e:
            print(f'Error occurred while extracting LinkedIn username: {e}')
            return None

    instagram_username = extract_username(instagram_link, 'instagram') if instagram_link else None
    print('Instagram Username:', instagram_username)

    facebook_username = extract_username(facebook_link, 'facebook') if facebook_link else None
    print('Facebook Username:', facebook_username)

    linkedin_username = get_linkedin_username(linkedin_link) if linkedin_link else None
    print('LinkedIn Username:', linkedin_username)

    twitter_username = extract_username(twitter_link, 'twitter') if twitter_link else None
    print('Twitter Username:', twitter_username)

    try:
        df = pd.read_csv(path)
        df["Social Platform Username"] = instagram_username
        df.to_csv(path, index=False)

    except Exception as e:
        print(f'Error occurred while working with DataFrame: {e}')

    et = time.time()
    username_time = et-st
    print('Total execution time of SocialUsernameCollectorCompetitor.py is:', username_time)

    return instagram_username, facebook_username, linkedin_username, twitter_username, username_time

#socialUsernameCollectorCompetitor('https://www.instagram.com/icdparis/?hl=fr/','https://www.facebook.com/icd.paris/','https://www.linkedin.com/school/icd-internationalbusinessschool/','/twitter.com/icd.paris/',1)
