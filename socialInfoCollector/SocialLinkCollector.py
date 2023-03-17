import requests
from bs4 import BeautifulSoup





def socialPlatformsUrl(url):
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

        # Find the first anchor tag with href attribute containing "facebook.com"
        facebook_links = soup.find_all("a", href=lambda href: href and "facebook.com" in href)
        if facebook_links:
            facebook_link = facebook_links[0]["href"]
            print("Facebook link:", facebook_link)
        else:
            print("No Facebook link found.")

        # Find the first anchor tag with href attribute containing "linkedin.com"
        linkedin_links = soup.find_all("a", href=lambda href: href and "linkedin.com" in href)
        if linkedin_links:
            linkedin_link = linkedin_links[0]["href"]
            print("LinkedIn link:", linkedin_link)
        else:
            print("No LinkedIn link found.")

        # Find all anchor tags with href attribute containing "instagram.com", "facebook.com", or "linkedin.com"
        mixed_links = [a["href"] for a in soup.find_all("a", href=lambda href: href and ("instagram.com" in href or "facebook.com" in href or "linkedin.com" in href))]

        # Print the links
        print("Mixed links:", mixed_links)
    else:
        print(f"No URL found or the URL is wrong: {url}")

    return instagram_link, facebook_link,linkedin_link

#socialPlatformsUrl('https://www.icd-ecoles.com/')