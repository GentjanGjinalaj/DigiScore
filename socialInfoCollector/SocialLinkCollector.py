import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def socialLinkCollector(url):
    st=time.time()
    #return None,None,None,None,0
    print('Started executing socialLinkCollector.py')
    #path = "DigiScore\\test.csv"
    path = "test.csv"
    if url:

        response=None

        try:
            # code that might raise an exception
            #response = requests.get(url, timeout= 5)
            response = requests.get(url)
            print(response.status_code)
            response.raise_for_status() # raise HTTPError for 404 Not Found
        except requests.exceptions.SSLError:
            # code to handle the SSL error
            response = requests.get(url, verify=False)
        except requests.exceptions.HTTPError as http_err:
            # code to handle HTTP errors
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            # code to handle other exceptions
            print("An error occurred:", e)

        if response and response.status_code == 200:
            # Parse the HTML content of the webpage using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the first anchor tag with href attribute containing "instagram.com"
            instagram_links = soup.find_all("a", href=lambda href: href and "instagram.com" in href)
            instagram_link=None
            if instagram_links:
                instagram_link = instagram_links[0]["href"]
                print("Instagram link:", instagram_link)
            else:
                print("No Instagram link found.")
                instagram_link=None

            '''# Find the first anchor tag with href attribute containing "instagram.com"
            instagram_links = soup.find_all("a", href=lambda href: href and "instagram.com" in href)
            instagram_link=None
            for link in instagram_links:
                match = re.match(r"(?:https?:)?//(?:www\.)?instagram.com/([^/]+)(?:/)?$", link["href"])
                if match:
                    instagram_link = match.group(0)
                    break
            if instagram_link:
                print("Instagram link:", instagram_link)
            else:
                print("No valid Instagram link found.")
                instagram_link=None'''

            # Find the first anchor tag with href attribute containing "facebook.com"
            facebook_links = soup.find_all("a", href=lambda href: href and "facebook.com" in href)
            facebook_link = None
            for link in facebook_links:
                match = re.match(r"(?:https?:)?//(?:www\.)?facebook.com/([^/]+)(?:/)?$", link["href"])
                if match:
                    facebook_link = match.group(0)
                    break

            if facebook_link:
                print("Facebook link:", facebook_link)
            else:
                print("No valid Facebook link found.")


            # Find the first anchor tag with href attribute containing "linkedin.com"
            linkedin_links = soup.find_all("a", href=lambda href: href and "linkedin.com" in href)
            linkedin_link=None
            if linkedin_links:
                linkedin_link = linkedin_links[0]["href"]
                print("LinkedIn link:", linkedin_link)
            else:
                print("No LinkedIn link found.")
                linkedin_link=None

            # Find the first anchor tag with href attribute containing "twitter.com"
            twitter_links = soup.find_all("a", href=lambda href: href and "twitter.com" in href)
            twitter_link=None
            for link in twitter_links:
                match = re.match(r"(?:https?:)?//(?:www\.)?twitter.com/([^/]+)(?:/)?$", link["href"])
                match1 = re.match(r"(?:https?:)?//(?:www\.)?x.com/([^/]+)(?:/)?$", link["href"])
                match2 = re.match(r"(?:https?:)?//(?:www\.)?X.com/([^/]+)(?:/)?$", link["href"])
                if match:
                    twitter_link = match.group(0)
                    break
                elif match1:
                    twitter_link = match1.group(0)
                    break
                elif match2:
                    twitter_link = match2.group(0)
                    break

            if twitter_link:
                print("Twitter link:", twitter_link)
            else:
                print("No valid Twitter link found.")

            # Find all anchor tags with href attribute containing "instagram.com", "facebook.com", or "linkedin.com"
            mixed_links = [a["href"] for a in soup.find_all("a", href=lambda href: href and ("instagram.com" in href or "facebook.com" in href or "linkedin.com" in href or "twitter.com in href"))]

            # Print the links
            #print("Mixed links:", mixed_links)
            try:
                data=pd.DataFrame({'Social Platform Link':[instagram_link]})
                data.to_csv(path,index=False, index_label=None)
            except Exception as e:
                print(f'Error occurred while working with DataFrame: {e}')
            et=time.time()
            links_time=et-st
            print('Total execution time of SocialLinkCollector.py is:',links_time)
        else:
            print(f"No URL found or the URL is wrong: {url}")
            instagram_link=None
            facebook_link=None
            linkedin_link=None
            twitter_link=None
            try:
                data=pd.DataFrame({'Social Platform Link':[instagram_link]})
                data.to_csv(path,index=False, index_label=None)
            except Exception as e:
                print(f'Error occurred while working with DataFrame: {e}')
            et=time.time()
            links_time=et-st
            print('Total execution time of SocialLinkCollector.py is:',links_time)

            return instagram_link,facebook_link,linkedin_link,twitter_link,links_time

        '''instagram_link=None
        facebook_link=None
        linkedin_link=None
        twitter_link=None
        data=pd.DataFrame({'Social Platform Link':[instagram_link]})
        data.to_csv(path,index=False, index_label=None)
        et=time.time()
        links_time=et-st
        print('Total execution time of SocialLinkCollector.py is:',links_time)

        return instagram_link,facebook_link,linkedin_link,twitter_link,links_time'''

    else:
        print("No URL found or the URL is wrong:",url)

        instagram_link=None
        facebook_link=None
        linkedin_link=None
        twitter_link=None
        try:
            data=pd.DataFrame({'Social Platform Link':[instagram_link]})
            data.to_csv(path,index=False, index_label=None)
        except Exception as e:
            print(f'Error occurred while working with DataFrame: {e}')
        et=time.time()
        links_time=et-st
        print('Total execution time of SocialLinkCollector.py is:',links_time)

    return instagram_link,facebook_link,linkedin_link,twitter_link,links_time

