import requests
import json
from time import sleep
#from FacebookData import facebookData


#from SocialLinkCollector import linkedin_link


def linkedinData(linkedin_link):
    path='C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\Actual\\linkedinData.json'
    #instagram_link, facebook_link,linkedin_link = socialPlatformsUrl(url)
    #print("my linkedin link:",linkedin_link)
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
                    import pandas as pd
                    pending = False
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

    if linkedin_link:
        print('spvdfnviwfvnsdvbsuefcsbwgeidsjkl')
        import pandas as pd
        #path1='C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\Actual\\linkedinData.json'

        try:
            df = pd.read_json(path)
        except Exception as e:
            print("An error occured while reading the data",e)

        try:
            linkedinFollowers = df['followers'][0]
        except Exception as e:
            print("An error occured while geting the data for Linkedin page Followers: ",e)
            linkedinFollowers = None

        try:
            post1Likes = df['updates'][0][0]['likes_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 1 Likes: ",e)
            post1Likes = None
        try:
            post1Comments = df['updates'][0][0]['comments_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 1 Comments: ",e)
            post1Comments = None

        try:
            post2Comments = df['updates'][0][1]['comments_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 2 Comments: ",e)
            post2Comments = None
        try:
            post2Likes = df['updates'][0][1]['likes_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 2 Likes: ",e)
            post2Likes = None

        try:
            post3Likes = df['updates'][0][2]['likes_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 3 Likes: ",e)
            post3Likes = None
        try:
            post3Comments = df['updates'][0][2]['comments_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 3 Comments: ",e)
            post3Comments = None

        try:
            post4Likes = df['updates'][0][3]['likes_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 4 Likes: ",e)
            post4Likes = None
        try:
            post4Comments = df['updates'][0][3]['comments_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 4 Comments: ",e)
            post4Comments = None

        try:
            post5Likes = df['updates'][0][4]['likes_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 5 Likes: ",e)
            post5Likes = None
        try:
            post5Comments = df['updates'][0][4]['comments_count']
        except Exception as e:
            print("An error occured while geting the data for Linkedin Post 5 Comments: ",e)
            post5Comments = None

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


        path1 = "C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test.csv"

    # Create a new row to append to the DataFrame
        new_row = {
                'Post 1 Likes': post1Likes,
                'Post 1 Comments': post1Comments,
                'Post 2 Likes': post2Likes,
                'Post 2 Comments': post2Comments,
                'Post 3 Likes': post3Likes,
                'Post 3 Comments': post3Comments,
                'Post 4 Likes': post4Likes,
                'Post 4 Comments': post4Comments,
                'Post 5 Likes': post5Likes,
                'Post 5 Comments': post5Comments,
                'Followers Count': linkedinFollowers
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

#linkedinData('qwerty')