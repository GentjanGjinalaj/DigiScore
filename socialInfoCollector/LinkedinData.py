#https://www.scraping-bot.io/
import json
from time import sleep
import pandas as pd
import requests
import time


def linkedinData(linkedin_link,linkedin_username):
    st=time.time()
    print('Started executing LinkedinkData.py')
    path1='DigiScore\\socialInfoCollector\\linkedinData.json'
    path = "DigiScore\\test.csv"

    '''if linkedin_link:
        username = 'gentjan_gjinalaj'
        apiKey = 'aWSMM1qwgr52Mm6Yyq6JPKWXH'
        scraper = 'linkedinCompanyProfile'
        #url = 'https://www.linkedin.com/school/icd-internationalbusinessschool/'
        url=linkedin_link

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

    if linkedin_link:

        likess=[]
        commentss=[]
        try:
            df = pd.read_json(path1)
        except Exception as e:
            print("An error occured while reading the data",e)

        try:
            linkedinFollowers = df['followers'][0]
        except Exception as e:
            print("An error occured while geting the data for Linkedin page Followers: ",e)
            linkedinFollowers = None

        try:
            post1Likes = df['updates'][0][0]['likes_count']
            likess.append(post1Likes)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 1 Likes: ",e)
            post1Likes = None
            likess.append(post1Likes)
        try:
            post1Comments = df['updates'][0][0]['comments_count']
            commentss.append(post1Comments)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 1 Comments: ",e)
            post1Comments = None
            commentss.append(post1Comments)

        try:
            post2Comments = df['updates'][0][1]['comments_count']
            commentss.append(post2Comments)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 2 Comments: ",e)
            post2Comments = None
            commentss.append(post2Comments)
        try:
            post2Likes = df['updates'][0][1]['likes_count']
            likess.append(post2Likes)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 2 Likes: ",e)
            post2Likes = None
            likess.append(post2Likes)

        try:
            post3Likes = df['updates'][0][2]['likes_count']
            likess.append(post3Likes)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 3 Likes: ",e)
            post3Likes = None
            likess.append(post3Likes)
        try:
            post3Comments = df['updates'][0][2]['comments_count']
            commentss.append(post3Comments)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 3 Comments: ",e)
            post3Comments = None
            commentss.append(post3Comments)

        try:
            post4Likes = df['updates'][0][3]['likes_count']
            likess.append(post4Likes)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 4 Likes: ",e)
            post4Likes = None
            likess.append(post4Likes)
        try:
            post4Comments = df['updates'][0][3]['comments_count']
            commentss.append(post4Comments)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 4 Comments: ",e)
            post4Comments = None
            commentss.append(post4Comments)

        try:
            post5Likes = df['updates'][0][4]['likes_count']
            likess.append(post5Likes)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 5 Likes: ",e)
            post5Likes = None
            likess.append(post5Likes)
        try:
            post5Comments = df['updates'][0][4]['comments_count']
            commentss.append(post5Comments)
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 5 Comments: ",e)
            post5Comments = None
            commentss.append(post5Comments)

        print(linkedinFollowers)
        print(post1Likes)
        print(post1Comments)
        print(post2Likes)
        print(post2Comments)
        print(post3Likes)
        print(post3Comments)
        print(post4Likes)
        print(post4Comments)
        print(post5Likes)
        print(post5Comments)
        print(likess)
        print(commentss)


        try:
            filtered_likes = [x for x in likess if x is not None]

            # Calculate the average
            if filtered_likes:
                average_likes = sum(filtered_likes) / len(filtered_likes)
            else:
                average_likes = None

            print(average_likes)
        except:
            print("An error occured while calculating the average likes")
            average_likes = None

        try:
            filtered_comments = [x for x in commentss if x is not None]

            # Calculate the average
            if filtered_comments:
                average_comments = sum(filtered_comments) / len(filtered_comments)
            else:
                average_comments = None

            print(average_comments)
        except:
            print("An error occured while calculating the average comments")
            average_comments = None


    # Create a new row to append to the DataFrame
        new_row = {
                'Social Platform Name':'Linkedin',
                'Social Platform Link':linkedin_link,
                'Social Platform Username':linkedin_username,
                'Followers Count': linkedinFollowers,
                'Average Likes per 5 posts': average_likes,
                'Average Comments per 5 posts': average_comments
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
        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df1 = None


    else:

        # Create a new row to append to the DataFrame
        new_row = {
                    'Social Platform Name':'Linkedin',
                    'Social Platform Link':None,
                    'Social Platform Username':None,
                    'Average Likes per 5 posts': None,
                    'Average Comments per 5 posts': None,
                    'Followers Count': None
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
        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df1 = None
    et=time.time()
    linkedin_time=et-st
    print('Total execution time of LinkedinData.py is:',linkedin_time,'seconds')

    return linkedin_time

#linkedinData('qwerty','revcrvinorevnoer')