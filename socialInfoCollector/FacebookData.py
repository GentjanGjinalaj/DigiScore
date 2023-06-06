#https://www.scraping-bot.io/
import json
from time import sleep
import pandas as pd
import requests
import time


def facebookData(facebook_link,facebook_username):
    st=time.time()
    print('Started executing FacebookData.py')
    path1 ='DigiScore\\socialInfoCollector\\facebook.json'
    path = "DigiScore\\test.csv"


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
                    result_df.to_json(path1)
                elif type(result) is dict:
                    if "status" in result and result["status"] == "pending":
                        print(result["message"])
                        continue
                    elif result["error"] is not None:
                        pending = False
                        print(json.dumps(result, indent=4))

        else:
            print(response.text)'''

    likess=[]
    comments=[]
    if facebook_link:
        try:
            df = pd.read_json(path1)
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
            likess.append(post1)
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 1 : ",e)
            post1 = None
            likess.append(post1)

        try:
            post2 = df['post_info'][0][1]['likes']
            likess.append(post2)
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 2 : ",e)
            post2 = None
            likess.append(post2)

        try:
            post3 = df['post_info'][0][2]['likes']
            likess.append(post3)
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 3 : ",e)
            post3 = None
            likess.append(post3)

        try:
            post4 = df['post_info'][0][3]['likes']
            likess.append(post4)
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 4 : ",e)
            post4 = None
            likess.append(post4)

        try:
            post5 = df['post_info'][0][4]['likes']
            likess.append(post5)
        except Exception as e:
            print("An error occured while geting the data for Facebook Post 5: ",e)
            post5 = None
            likess.append(post5)

        try:
            filtered_likes = [x for x in likess if x is not None]
            filtered_likes = [x for x in likess if x!=""]

            # Calculate the average
            if filtered_likes:
                average_likes = sum(filtered_likes) / len(filtered_likes)
            else:
                average_likes = None

            print(average_likes)
        except:
            print("An error occured while calculating the average likes")
            average_likes = None


        print(fb_followers)
        print(fb_likes)
        print(post1)
        print(post2)
        print(post3)
        print(post4)
        print(post5)
        print(likess)
        print(comments)
        print('Avarage Fb Likes:',average_likes)

        # Create a new row to append to the DataFrame
        new_row = {
                    'Social Platform Name':'Facebook',
                    'Social Platform Link':facebook_link,
                    'Social Platform Username':facebook_username,
                    'Followers Count': fb_followers,
                    #'Page Like Count':fb_likes,
                    'Average Likes per 5 posts':average_likes,
                    'Average Comments per 5 posts':0
                }


        try:
            df1 = pd.read_csv(path)
            # Convert the dictionary to a DataFrame
            new_row_df = pd.DataFrame([new_row])
            # Append the new row of data to the existing DataFrame
            df1 = pd.concat([df1,new_row_df], ignore_index=True)
            # df1.loc[len(df1)] = new_row

            # Write the updated DataFrame to the CSV file
            df1.to_csv(path, index=False)
            print(df1)
        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df1 = None
            et=time.time()
            print('Total execution time of FacebookData.py is:',et-st,'seconds')

    else:
        print("There is no facebook link on their webpage")

        # Create a new row to append to the DataFrame
        new_row = {
                    'Social Platform Name':'Facebook',
                    'Social Platform Link':None,
                    'Social Platform Username':None,
                    'Average Likes per 5 posts':None,
                    'Followers Count': None,
                    'Average Comments per 5 posts':None
                    #'Page Like Count':None
                }
        try:
            df1 = pd.read_csv(path)
            # Convert the dictionary to a DataFrame
            new_row_df = pd.DataFrame([new_row])
            # Append the new row of data to the existing DataFrame
            df1 = pd.concat([df1,new_row_df], ignore_index=True)
            # df1.loc[len(df1)] = new_row

            # Write the updated DataFrame to the CSV file
            df1.to_csv(path, index=False)
            print(df1)
        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df1 = None

    et=time.time()
    facebook_time=et-st
    print('Total execution time of FacebookData.py is:',facebook_time,'seconds')

    return facebook_time


#facebookData('cvsdv','qewfw')