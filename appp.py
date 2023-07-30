import os
import urllib.parse
from flask import Flask,request,render_template,send_file
from socialInfoCollector import SocialLinkCollector,SocialUsernameCollector,InstagramData,LinkedinData,FacebookData,TwitterData
from DataML import SimiWebData, GetDataFromPics, GetCompetitorsFromPics,GetKeywordsNumber,GetMarketingChannelDistribution
from semRushAPI import SemRushApi

appp = Flask(__name__)

def collect_data_for_competitor(competitorURL, competitor_num):
    instagram_link, facebook_link, linkedin_link, twitter_link, links_time = SocialLinkCollector.socialLinkCollectorCompetitor(competitorURL, competitor_num)
    instagram_username, facebook_username, linkedin_username, twitter_username, username_time = SocialUsernameCollector.socialUsernameCollectorCompetitor(instagram_link=instagram_link, facebook_link=facebook_link, linkedin_link=linkedin_link, twitter_link=twitter_link,competitor_num=competitor_num)

    instagram_data = InstagramData.instagramDataCompetitor(instagram_username=instagram_username,competitor_num=competitor_num)
    twitter_data = TwitterData.twitterDataCompetitor(twitter_link=twitter_link, twitter_username=twitter_username,competitor_num=competitor_num)
    linkedin_data = LinkedinData.linkedinDataCompetitor(linkedin_link=linkedin_link, linkedin_username=linkedin_username,competitor_num=competitor_num)
    facebook_data = FacebookData.facebookDataCompetitor(facebook_link=facebook_link, facebook_username=facebook_username,competitor_num=competitor_num)

    social_data_times_Competitor = sum([instagram_data, twitter_data, linkedin_data, facebook_data, links_time, username_time])

    simiweb_data = SimiWebData.simiWebDataCompetitor(competitorURL, competitor_num)
    data_from_pics_data = GetDataFromPics.getDataFromPicsCompetitor(competitorURL, competitor_num)
    keywords_number_data = GetKeywordsNumber.getKeywordsNumberCompetitor(competitorURL, competitor_num)
    channel_distrib_data = GetMarketingChannelDistribution.getMarketingChannelDistributionCompetitor(competitorURL, competitor_num)
    semRush_data = SemRushApi.semRushApiCompetitor(competitorURL, competitor_num)

    seo_times = sum([simiweb_data, data_from_pics_data, keywords_number_data, channel_distrib_data, semRush_data])

    total_time = seo_times + social_data_times_Competitor
    return total_time


@appp.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == 'POST':
            user_input = request.form['user_input']
            url = urllib.parse.urlparse(user_input)
            if not (url.scheme == 'http' or url.scheme == 'https'):
                raise ValueError("Invalid URL. Please ensure your URL starts with 'http' or 'https'.")

            instagram_link, facebook_link, linkedin_link, twitter_link, links_time = SocialLinkCollector.socialLinkCollector(user_input)
            instagram_username, facebook_username, linkedin_username, twitter_username, username_time = SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link, facebook_link=facebook_link, linkedin_link=linkedin_link, twitter_link=twitter_link)

            simiweb_data = SimiWebData.simiWebData(user_input)
            data_from_pics_data = GetDataFromPics.getDataFromPics(user_input)
            competitors_from_pics_data = GetCompetitorsFromPics.getCompetitors(user_input)
            getCompetitorsFromPics_time, competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5 = competitors_from_pics_data

            tasks = [
                simiweb_data,
                InstagramData.instagramData(instagram_username=instagram_username),
                TwitterData.twitterData(twitter_link=twitter_link, twitter_username=twitter_username),
                LinkedinData.linkedinData(linkedin_link=linkedin_link, linkedin_username=linkedin_username),
                FacebookData.facebookData(facebook_link=facebook_link, facebook_username=facebook_username),
                data_from_pics_data,
                GetMarketingChannelDistribution.getMarketingChannelDistribution(user_input),
                GetKeywordsNumber.getKeywordsNumber(user_input),
                SemRushApi.semRushApi(user_input)
            ]
            results = [task if not isinstance(task, Exception) else 0 for task in tasks]

            for result in results:
                if isinstance(result, Exception):
                    if 'session not created' in str(result) or 'driver' in str(result):
                        error_message = "Browser or driver version issue. Please check your browser or driver version. It seems the ChromeDriver needs updating... " + str(result)
                        return render_template("error.html", error_message=error_message)
                    else:
                        return render_template("error.html", error_message=str(result))

            total_time = links_time + username_time + getCompetitorsFromPics_time + sum(results)
            print('Total execution time for the main Company:', total_time, 'seconds')

            competitors = ["https://www." + comp for comp in [competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5] if comp is not None]

            competitor_total_times = []
            for i, competitor in enumerate(competitors, start=1):
                if competitor is not None:
                    print('Inside for loop before calling competitor function:', competitor)
                    print(i)
                    competitor_total_time = collect_data_for_competitor(competitor, i)  # passing the competitor number
                    competitor_total_times.append(competitor_total_time)
                    print(f"competitorNo{i}_total_time: {competitor_total_time}")

            total_time += sum(competitor_total_times)
            print('Total execution time:', total_time, 'seconds')

            return render_template("result.html", result=total_time)

        else:
            # If the request method is GET, return the HTML form
            return render_template("index.html")

    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500



@appp.route('/download_Social_Media_csv')
def download_csv():
    filename = "test.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    return send_file(path, as_attachment=True)

@appp.route('/download_SEO_Website_csv')
def download_csv1():
    filename = "test1.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    return send_file(path, as_attachment=True)

@appp.route('/download_Info_csv')
def download_csv_info():
    filename = "t_column_info.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    appp.run(debug=True,port=5000)