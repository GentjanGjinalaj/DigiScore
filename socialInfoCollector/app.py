import os
from flask import Flask,request,render_template,send_file
import sys
#from DigiScore.socialInfoCollector.SocialUsernameCollector import socialUsernameCollector

#sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')
#sys.path.insert(0,'./socialInfoCollector')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\templates')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\templates\\result.html')
sys.path.append('C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\templates\\index.html')
#print(sys.path)
#sys.path.insert(0, 'C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\socialInfoCollector\\InstagramData.py')

import SocialLinkCollector
import SocialUsernameCollector
import InstagramData
import LinkedinData
import FacebookData
import TwitterData

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        instagram_link,facebook_link,linkedin_link,twitter_link,links_time = SocialLinkCollector.socialLinkCollector(user_input)
        instagram_username,facebook_username,linkedin_username,twitter_username,username_time=SocialUsernameCollector.socialUsernameCollector(instagram_link=instagram_link,facebook_link=facebook_link,linkedin_link=linkedin_link,twitter_link=twitter_link)
        instagram_time=InstagramData.instagramData(instagram_username=instagram_username)
        linkedin_time=LinkedinData.linkedinData(linkedin_link=linkedin_link,linkedin_username=linkedin_username)
        facebook_time=FacebookData.facebookData(facebook_link=facebook_link,facebook_username=facebook_username)
        twitter_time=TwitterData.twitterData(twitter_link=twitter_link,twitter_username=twitter_username)
        result=instagram_time+linkedin_time+facebook_time+twitter_time+links_time+username_time
        print('Total execution time:',result)

        # Create the CSV file and write the data to it

        return render_template("result.html",result=result)
    else:
        return render_template("index.html")

'''  return render_template("result.html", result=result)
    # If the request method is GET, return the HTML form
    return render_template("index.html")
'''


@app.route('/download_csv')
def download_csv():
    path = "C:\\Users\\User\\OneDrive - Fakulteti i Teknologjise se Informacionit\\Desktop\\Digitalized\\DigiScore\\test.csv"
    return send_file(path, as_attachment=True)


def result():
    # get user input from the form
    user_input = request.form['user_input']

    # use user input to generate your CSV file
    # save your CSV file in a desired location
    # set the file_path variable to the path of the saved CSV file

    # construct the file download response
    directory, filename = os.path.split('DigiScore\\test.csv')
    return send_file('test.csv', attachment_filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,port=5000)