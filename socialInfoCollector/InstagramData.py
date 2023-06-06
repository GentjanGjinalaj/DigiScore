import configparser
import time
import instaloader
import pandas as pd
import itertools


def instagramData(instagram_username):
    st=time.time()
    #return 0
    print('Started executing InstagramData.py')
    path = "DigiScore\\test.csv"
    if instagram_username:
        # Load the configuration file
        config = configparser.ConfigParser()
        config.read('DigiScore\\socialInfoCollector\\config.ini')

        # Get the username and password from the config file
        username = config.get('instagram', 'username')
        password = config.get('instagram', 'password')

        # Creating an instance of the Instaloader class
        bot = instaloader.Instaloader()
        #outlook email = datadigitest@hotmail.com
        #outlook password = Digitalized1243
        #Instagram username=data_digi_test
        #Instagram password=Digitalized1243

        try:# Log in to Instagram# Log in with your new credentials
            bot.login(username, password)
            # Save the session to a file
            bot.save_session_to_file(username)
        except Exception as e:
            print(e)



        # Save the session to a file
        #bot.save_session_to_file(username)

        bot.context.log("Logging in...")
        #bot.load_session_from_file(username)
        if not bot.context.is_logged_in:
            bot.context.log("Login failed.")
        else:
            bot.context.log("Login successful.")

        try:
            profile = instaloader.Profile.from_username(bot.context, instagram_username)
        except instaloader.exceptions.ProfileNotExistsException:
            print('The profile does not exist.')
        else:
            print("Username: ", profile.username)
            print("User ID: ", profile.userid)
            print("Number of Posts: ", profile.mediacount)
            print("Followers Count: ", profile.followers)
            ###print("Following Count: ", profile.followees)
            print("Bio: ", profile.biography)
            print("External URL: ", profile.external_url)

            # L.load_session_from_file(username) # load session if previously saved


            # Get the posts of the user
            posts = itertools.islice(profile.get_posts(),5)
            likess=[]
            commentss=[]
            # Iterate over the last 5 posts and collect the likes and comments count
            for post in posts:

            # Get the number of likes and comments
                likes = post.likes
                comments = post.comments

                # Print the number of likes and comments
                print(f"Post {post.shortcode} has {likes} likes and {comments} comments")
                likess.append(likes)
                commentss.append(comments)


            try:
                df = pd.read_csv(path)
                df['Social Platform Name']='Instagram'
            except Exception as e:
                print("An error occurred while reading the CSV file: ", e)
                df = None
            try:
                df["Followers Count"] = profile.followers
            except Exception as e:
                print("An error occured while geting the data for Instagram Followers Count: ",e)
                df['Followers Count']=None



            '''try:
                df['Following Count']=profile.followees
            except Exception as e:
                print("An error occured while geting the data for Instagram Following Count: ",e)
                df['Following Count']=None
            try:
                df['Post 1 Likes']=likess[0]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 1 Likes: ",e)
                df['Post 1 Likes']=None
            try:
                df['Post 1 Comments']=commentss[0]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 1 Comments: ",e)
                df['Post 1 Comments']=None
            try:
                df['Post 2 Likes']=likess[1]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 2 Likes: ",e)
                df['Post 2 Likes']=None
            try:
                df['Post 2 Comments']=commentss[1]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 2 Comments: ",e)
                df['Post 2 Comments']=None
            try:
                df['Post 3 Likes']=likess[2]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 3 Likes: ",e)
                df['Post 3 Likes']=None
            try:
                df['Post 3 Comments']=commentss[2]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 3 Comments: ",e)
                df['Post 3 Comments']=None
            try:
                df['Post 4 Likes']=likess[3]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 4 Likes: ",e)
                df['Post 4 Likes']=None
            try:
                df['Post 4 Comments']=commentss[3]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 4 Comments: ",e)
                df['Post 4 Comments']=None
            try:
                df['Post 5 Likes']=likess[4]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 5 Likes: ",e)
                df['Post 5 Likes']=None
            try:
                df['Post 5 Comments']=commentss[4]
            except Exception as e:
                print("An error occured while geting the data for Instagram Post 5 Comments: ",e)
                df['Post 5 Comments']=None'''
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
                df['Average Likes per 5 posts']=average_likes
            except:
                df['Average Likes per 5 posts']=None
            try:
                df['Average Comments per 5 posts']=average_comments
            except:
                df['Average Comments per 5 posts']=None

            try:
                df.to_csv(path, index=False,index_label=None)
            except:
                print("An error occured while writing the data to the csv file")

            print(df)
            print(likess)
            print(commentss)

    else:
        print("No Instagram Username")

        try:
            df = pd.read_csv(path)
            df['Social Platform Name']='Instagram'
            df['Followers Count']=None
            #df['Following Count']=None
            df['Average Likes per 5 posts']=None
            df['Average Comments per 5 posts']=None

            df.to_csv(path, index=False,index_label=None)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None

    et=time.time()
    instagram_time=et-st
    print('Total execution time of InstagramData.py is:',instagram_time,'seconds')

    return instagram_time

#instagramData('ermal_beluli')