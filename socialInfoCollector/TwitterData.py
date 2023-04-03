import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
import time
from datetime import datetime, timedelta

def twitterData(twitter_link,twitter_username):
    st=time.time()
    path = "C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test.csv"
    if twitter_link:
        now=datetime.today()
        now_withot_hour=now.strftime(f"%Y-%m-%d")
        d = datetime.today() - timedelta(days=30)
        date_without_hour = d.strftime(f"%Y-%m-%d")

        # set the Twitter account handle
        twitter_handle = twitter_username

        # get the user object for the Twitter account
        user_query = f"from:{twitter_handle}"
        user_results = list(sntwitter.TwitterSearchScraper(user_query + f" since:{date_without_hour} until:{now_withot_hour}").get_items())
        user = user_results[0].user


        # get the number of followers and following
        followers_count = user.followersCount
        following_count = user.friendsCount

        # get the last 5 posts for the Twitter account
        posts_query = f"from:{twitter_handle}"
        posts_results = list(sntwitter.TwitterSearchScraper(posts_query + " since:2023-02-01 until:2023-03-30").get_items())
        posts_results = posts_results[:5]

        # loop through the posts and get the number of likes and comments
        post_data = []
        i=1
        for post in posts_results:
            likes_count = post.likeCount
            comments_count = post.replyCount
            retweets = post.retweetCount
            post_data.append({f"Post {i} Likes": likes_count, f"Post {i} Comments": comments_count,f'Post {i} Retweets':retweets})
            i+=1

        my_dict=dict()
        for index, value in enumerate(post_data):
            for k, v in value.items():
                if k.endswith("Likes") or k.endswith("Comments") or k.endswith("retweets"):
                    my_dict.setdefault(k, 0)
                    my_dict[k] += v
        my_dict['Social Platform Name']='Twitter'
        my_dict['Social Platform Link']=twitter_link
        my_dict['Social Platform Username']=twitter_username
        my_dict['Followers Count']=followers_count
        my_dict['Following Count']=following_count

        print(my_dict)

        try:
            df1 = pd.read_csv(path)
            # Convert the dictionary to a DataFrame
            new_row_df = pd.DataFrame([my_dict])
            # Append the new row of data to the existing DataFrame
            df1 = pd.concat([df1,new_row_df], ignore_index=True)
            # df1.loc[len(df1)] = new_row

            # Write the updated DataFrame to the CSV file
            df1.to_csv(path, index=False)
            print(df1)
        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df1 = None

        # print the number of followers, following, and the post data
        print(f"Followers: {followers_count}")
        print(f"Following: {following_count}")
    else:
        print("There is no twitter account associated at this webpage")

        # Create a new row to append to the DataFrame
        new_row = {
                    'Social Platform Name':'Twitter',
                    'Social Platform Link':None,
                    'Social Platform Username':None,
                    'Post 1 Likes': None,
                    'Post 1 Comments': None,
                    'Post 1 Retweets':None,
                    'Post 2 Likes': None,
                    'Post 2 Comments': None,
                    'Post 2 Retweets':None,
                    'Post 3 Likes': None,
                    'Post 3 Comments': None,
                    'Post 3 Retweets':None,
                    'Post 4 Likes': None,
                    'Post 4 Comments': None,
                    'Post 4 Retweets':None,
                    'Post 5 Likes': None,
                    'Post 5 Comments': None,
                    'Post 5 Retweets':None,
                    'Followers Count': None,
                    'Following Count': None,
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
    twitter_time=et-st
    print('Total execution time of TwitterData.py is:',twitter_time)

    return twitter_time
#twitterData('https://twitter.com/AXA')