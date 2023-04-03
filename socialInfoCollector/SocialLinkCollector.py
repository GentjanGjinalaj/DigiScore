import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
#from FacebookData import facebookData
#from InstagramData import instagramData
#from LinkedinData import linkedinData
#from SocialUsernameCollector import socialUsernameCollector




def socialLinkCollector(url):
    st=time.time()
    path = "C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test.csv"
    if url:

        # The URL of the webpage you want to scrape
        #url = "https://www.icd-ecoles.com/"
        #url = input('Please enter your url: ')

        response=None

        try:
            # code that might raise an exception
            response = requests.get(url)
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

        if response:
            # Parse the HTML content of the webpage using BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the first anchor tag with href attribute containing "instagram.com"
            instagram_links = soup.find_all("a", href=lambda href: href and "instagram.com" in href)
            if instagram_links:
                instagram_link = instagram_links[0]["href"]
                print("Instagram link:", instagram_link)
            else:
                print("No Instagram link found.")
                instagram_link=None

            # Find the first anchor tag with href attribute containing "facebook.com"
            facebook_links = soup.find_all("a", href=lambda href: href and "facebook.com" in href)
            if facebook_links:
                facebook_link = facebook_links[0]["href"]
                print("Facebook link:", facebook_link)
            else:
                print("No Facebook link found.")
                facebook_link=None

            # Find the first anchor tag with href attribute containing "linkedin.com"
            linkedin_links = soup.find_all("a", href=lambda href: href and "linkedin.com" in href)
            if linkedin_links:
                linkedin_link = linkedin_links[0]["href"]
                print("LinkedIn link:", linkedin_link)
            else:
                print("No LinkedIn link found.")
                linkedin_link=None

            # Find the first anchor tag with href attribute containing "twitter.com"
            twitter_links = soup.find_all("a", href=lambda href: href and "twitter.com" in href)
            if twitter_links:
                twitter_link = twitter_links[0]["href"]
                print("Twitter link:", twitter_link)
            else:
                print("No Twitter link found.")
                twitter_link=None

            # Find all anchor tags with href attribute containing "instagram.com", "facebook.com", or "linkedin.com"
            mixed_links = [a["href"] for a in soup.find_all("a", href=lambda href: href and ("instagram.com" in href or "facebook.com" in href or "linkedin.com" in href or "twitter.com in href"))]

            # Print the links
            print("Mixed links:", mixed_links)
        else:
            print(f"No URL found or the URL is wrong: {url}")

        data=pd.DataFrame({'Social Platform Link':[instagram_link]})
        data.to_csv(path,index=False, index_label=None)

        et=time.time()
        links_time=et-st
        return instagram_link,facebook_link,linkedin_link,twitter_link,links_time

    else:
        print("No URL found or the URL is wrong:",url)

        et=time.time()
        links_time=et-st
        print('Total execution time of SocialLinkCollector.py is:',links_time)
        instagram_link=None
        facebook_link=None
        linkedin_link=None
        twitter_link=None

    return instagram_link,facebook_link,linkedin_link,twitter_link,links_time


