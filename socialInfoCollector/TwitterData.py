import snscrape.modules.twitter as sntwitter
import pandas as pd
import time
from datetime import datetime, timedelta

def twitterData(twitter_link,twitter_username):
    st=time.time()
    return 0
    print('Started executing TwitterData.py')
    #path = "DigiScore\\test.csv"
    path = "test.csv"
    if twitter_link:
        now=datetime.today()
        now_withot_hour=now.strftime(f"%Y-%m-%d")
        d = datetime.today() - timedelta(days=90)
        date_without_hour = d.strftime(f"%Y-%m-%d")

        try:
            # set the Twitter account handle
            twitter_handle = twitter_username

            # get the user object for the Twitter account
            user_query = f"from:{twitter_handle}"
            user_results = list(sntwitter.TwitterSearchScraper(user_query + f" since:{date_without_hour} until:{now_withot_hour}").get_items())
            print(user_results)
        except Exception as e:
             print("Snscrape is not working:", e)
             user_results=[]

        if not user_results==[] and user_results:

            user = user_results[0].user
            print(user)

            # get the number of followers and following
            followers_count = user.followersCount
            following_count = user.friendsCount

            # get the last 5 posts for the Twitter account
            posts_query = f"from:{twitter_handle}"
            posts_results = list(sntwitter.TwitterSearchScraper(posts_query + " since:2023-02-01 until:2023-03-30").get_items())
            posts_results = posts_results[:5]

            # loop through the posts and get the number of likes and comments
            post_data = []
            likess=[]
            commentss=[]
            retweetss=[]
            i=1
            for post in posts_results:
                likes_count = post.likeCount
                likess.append(likes_count)
                comments_count = post.replyCount
                commentss.append(comments_count)
                retweets = post.retweetCount
                retweetss.append(retweets)
                post_data.append({f"Post {i} Likes": likes_count, f"Post {i} Comments": comments_count,f'Post {i} Retweets':retweets})
                i+=1

            '''my_dict=dict()
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

            print(my_dict)'''


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

            try:
                filtered_comments = [x for x in commentss if x is not None]
                filtered_comments = [x for x in commentss if x!=""]

                # Calculate the average
                if filtered_comments:
                    average_comments = sum(filtered_comments) / len(filtered_comments)
                else:
                    average_comments = None

                print(average_comments)
            except:
                print("An error occured while calculating the average comments")
                average_comments = None
            try:
                filtered_retweets = [x for x in retweetss if x is not None]
                filtered_retweets = [x for x in retweetss if x!=""]

                # Calculate the average
                if filtered_retweets:
                    average_retweets = sum(filtered_retweets) / len(filtered_retweets)
                else:
                    average_retweets = None

                print(average_retweets)
            except:
                print("An error occured while calculating the average comments")
                average_retweets = None

            # Create a new row to append to the DataFrame
            new_row = {
                    'Social Platform Name':'Twitter',
                    'Social Platform Link':twitter_link,
                    'Social Platform Username':twitter_username,
                    'Followers Count': followers_count,
                    #'Following Count': following_count,
                    'Average Likes per 5 posts': average_likes,
                    'Average Comments per 5 posts': average_comments,
                    #'Avarage Retweets per 5 posts':average_retweets
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

            # print the number of followers, following, and the post data
            print(f"Followers: {followers_count}")
            print(f"Following: {following_count}")
        else:
            print("Could not get the data from the twitter account")
                # Create a new row to append to the DataFrame
            new_row = {
                            'Social Platform Name':'Twitter',
                            'Social Platform Link':None,
                            'Social Platform Username':None,
                            'Followers Count': None,
                            #'Following Count': None,
                            'Average Likes per 5 posts': None,
                            'Average Comments per 5 posts': None,
                            #'Avarage Retweets per 5 posts':None
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
        print("There is no twitter account associated at this webpage")

            # Create a new row to append to the DataFrame
        new_row = {
                        'Social Platform Name':'Twitter',
                        'Social Platform Link':None,
                        'Social Platform Username':None,
                        'Followers Count': None,
                        #'Following Count': None,
                        'Average Likes per 5 posts': None,
                        'Average Comments per 5 posts': None,
                        #'Avarage Retweets per 5 posts':None
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
    print('Total execution time of TwitterData.py is:',twitter_time,'seconds')

    return twitter_time

#twitterData('https://www.axa.com/','elonmusk')



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################




def twitterDataCompetitor(twitter_link,twitter_username,competitor_num):
    st=time.time()
    return 0
    print('Started executing TwitterDataCompetitor.py')
    #path = f"DigiScore\\DataML\\Competitors\\socialCompetitor_{competitor_num}.csv"
    path = f"DataML\\Competitors\\socialCompetitor_{competitor_num}.csv"
    if twitter_link:
        now=datetime.today()
        now_withot_hour=now.strftime(f"%Y-%m-%d")
        d = datetime.today() - timedelta(days=90)
        date_without_hour = d.strftime(f"%Y-%m-%d")

        try:
            # set the Twitter account handle
            twitter_handle = twitter_username

            # get the user object for the Twitter account
            user_query = f"from:{twitter_handle}"
            user_results = list(sntwitter.TwitterSearchScraper(user_query + f" since:{date_without_hour} until:{now_withot_hour}").get_items())
            print(user_results)
        except Exception as e:
             print("Snscrape is not working:", e)
             user_results=[]

        if not user_results==[] and user_results:

            user = user_results[0].user
            print(user)

            # get the number of followers and following
            followers_count = user.followersCount
            following_count = user.friendsCount

            # get the last 5 posts for the Twitter account
            posts_query = f"from:{twitter_handle}"
            posts_results = list(sntwitter.TwitterSearchScraper(posts_query + " since:2023-02-01 until:2023-03-30").get_items())
            posts_results = posts_results[:5]

            # loop through the posts and get the number of likes and comments
            post_data = []
            likess=[]
            commentss=[]
            retweetss=[]
            i=1
            for post in posts_results:
                likes_count = post.likeCount
                likess.append(likes_count)
                comments_count = post.replyCount
                commentss.append(comments_count)
                retweets = post.retweetCount
                retweetss.append(retweets)
                post_data.append({f"Post {i} Likes": likes_count, f"Post {i} Comments": comments_count,f'Post {i} Retweets':retweets})
                i+=1

            '''my_dict=dict()
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

            print(my_dict)'''


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

            try:
                filtered_comments = [x for x in commentss if x is not None]
                filtered_comments = [x for x in commentss if x!=""]

                # Calculate the average
                if filtered_comments:
                    average_comments = sum(filtered_comments) / len(filtered_comments)
                else:
                    average_comments = None

                print(average_comments)
            except:
                print("An error occured while calculating the average comments")
                average_comments = None
            try:
                filtered_retweets = [x for x in retweetss if x is not None]
                filtered_retweets = [x for x in retweetss if x!=""]

                # Calculate the average
                if filtered_retweets:
                    average_retweets = sum(filtered_retweets) / len(filtered_retweets)
                else:
                    average_retweets = None

                print(average_retweets)
            except:
                print("An error occured while calculating the average comments")
                average_retweets = None

            # Create a new row to append to the DataFrame
            new_row = {
                    'Social Platform Name':'Twitter',
                    'Social Platform Link':twitter_link,
                    'Social Platform Username':twitter_username,
                    'Followers Count': followers_count,
                    #'Following Count': following_count,
                    'Average Likes per 5 posts': average_likes,
                    'Average Comments per 5 posts': average_comments,
                    #'Avarage Retweets per 5 posts':average_retweets
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

            # print the number of followers, following, and the post data
            print(f"Followers: {followers_count}")
            print(f"Following: {following_count}")
        else:
            print("Could not get the data from the twitter account")
                # Create a new row to append to the DataFrame
            new_row = {
                            'Social Platform Name':'Twitter',
                            'Social Platform Link':None,
                            'Social Platform Username':None,
                            'Followers Count': None,
                            #'Following Count': None,
                            'Average Likes per 5 posts': None,
                            'Average Comments per 5 posts': None,
                            #'Avarage Retweets per 5 posts':None
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
        print("There is no twitter account associated at this webpage")

            # Create a new row to append to the DataFrame
        new_row = {
                        'Social Platform Name':'Twitter',
                        'Social Platform Link':None,
                        'Social Platform Username':None,
                        'Followers Count': None,
                        #'Following Count': None,
                        'Average Likes per 5 posts': None,
                        'Average Comments per 5 posts': None,
                        #'Avarage Retweets per 5 posts':None
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
    print('Total execution time of TwitterDataCompetitor.py is:',twitter_time,'seconds')

    return twitter_time

#twitterDataCompetitor('https://www.axa.com/','elonmusk',1)


'''from twitter_scraper import Profile, get_tweets

def get_user_profile_info(username):
    profile = Profile(username)
    return {"followers": profile.followers_count, "following": profile.following_count}

def get_tweets_info(username, count=5):
    tweets = list(get_tweets(username, pages=1))[:count]
    return [
        {
            "likes": tweet["likes"],
            "retweets": tweet["retweets"],
            "replies": tweet["replies"],
        }
        for tweet in tweets
    ]
cd
if __name__ == "__main__":
    username = "AXA"
    profile_info = get_user_profile_info(username)
    tweet_info = get_tweets_info(username)
    print(f"Profile Info for {username}: {profile_info}")
    print(f"Tweet Info for {username}: {tweet_info}")'''


'''import twint

# Configure Twint
username = "AXA"
c = twint.Config()
c.Username = username
c.Count = 5
c.Store_object = True

# Search for tweets
twint.run.Search(c)

# Get number of followers and following
followers = twint.output.users_list[-1].followers
following = twint.output.users_list[-1].following

# Get number of likes, comments, and retweets for each tweet
for tweet in twint.output.tweets_list:
    print(f"Likes: {tweet.likes_count}")
    print(f"Comments: {tweet.replies_count}")
    print(f"Retweets: {tweet.retweets_count}")'''


'''
    profile = twitter_username
    userScraper = sntwitter.TwitterUserScraper(profile)
    userdata = userScraper._get_entity()

    print(f"Scraping {profile}")

    for i, tweet in enumerate(userScraper.get_items()):
        print(f"#{i+1} of {userdata.statusesCount} on ({tweet.date.strftime('%Y-%m-%d %H:%M')}): {tweet.url}")

        print("Done!")
'''

