import os
import asyncio
from flask import Flask,request,render_template,send_file
from socialInfoCollector import SocialLinkCollector,SocialUsernameCollector,InstagramData,LinkedinData,FacebookData,TwitterData
from DataML import SimiWebData, GetDataFromPics


app = Flask(__name__)

async def collect_social_links(username):
    instagram_link, facebook_link, linkedin_link, twitter_link, links_time = SocialLinkCollector.socialLinkCollector(username)
    return instagram_link, facebook_link, linkedin_link, twitter_link, links_time

async def collect_social_usernames(instagram_link, facebook_link, linkedin_link, twitter_link):
    instagram_username, facebook_username, linkedin_username, twitter_username, username_time = SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link,facebook_link=facebook_link,linkedin_link=linkedin_link,twitter_link=twitter_link)
    return instagram_username, facebook_username, linkedin_username, twitter_username, username_time

async def get_simiweb_data(user_input):
    return SimiWebData.simiWebData(user_input)

async def get_instagram_data(instagram_username):
    return InstagramData.instagramData(instagram_username=instagram_username)

async def get_twitter_data(twitter_link, twitter_username):
    return TwitterData.twitterData(twitter_link=twitter_link,twitter_username=twitter_username)

async def get_linkedin_data(linkedin_link, linkedin_username):
    return LinkedinData.linkedinData(linkedin_link=linkedin_link,linkedin_username=linkedin_username)

async def get_facebook_data(facebook_link, facebook_username):
    return FacebookData.facebookData(facebook_link=facebook_link,facebook_username=facebook_username)


@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        social_links_task = asyncio.create_task(collect_social_links(user_input))
        instagram_link, facebook_link, linkedin_link, twitter_link, links_time = await social_links_task

        social_usernames_task = asyncio.create_task(collect_social_usernames(instagram_link, facebook_link, linkedin_link, twitter_link))
        instagram_username, facebook_username, linkedin_username, twitter_username, username_time = await social_usernames_task

        simiweb_task = asyncio.create_task(get_simiweb_data(user_input))
        instagram_task = asyncio.create_task(get_instagram_data(instagram_username))
        twitter_task = asyncio.create_task(get_twitter_data(twitter_link, twitter_username))
        linkedin_task = asyncio.create_task(get_linkedin_data(linkedin_link, linkedin_username))
        facebook_task = asyncio.create_task(get_facebook_data(facebook_link, facebook_username))


        await asyncio.gather(simiweb_task, instagram_task, twitter_task, linkedin_task, facebook_task)

        getDataFromPics_time = GetDataFromPics.getDataFromPics()

        result = simiweb_task.result() + instagram_task.result() + twitter_task.result() + linkedin_task.result() + facebook_task.result() + links_time + username_time + getDataFromPics_time
        print('Total execution time:', result, 'seconds')

        return render_template("result.html", result=result)
    else:
        # If the request method is GET, return the HTML form
        return render_template("index.html")


@app.route('/download_csv')
def download_csv():
    filename = "test.csv"
    path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True,port=5000)

'''import os
from flask import Flask,request,render_template,send_file
from socialInfoCollector import SocialLinkCollector,SocialUsernameCollector,InstagramData,LinkedinData,FacebookData,TwitterData
from DataML import SimiWebData


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        instagram_link,facebook_link,linkedin_link,twitter_link,links_time = SocialLinkCollector.socialLinkCollector(user_input)
        instagram_username,facebook_username,linkedin_username,twitter_username,username_time=SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link,facebook_link=facebook_link,linkedin_link=linkedin_link,twitter_link=twitter_link)
        instagram_time=InstagramData.instagramData(instagram_username=instagram_username)
        twitter_time=TwitterData.twitterData(twitter_link=twitter_link,twitter_username=twitter_username)
        linkedin_time=LinkedinData.linkedinData(linkedin_link=linkedin_link,linkedin_username=linkedin_username)
        facebook_time=FacebookData.facebookData(facebook_link=facebook_link,facebook_username=facebook_username)
        simiWebData_time=SimiWebData.simiWebData(user_input)
        result=instagram_time+linkedin_time+facebook_time+twitter_time+links_time+username_time+simiWebData_time
        print('Total execution time:',result,'seconds')

        return render_template("result.html",result=result)
    else:
        # If the request method is GET, return the HTML form
        return render_template("index.html")


@app.route('/download_csv')
def download_csv():
    filename = "test.csv"
    path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True,port=5000)


'''
