import os
import zipfile
import urllib.parse
from flask import Flask,request,render_template,send_file
from socialInfoCollector import SocialLinkCollector,SocialUsernameCollector,InstagramData,LinkedinData,FacebookData,TwitterData
from DataML import SimiWebData, GetDataFromPics, GetCompetitorsFromPics,GetKeywordsNumber,GetMarketingChannelDistribution
from semRushAPI import SemRushApi
from RatingSystem import final


appp = Flask(__name__)

# Global flag for termination
terminate_flag = False

def collect_data_for_competitor(competitorURL, competitor_num):
    instagram_link, facebook_link, linkedin_link, twitter_link, links_time = SocialLinkCollector.socialLinkCollectorCompetitor(competitorURL, competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    instagram_username, facebook_username, linkedin_username, twitter_username, username_time = SocialUsernameCollector.socialUsernameCollectorCompetitor(instagram_link=instagram_link, facebook_link=facebook_link, linkedin_link=linkedin_link, twitter_link=twitter_link,competitor_num=competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    instagram_data = InstagramData.instagramDataCompetitor(instagram_username=instagram_username,competitor_num=competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    twitter_data = TwitterData.twitterDataCompetitor(twitter_link=twitter_link, twitter_username=twitter_username,competitor_num=competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    linkedin_data = LinkedinData.linkedinDataCompetitor(linkedin_link=linkedin_link, linkedin_username=linkedin_username,competitor_num=competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    facebook_data = FacebookData.facebookDataCompetitor(facebook_link=facebook_link, facebook_username=facebook_username,competitor_num=competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")


    social_data_times_Competitor = sum([instagram_data, twitter_data, linkedin_data, facebook_data, links_time, username_time])

    simiweb_data = SimiWebData.simiWebDataCompetitor(competitorURL, competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    data_from_pics_data = GetDataFromPics.getDataFromPicsCompetitor(competitorURL, competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    keywords_number_data = GetKeywordsNumber.getKeywordsNumberCompetitor(competitorURL, competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    channel_distrib_data = GetMarketingChannelDistribution.getMarketingChannelDistributionCompetitor(competitorURL, competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")

    semRush_data = SemRushApi.semRushApiCompetitor(competitorURL, competitor_num)
    # Check for termination signal
    if terminate_flag:
        return render_template("error.html", error_message="Process terminated by the user.")


    seo_times = sum([simiweb_data, data_from_pics_data, keywords_number_data, channel_distrib_data, semRush_data])


    total_time = seo_times + social_data_times_Competitor
    return total_time


@appp.route("/", methods=["GET", "POST"])
def index():
    try:
        global terminate_flag
        if request.method == 'POST':
            # Reset the termination flag at the beginning of processing
            terminate_flag = False
            user_input = request.form['user_input']
            url = urllib.parse.urlparse(user_input)
            if not (url.scheme == 'http' or url.scheme == 'https'):
                raise ValueError("Invalid URL. Please ensure your URL starts with 'http' or 'https'.")


            instagram_link, facebook_link, linkedin_link, twitter_link, links_time = SocialLinkCollector.socialLinkCollector(user_input)
            # Check for termination signal
            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")

            instagram_username, facebook_username, linkedin_username, twitter_username, username_time = SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link, facebook_link=facebook_link, linkedin_link=linkedin_link, twitter_link=twitter_link)
            # Check for termination signal
            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")

            simiweb_data = SimiWebData.simiWebData(user_input)
            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")

            data_from_pics_data = GetDataFromPics.getDataFromPics(user_input)
            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")

            competitors_from_pics_data = GetCompetitorsFromPics.getCompetitors(user_input)
            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")

            getCompetitorsFromPics_time, competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5 = competitors_from_pics_data
            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")


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
            # Fetch the manually entered competitors from the form
            competitor1User = request.form.get('competitor1')
            competitor2User = request.form.get('competitor2')
            competitor3User = request.form.get('competitor3')
            competitor4User = request.form.get('competitor4')
            competitor5User = request.form.get('competitor5')
            # List to hold the manually entered competitors
            new_competitors = [competitor1User, competitor2User, competitor3User, competitor4User, competitor5User]
            # Filter out None values and check if they are not already in the competitors list
            manual_competitors = [comp for comp in new_competitors if comp and comp not in competitors]

            if manual_competitors:
                # Replace the last competitors with the manually entered ones
                competitors = competitors[:-len(manual_competitors)] + manual_competitors

            if terminate_flag:
                return render_template("error.html", error_message="Process terminated by the user.")

            competitor_total_times = []
            for i, competitor in enumerate(competitors, start=1):
                if competitor is not None:
                    print('Inside for loop before calling competitor function:', competitor)
                    print(i)
                    competitor_total_time = collect_data_for_competitor(competitor, i)  # passing the competitor number
                    competitor_total_times.append(competitor_total_time)
                    print(f"competitorNo{i}_total_time: {competitor_total_time}")

            rating_time = final.weightRatingSystem()
            total_time += sum(competitor_total_times)
            total_time = total_time + rating_time
            print('Total execution time:', total_time, 'seconds')

            return render_template("result.html", result=total_time)

        else:
            # If the request method is GET, return the HTML form
            return render_template("index.html")

    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500



@appp.route('/download_Social_Media_csv')
def download_csv():
    filenames = ["test.csv",'DataML\Competitors\socialCompetitor_1.csv','DataML\Competitors\socialCompetitor_2.csv','DataML\Competitors\socialCompetitor_3.csv','DataML\Competitors\socialCompetitor_4.csv','DataML\Competitors\socialCompetitor_5.csv']
    zip_filename = "Social_Media_csv_files.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for filename in filenames:
            #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
            path = os.path.abspath(os.path.join(os.getcwd(), filename))
            if filename == "test.csv":
                zipf.write(path, arcname="socialMainCompany.csv")
            else:
                zipf.write(path, arcname=os.path.basename(filename))

    return send_file(zip_filename, as_attachment=True)

@appp.route('/download_SEO_Website_csv')
def download_csv1():
    filenames = ["test1.csv",'DataML\Competitors\seoCompetitor_1.csv','DataML\Competitors\seoCompetitor_2.csv','DataML\Competitors\seoCompetitor_3.csv','DataML\Competitors\seoCompetitor_4.csv','DataML\Competitors\seoCompetitor_5.csv']
    zip_filename = "SEO_and_WEBSITE_csv_files.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for filename in filenames:
            #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
            path = os.path.abspath(os.path.join(os.getcwd(), filename))
            if filename == "test1.csv":
                zipf.write(path, arcname="seoMainCompany.csv")
            else:
                zipf.write(path, arcname=os.path.basename(filename))

    return send_file(zip_filename, as_attachment=True)


@appp.route('/download_Info_csv')
def download_csv_info():
    filename = "t_column_info.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(), filename))
    return send_file(path, as_attachment=True)

@appp.route('/download_Ratings_csv')
def download_csv_final_scores():
    filename = "final_scores.csv"
    #path = os.path.abspath(os.path.join(os.getcwd(), "DigiScore", filename))
    path = os.path.abspath(os.path.join(os.getcwd(),"RatingSystem", filename))
    return send_file(path, as_attachment=True)

# Route to handle termination
@appp.route("/terminate", methods=["GET"])
def terminate():
    global terminate_flag
    terminate_flag = True
    return render_template("error.html", error_message="Process terminated by the user."), 400


if __name__ == '__main__':
    appp.run(debug=True,port=5000)