#socialLinkCollector('https://www.icd-ecoles.com/')
#socialLinkCollector('https://www.lescausantes.com/')

'''
        # create a list of column names
        columns = ['Social Platform Link', 'Social Platform Name','Page Like Count','Social Platform Username', 'Followers Count','Following Count','Average Likes per 5 posts','Average Comments per 5 posts','Avarage Retweets per 5 posts']

        # create an empty DataFrame with the specified columns
        data = pd.DataFrame(columns=columns)
        data["Social Platform Link"] = instagram_link
        data.to_csv(path,index=False, index_label=None)
'''


##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################




def socialLinkCollectorCompetitor(url,competitor_num):
    st=time.time()
    #return None,None,None,None,0
    print('Started executing socialLinkCollectorCompetitor.py')

    #path = "DigiScore\\DataML\\Competitors\\socialCompetitor_{competitor_num}.csv"
    #path = f"DataML\\Competitors\\socialCompetitor_{competitor_num}.csv"
    path = os.path.join('DataML', 'Competitors', f'socialCompetitor_{competitor_num}.csv')
    if url:

        response=None

        try:
            # code that might raise an exception
            #response = requests.get(url, timeout= 5)
            response = requests.get(url)
            print(response.status_code)
            response.raise_for_status() # raise HTTPError for 404 Not Found
        except requests.exceptions.SSLError:
            # code to handle the SSL error
            response = requests.get(url, verify=False)
        except requests.exceptions.HTTPError as http_err:
            # code to handle HTTP errors
            print(f"HTTP error occurred: {http_err}")
        except Exception as e:
            # code to handle other exceptions
            print("An error occurred:", e)

        if response and response.status_code == 200:
            # Parse the HTML content of the webpage using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the first anchor tag with href attribute containing "instagram.com"
            instagram_links = soup.find_all("a", href=lambda href: href and "instagram.com" in href)
            instagram_link=None
            if instagram_links:
                instagram_link = instagram_links[0]["href"]
                print("Instagram link:", instagram_link)
            else:
                print("No Instagram link found.")
                instagram_link=None

            '''# Find the first anchor tag with href attribute containing "instagram.com"
            instagram_links = soup.find_all("a", href=lambda href: href and "instagram.com" in href)
            instagram_link=None
            for link in instagram_links:
                match = re.match(r"(?:https?:)?//(?:www\.)?instagram.com/([^/]+)(?:/)?$", link["href"])
                if match:
                    instagram_link = match.group(0)
                    break

            if instagram_link:
                print("Instagram link:", instagram_link)
            else:
                print("No valid Instagram link found.")
                instagram_link=None'''

            # Find the first anchor tag with href attribute containing "facebook.com"
            facebook_links = soup.find_all("a", href=lambda href: href and "facebook.com" in href)
            facebook_link = None
            for link in facebook_links:
                match = re.match(r"(?:https?:)?//(?:www\.)?facebook.com/([^/]+)(?:/)?$", link["href"])
                if match:
                    facebook_link = match.group(0)
                    break

            if facebook_link:
                print("Facebook link:", facebook_link)
            else:
                print("No valid Facebook link found.")


            # Find the first anchor tag with href attribute containing "linkedin.com"
            linkedin_links = soup.find_all("a", href=lambda href: href and "linkedin.com" in href)
            linkedin_link=None
            if linkedin_links:
                linkedin_link = linkedin_links[0]["href"]
                print("LinkedIn link:", linkedin_link)
            else:
                print("No LinkedIn link found.")
                linkedin_link=None

            # Find the first anchor tag with href attribute containing "twitter.com"
            twitter_links = soup.find_all("a", href=lambda href: href and "twitter.com" in href)
            twitter_link=None
            for link in twitter_links:
                match = re.match(r"(?:https?:)?//(?:www\.)?twitter.com/([^/]+)(?:/)?$", link["href"])
                match1 = re.match(r"(?:https?:)?//(?:www\.)?x.com/([^/]+)(?:/)?$", link["href"])
                match2 = re.match(r"(?:https?:)?//(?:www\.)?X.com/([^/]+)(?:/)?$", link["href"])
                if match:
                    twitter_link = match.group(0)
                    break
                elif match1:
                    twitter_link = match1.group(0)
                    break
                elif match2:
                    twitter_link = match2.group(0)
                    break

            if twitter_link:
                print("Twitter link:", twitter_link)
            else:
                print("No valid Twitter link found.")

            # Find all anchor tags with href attribute containing "instagram.com", "facebook.com", or "linkedin.com"
            mixed_links = [a["href"] for a in soup.find_all("a", href=lambda href: href and ("instagram.com" in href or "facebook.com" in href or "linkedin.com" in href or "twitter.com in href"))]

            # Print the links
            #print("Mixed links:", mixed_links)
            try:
                data=pd.DataFrame({'Social Platform Link':[instagram_link]})
                data.to_csv(path,index=False, index_label=None)
            except Exception as e:
                print(f'Error occurred while working with DataFrame: {e}')

            et=time.time()
            links_time=et-st
            print('Total execution time of SocialLinkCollector.py is:',links_time)
        else:
            print(f"No URL found or the URL is wrong: {url}")
            instagram_link=None
            facebook_link=None
            linkedin_link=None
            twitter_link=None
            try:
                data=pd.DataFrame({'Social Platform Link':[instagram_link]})
                data.to_csv(path,index=False, index_label=None)

            except Exception as e:
                print(f'Error occurred while working with DataFrame: {e}')

            et=time.time()
            links_time=et-st
            print('Total execution time of socialLinkCollectorCompetitor.py is:',links_time)
            return instagram_link,facebook_link,linkedin_link,twitter_link,links_time

        '''instagram_link=None
        facebook_link=None
        linkedin_link=None
        twitter_link=None
        data=pd.DataFrame({'Social Platform Link':[instagram_link]})
        data.to_csv(path,index=False, index_label=None)
        et=time.time()
        links_time=et-st
        print('Total execution time of socialLinkCollectorCompetitor.py is:',links_time)

        return instagram_link,facebook_link,linkedin_link,twitter_link,links_time'''

    else:
        print("No URL found or the URL is wrong:",url)

        instagram_link=None
        facebook_link=None
        linkedin_link=None
        twitter_link=None
        try:
            data=pd.DataFrame({'Social Platform Link':[instagram_link]})
            data.to_csv(path,index=False, index_label=None)
        except Exception as e:
            print(f'Error occurred while working with DataFrame: {e}')

        et=time.time()
        links_time=et-st
        print('Total execution time of socialLinkCollectorCompetitor.py is:',links_time)

    return instagram_link,facebook_link,linkedin_link,twitter_link,links_time

#socialLinkCollectorCompetitor('https://www.icd-ecoles.com/',1)
#socialLinkCollectorCompetitor('https://junto.fr/',1)
#socialLinkCollectorCompetitor('https://www.lescausantes.com/',1)
