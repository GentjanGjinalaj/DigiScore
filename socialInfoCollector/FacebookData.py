import json
from time import sleep
import pandas as pd
import requests
#from SocialLinkCollector import facebook_link


def facebookData(facebook_link):
    path='C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\Actual\\facebook.json'
    #instagram_link, facebook_link,linkedin_link = socialPlatformsUrl(url)
    #print("My facebook link:",facebook_link)

    '''if facebook_link:
        username = 'gentjan_gjinalaj'
        apiKey = 'aWSMM1qwgr52Mm6Yyq6JPKWXH'
        scraper = 'facebookProfile'
        url = facebook_link

        apiEndPoint = "http://api.scraping-bot.io/scrape/data-scraper"
        apiEndPointResponse = "http://api.scraping-bot.io/scrape/data-scraper-response?"

        payload = json.dumps({"url": url, "scraper": scraper})
        headers = {
            'Content-Type': "application/json"
        }

        response = requests.request("POST", apiEndPoint, data=payload, auth=(username, apiKey), headers=headers)
        if response.status_code == 200:
            print(response.json())
            print(response.json()["responseId"])
            responseId = response.json()["responseId"]

            pending = True
            while pending:
                # sleep 5s between each loop, social-media scraping can take quite long to complete
                # so there is no point calling the api quickly as we will return an error if you do so
                sleep(5)
                finalResponse = requests.request("GET", apiEndPointResponse + "scraper=" + scraper + "&responseId=" + responseId, auth=(username, apiKey))
                result = finalResponse.json()
                if type(result) is list:
                    pending = False
                    print(finalResponse.text)
                    # Write result to JSON file using Pandas
                    result_df = pd.DataFrame(result)
                    result_df.to_json(path)
                elif type(result) is dict:
                    if "status" in result and result["status"] == "pending":
                        print(result["message"])
                        continue
                    elif result["error"] is not None:
                        pending = False
                        print(json.dumps(result, indent=4))

        else:
            print(response.text)'''


    if facebook_link:
        try:
            df = pd.read_json(path)
        except Exception as e:
            print("An error occured while reading the json: ",e)

        try:
            fb_followers = df['profile_followers'][0]
        except Exception as e:
            print("An error occured while geting the data for Facebook Page Followers: ",e)
            fb_followers = None
        try:
            fb_likes = df['profile_likes'][0]
        except Exception as e:
            print("An error occured while geting the data for Facebook Page Likes : ",e)
            fb_likes = None

        try:
            post1 = df['post_info'][0][0]['likes']
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 1 : ",e)
            post1 = None

        try:
            post2 = df['post_info'][0][1]['likes']
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 2 : ",e)
            post2 = None

        try:
            post3 = df['post_info'][0][2]['likes']
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 3 : ",e)
            post3 = None

        try:
            post4 = df['post_info'][0][3]['likes']
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 4 : ",e)
            post4 = None

        try:
            post5 = df['post_info'][0][4]['likes']
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 5: ",e)
            post5 = None

        print(fb_followers)
        print(fb_likes)
        print(post1)
        print(post2)
        print(post3)
        print(post4)
        print(post5)

        path1 = "C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test.csv"

        # Create a new row to append to the DataFrame
        new_row = {
                    'Post 1 Likes': post1,
                    #'Post 1 Comments': post1Comments,
                    'Post 2 Likes': post2,
                    #'Post 2 Comments': post2Comments,
                    'Post 3 Likes': post3,
                    #'Post 3 Comments': post3Comments,
                    'Post 4 Likes': post4,
                    #'Post 4 Comments': post4Comments,
                    'Post 5 Likes': post5,
                    #'Post 5 Comments': post5Comments,
                    'Followers Count': fb_followers,
                    'Page Like Count':fb_likes
                }


        try:
            df1 = pd.read_csv(path1)
        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df1 = None
        # Convert the dictionary to a DataFrame
        new_row_df = pd.DataFrame([new_row])
        # Append the new row of data to the existing DataFrame
        df1 = pd.concat([df1,new_row_df], ignore_index=True)
        # df1.loc[len(df1)] = new_row

        # Write the updated DataFrame to the CSV file
        df1.to_csv(path1, index=False)
        print(df1)

    else:
        print("There is no facebook link on their webpage")


#facebookData('cvsdv')