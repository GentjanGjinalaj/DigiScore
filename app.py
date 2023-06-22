import os
import asyncio
from flask import Flask,request,render_template,send_file
from socialInfoCollector import SocialLinkCollector,SocialUsernameCollector,InstagramData,LinkedinData,FacebookData,TwitterData
from DataML import SimiWebData, GetDataFromPics, GetCompetitorsFromPics,GetKeywordsNumber,GetMarketingChannelDistribution
from semRushAPI import SemRushApi


app = Flask(__name__)

async def collect_social_links(username):
    instagram_link, facebook_link, linkedin_link, twitter_link, links_time = SocialLinkCollector.socialLinkCollector(username)
    return instagram_link, facebook_link, linkedin_link, twitter_link, links_time

async def collect_social_usernames(instagram_link, facebook_link, linkedin_link, twitter_link):
    instagram_username, facebook_username, linkedin_username, twitter_username, username_time = SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link,facebook_link=facebook_link,linkedin_link=linkedin_link,twitter_link=twitter_link)
    return instagram_username, facebook_username, linkedin_username, twitter_username, username_time

async def get_simiweb_data(user_input):
    return SimiWebData.simiWebData(user_input)

async def get_data_from_pics(user_input):
    return GetDataFromPics.getDataFromPics(user_input)

async def get_competitors_from_pics(user_input):
    return GetCompetitorsFromPics.getCompetitors(user_input)

async def get_marketing_channel_distribution(user_input):
    return GetMarketingChannelDistribution.getMarketingChannelDistribution(user_input)

async def get_keywords_number(user_input):
    return GetKeywordsNumber.getKeywordsNumber(user_input)

async def get_instagram_data(instagram_username):
    return InstagramData.instagramData(instagram_username=instagram_username)

async def get_twitter_data(twitter_link, twitter_username):
    return TwitterData.twitterData(twitter_link=twitter_link,twitter_username=twitter_username)

async def get_linkedin_data(linkedin_link, linkedin_username):
    return LinkedinData.linkedinData(linkedin_link=linkedin_link,linkedin_username=linkedin_username)

async def get_facebook_data(facebook_link, facebook_username):
    return FacebookData.facebookData(facebook_link=facebook_link,facebook_username=facebook_username)

async def get_semRush_api(user_input):
    return SemRushApi.semRush_Api(user_input)

@app.route("/", methods=["GET", "POST"])
async def index():
    try:
        if request.method == 'POST':
            user_input = request.form['user_input']
            social_links_task = asyncio.create_task(collect_social_links(user_input))
            instagram_link, facebook_link, linkedin_link, twitter_link, links_time = await social_links_task

            social_usernames_task = asyncio.create_task(collect_social_usernames(instagram_link, facebook_link, linkedin_link, twitter_link))
            instagram_username, facebook_username, linkedin_username, twitter_username, username_time = await social_usernames_task

            simiweb_task = asyncio.create_task(get_simiweb_data(user_input))
            data_from_pics_task = asyncio.create_task(get_data_from_pics(user_input))
            competitors_from_pics_task = asyncio.create_task(get_competitors_from_pics(user_input))
            channel_distrib_task = asyncio.create_task(get_marketing_channel_distribution(user_input))
            keywords_number_task = asyncio.create_task(get_keywords_number(user_input))
            instagram_task = asyncio.create_task(get_instagram_data(instagram_username))
            twitter_task = asyncio.create_task(get_twitter_data(twitter_link, twitter_username))
            linkedin_task = asyncio.create_task(get_linkedin_data(linkedin_link, linkedin_username))
            facebook_task = asyncio.create_task(get_facebook_data(facebook_link, facebook_username))
            semRush_task = asyncio.create_task(get_semRush_api(user_input))

            tasks = [simiweb_task, instagram_task, twitter_task, linkedin_task, facebook_task, data_from_pics_task, competitors_from_pics_task, channel_distrib_task, keywords_number_task,semRush_task]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    if 'session not created' in str(result) or 'driver' in str(result):
                        error_message = "Browser or driver version issue. Please check your browser or driver version. It seems the ChromeDriver needs updating... " + str(result)
                        return render_template("error.html", error_message=error_message)
                    else:
                        return render_template("error.html", error_message=str(result))

            total_time = links_time + username_time + sum(result if not isinstance(result, Exception) else 0 for result in results)
            print('Total execution time:', total_time, 'seconds')

            return render_template("result.html", result=total_time)

        else:
            # If the request method is GET, return the HTML form
            return render_template("index.html")

    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500



@app.route('/download_Social_Media_csv')
def download_csv():
    filename = "test.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    return send_file(path, as_attachment=True)

@app.route('/download_SEO_Website_csv')
def download_csv1():
    filename = "test1.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    return send_file(path, as_attachment=True)

@app.route('/download_Info_csv')
def download_csv_info():
    filename = "t_column_info.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
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
    try:
        if request.method == 'POST':
            user_input = request.form['user_input']
            instagram_link,facebook_link,linkedin_link,twitter_link,links_time = SocialLinkCollector.socialLinkCollector(user_input)
            instagram_username,facebook_username,linkedin_username,twitter_username,username_time=SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link,facebook_link=facebook_link,linkedin_link=linkedin_link,twitter_link=twitter_link)
            instagram_time=InstagramData.instagramData(instagram_username=instagram_username)
            twitter_time=TwitterData.twitterData(twitter_link=twitter_link,twitter_username=twitter_username)
            linkedin_time=LinkedinData.linkedinData(linkedin_link=linkedin_link,linkedin_username=linkedin_username)
            facebook_time=FacebookData.facebookData(facebook_link=facebook_link,facebook_username=facebook_username)
            simiWebData_time=SimiWebData.simiWebData(user_input)
            data_from_pics_time=GetDataFromPics.getDataFromPics(user_input)
            competitors_from_pics_time=GetCompetitorsFromPics.getCompetitorsFromPics(user_input)
            channel_distrib_time=GetMarketingChannelDistribution.getMarketingChannelDistribution(user_input)
            keywords_number_time=GetKeywordsNumber.getKeywordsNumber(user_input)
            semRush_time=SemRushApi.semRushApi(user_input)

            result=instagram_time+linkedin_time+facebook_time+twitter_time+links_time+username_time+simiWebData_time+data_from_pics_time+competitors_from_pics_time+channel_distrib_time+keywords_number_time+semRush_time
            print('Total execution time:',result,'seconds')

            return render_template("result.html",result=result)
        else:
            # If the request method is GET, return the HTML form
            return render_template("index.html")
    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500


@app.route('/download_csv')
def download_csv():
    filename = "test.csv"
    path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    return send_file(path, as_attachment=True)

@app.route('/download_csv1')
def download_csv1():
    filename = "test1.csv"
    path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    return send_file(path, as_attachment=True)

@app.route('/download_csv_info')
def download_csv1():
    filename = "t_column_info.csv"
    path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))

if __name__ == '__main__':
    app.run(debug=True,port=5000)


'''
