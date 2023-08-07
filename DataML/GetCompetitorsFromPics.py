import glob
from io import StringIO
import os
import re
import easyocr
from IPython.display import display
from PIL import Image
import time
import pandas as pd
import requests


def getCompetitors(mainUrl):
    st=time.time()
    #return 0,'axa.com','neoma-bs.fr','yumens.fr','ads-up.fr','youlovewords.com'#lescausantes.com'
    print('Started executing GetCompetitorsFromPics.py')
    #mainUrl=url

    #path1='DigiScore\\DataML\\DataScreenshots'
    #new_path = "DigiScore\\test1.csv"
    path1='DataML\\DataScreenshots'
    new_path = "test1.csv"

    # Set the initial image coordinates
    x1, y1 = 0, 0
    x2, y2 = 1920, 1440

    #picture_folder_path = 'DigiScore\\DataML\\Pics'
    picture_folder_path = 'DataML\\Pics'

    # Get a list of image files in the folder
    image_files = glob.glob(os.path.join(picture_folder_path, '*.png'))  # Change the file extension if necessary

    # Sort the image files based on their modified time
    sorted_files = sorted(image_files, key=os.path.getmtime)

    try:
        # Get the last (most recently modified) image file
        last_image_file = sorted_files[-3]
        print(last_image_file)
        # Load the image
        image = Image.open(last_image_file)
        # Display the image inline
        display(image)
    except Exception as e:
        print('Could not read a picture:',e)
        competitor_No1=None
        competitor_No2=None
        competitor_No3=None
        competitor_No4=None
        competitor_No5=None

        try:
            print("Entered the nested try except execution")
            df = pd.read_csv(new_path)

            # Prepare the 'Competitors' row
            competitors_row = pd.DataFrame([['Competitors Panel'] + [''] * (df.shape[1] - 1)], columns=df.columns)

            # Create a DataFrame with the new data and the corresponding column names
            new_data = pd.DataFrame({
                'Website Data': [competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5],
                'Website Data Type': ['First Competitor', 'Second Competitor', 'Third Competitor', 'Fourth Competitor', 'Fifth Competitor']
            })

            # Append the new data to the existing DataFrame
            df = pd.concat([df,  competitors_row, new_data], ignore_index=True)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None
            et=time.time()
            #print('Total execution time of GettingCompetitorsFromPics.py is:',et-st,'seconds')


        et=time.time()
        getCompetitorsFromPics_time=et-st
        print('Total execution time of GetCompetitorsFromPics.py is:',getCompetitorsFromPics_time,'seconds')
        return getCompetitorsFromPics_time

    # Construct the full file paths
    competitors_path = os.path.join(path1, 'competitors.png')
    # Define the ROIs
    competitors_roi = (200, 250, 570, 850)
    # Crop the image to the ROIs
    competitors = image.crop(competitors_roi)
    # save the PIL image as a file
    competitors.save(competitors_path)

    # Perform OCR on each ROI
    reader = easyocr.Reader(['en'])
    # perform OCR on the file
    text_competitors = reader.readtext(competitors_path)

    competitors = []
    try:
        index = 0
        while len(competitors) < 5 and index < len(text_competitors):
            competitor = text_competitors[index][1]
            confidence_competitor = text_competitors[index][2]

            # Check if the competitor's length is less than 4 characters or ends with 'L'
            if len(competitor) < 4 or competitor[-1] == 'L':
                index += 1
                continue

            # Replace ":" with "."
            competitor = competitor.replace(":", ".")

            if competitor[:4].lower() != "site":
                competitors.append((competitor, confidence_competitor))
                print(f'Competitor {len(competitors)}:', competitor, confidence_competitor)

            index += 1

        if len(competitors) < 5:
            print('Fewer than 5 valid competitors found.')
            # pad competitors list with None values
            while len(competitors) < 5:
                competitors.append((None, None))

    except Exception as e:
        print('An error occurred while trying to get the data about "Competitors":', e)
        print(text_competitors)

    first_competitor, confidence_first_competitor = competitors[0]
    second_competitor, confidence_second_competitor = competitors[1]
    third_competitor, confidence_third_competitor = competitors[2]
    fourth_competitor, confidence_fourth_competitor = competitors[3]
    fifth_competitor, confidence_fifth_competitor = competitors[4]
    print(first_competitor,'first_competitor')


    def fix_url(url):

        if url is None:  # If the url is None, return None
            return None

        # Remove whitespace and replace with dots
        url = url.replace(' ', '.')

        # Delete 'www' at the start
        if url.startswith('www'):
            url = url[3:]
        if url.endswith('fr'):
            url = url[:-2] + '.' + url[-2:]
        elif url.endswith('com'):
            if url[-4:] != '.com':
                url = url[:-3] + '.' + url[-3:]
        elif url.endswith('net'):
            if url[-4:] != '.net':
                url = url[:-3] + '.' + url[-3:]
        elif url.endswith('site'):
            if url[-5:] != '.site':
                url = url[:-4] + '.' + url[-4:]

        # Check if the URL already contains a valid domain extension
        valid_extensions = ['.fr', '.com', '.net']  # Add more valid extensions if needed
        if any(url.endswith(ext) for ext in valid_extensions):
            # Remove consecutive dots and ensure only one dot between parts
            url = re.sub(r'\.+', '.', url)
            url = re.sub(r'\.(?=[^.]*\.)', '', url)
            return url

        # Handle 'co' at the end of the string with different scenarios
        co_match = re.search(r'co[_\.]+$', url)
        if co_match:
            url = url[:co_match.start()] + '.com'

    # Remove non-alphanumeric character if present at the end of the string
        if not url[-1].isalnum():
            url = url[:-1]

        if url.endswith('cons'):
            url += 'eil.fr'

        if url.endswith('.Top.Mar'):
            url = url.replace('.Top.Mar','')
            return url

        if url.endswith('.channels.dr'):
            url = None
            return url

        if url.endswith('.Distributio'):
            url = None
            return url

        return url

    competitor_No1 = fix_url(first_competitor) if first_competitor is not None else None
    competitor_No2 = fix_url(second_competitor) if second_competitor is not None else None
    competitor_No3 = fix_url(third_competitor) if third_competitor is not None else None
    competitor_No4 = fix_url(fourth_competitor) if fourth_competitor is not None else None
    competitor_No5 = fix_url(fifth_competitor) if fifth_competitor is not None else None
    print(competitor_No1)
    print(competitor_No2)
    print(competitor_No3)
    print(competitor_No4)
    print(competitor_No5)

    competitors = [competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5]
    competitorEqualMainUrl= False
    mainUrl = mainUrl.replace('https://www.', '').replace('https://', '').replace('www.', '').replace('/', '')  # Remove 'https://www.' from the URL
    # Check if any competitor has the same URL as the passed URL
    for competitor in competitors:
        if competitor == mainUrl:
            competitorEqualMainUrl=True
            print('The URL is found in the competitors list.')
            print(mainUrl)
            try:
                api_key = '8bdbff61b7aa7c84bd0a8be0ffb526c9'
                response=requests.get('http://www.semrush.com/users/countapiunits.html?key=8bdbff61b7aa7c84bd0a8be0ffb526c9')
                print(response)
                print(response.text)
                apiUnitsBeforeExecution = response.text
                apiUnitsBeforeExecution=int(apiUnitsBeforeExecution)
                print('API_Units_Before_Execution:',apiUnitsBeforeExecution)
                #call the competitors API from semrush to get 5 competitors. The cost will be 200 API units
                response=requests.get(f'https://api.semrush.com/?type=domain_organic_organic&key={api_key}&display_limit=5&export_columns=Dn,Cr,Np,Or,Ot,Oc,Ad,Sr,St,Sc&domain={mainUrl}&database=fr')
                print(response)
                print(response.text)
                data = pd.read_csv(StringIO(response.text), sep=';')  # Specify delimiter

                # Initialize all competitors to None
                competitor_No1 = None
                competitor_No2 = None
                competitor_No3 = None
                competitor_No4 = None
                competitor_No5 = None

                for i, row in data.iterrows():
                    competitor_Dn = row['Domain']

                    # Assign the value of Dn to the corresponding competitor variable
                    if i == 0:
                        competitor_No1 = competitor_Dn
                    elif i == 1:
                        competitor_No2 = competitor_Dn
                    elif i == 2:
                        competitor_No3 = competitor_Dn
                    elif i == 3:
                        competitor_No4 = competitor_Dn
                    elif i == 4:
                        competitor_No5 = competitor_Dn
                '''# Assuming the first row of the DataFrame is the relevant data
                data_dict = data.iloc[0].to_dict()
                print('--------------------------------------------------------------------------------------------')
                print(data_dict)
                print('--------------------------------------------------------------------------------------------')

                # Check if each key exists in the dictionary before unpacking
                Dn = data_dict.get('Dn', None)
                Cr = data_dict.get('Cr', None)
                Np = data_dict.get('Np', None)
                Or = data_dict.get('Or', None)
                Ot = data_dict.get('Ot', None)
                Oc = data_dict.get('Oc', None)
                Od = data_dict.get('Ad', None)
                Sr = data_dict.get('Sr', None)
                St = data_dict.get('St', None)
                Sc = data_dict.get('Sc', None)'''

            except Exception as e:
                print(f'An error occurred: {e}')
                competitor_No1 = None
                competitor_No2 = None
                competitor_No3 = None
                competitor_No4 = None
                competitor_No5 = None
                '''Dn = None
                Cr = None
                Np = None
                Or = None
                Ot = None
                Oc = None
                Od = None
                Sr = None
                St = None
                Sc = None'''
            try:
                #API units balance
                response=requests.get('http://www.semrush.com/users/countapiunits.html?key=8bdbff61b7aa7c84bd0a8be0ffb526c9')
                print(response)
                print(response.text)
                apiUnitsAfterExecution = response.text
                apiUnitsAfterExecution=int(apiUnitsAfterExecution)
                apiUnitsSpent = apiUnitsAfterExecution-apiUnitsBeforeExecution
                print('API_Units_Left:',apiUnitsAfterExecution)
                print('API_Units_Spent:',apiUnitsSpent)
            except Exception as e:
                print("An error occured:",e)
            #return Dn,Cr,Np,Or,Ot,Oc,Od,Sr,St,Sc
        else:
            print('The URL is not found in the competitors list.')
            print(mainUrl)



    none_indices = [i for i, competitor in enumerate(competitors) if competitor is None]
    # Get the length of the none_indices array
    length_of_none_indices = len(none_indices)
    if competitorEqualMainUrl == False:
        if length_of_none_indices<6 and length_of_none_indices>0:
            try:
                print('The number of None competitors is:',length_of_none_indices,' at the positions:',none_indices)

                # Fetch the data from the API only once for all the None values
                api_key = '8bdbff61b7aa7c84bd0a8be0ffb526c9'

                api_key = '8bdbff61b7aa7c84bd0a8be0ffb526c9'
                response=requests.get(f'http://www.semrush.com/users/countapiunits.html?key={api_key}')
                print(response)
                print('API units before execution',response.text)
                apiUnitsBeforeExecution = response.text
                apiUnitsBeforeExecution=int(apiUnitsBeforeExecution)

                try:
                    response = requests.get(f'https://api.semrush.com/?type=domain_organic_organic&key={api_key}&display_limit={length_of_none_indices}&export_columns=Dn,Cr,Np,Or,Ot,Oc,Ad,Sr,St,Sc&domain={mainUrl}&database=fr')
                    #response = requests.get(f'https://api.semrush.com/?type=domain_organic_organic&key={api_key}&display_limit={1}&export_columns=Dn,Cr,Np,Or,Ot,Oc,Ad,Sr,St,Sc&domain={mainUrl}&database=fr')
                    data = pd.read_csv(StringIO(response.text), sep=';')  # Specify delimiter
                    print(data.columns)
                except Exception as e:
                    print(f'Error occurred: {e}')

                if not data.empty:
                    # Assuming that the API response provides data in order and fills the competitors list accordingly.
                    # If the assumption is incorrect, you may need to implement a more sophisticated matching mechanism.

                    # Iterate over None indices and update the competitor_NoX variables
                    for idx, api_row in zip(none_indices, data.itertuples()):
                        competitor_Dn = getattr(api_row, 'Domain')  # Get the 'Domain' data from the API response

                        # Assign the value of Dn to the corresponding competitor variable
                        if idx == 0:
                            competitor_No1 = competitor_Dn
                        elif idx == 1:
                            competitor_No2 = competitor_Dn
                        elif idx == 2:
                            competitor_No3 = competitor_Dn
                        elif idx == 3:
                            competitor_No4 = competitor_Dn
                        elif idx == 4:
                            competitor_No5 = competitor_Dn

                    #API units balance
                    response=requests.get(f'http://www.semrush.com/users/countapiunits.html?key={api_key}')
                    print(response)
                    print(response.text)
                    apiUnitsAfterExecution = response.text
                    apiUnitsAfterExecution=int(apiUnitsAfterExecution)
                    apiUnitsSpent = apiUnitsAfterExecution-apiUnitsBeforeExecution
                    print('API_Units_Left:',apiUnitsAfterExecution)
                    print('API_Units_Spent:',apiUnitsSpent)

                else:
                    print('API did not return any data.')
            except Exception as e:
                print(f'An error occurred: {e}')
        elif length_of_none_indices == 0:
            print('There are no missing competitors but exactly 5 competitors')

        else:
            print('Look carefully at the number of None competitors',none_indices,'at the length:',length_of_none_indices)
            print('List of competitors:', competitors)



    try:
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(new_path)

        # Prepare the 'Competitors' row
        competitors_row = pd.DataFrame([['Competitors Panel'] + [''] * (df.shape[1] - 1)], columns=df.columns)

        # Append the 'Competitors' row and the new data to the existing DataFrame
        #df = pd.concat([df, competitors_row], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        #df.to_csv(path, index=False)

        #df = pd.read_csv(path)
        # Create a DataFrame with the new data and the corresponding column names
        new_data = pd.DataFrame({
            'Website Data': [competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5],
            'Website Data Type': ['First Competitor', 'Second Competitor', 'Third Competitor', 'Fourth Competitor', 'Fifth Competitor']
        })

        # Append the new data to the existing DataFrame
        df = pd.concat([df,  competitors_row, new_data], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(new_path, index=False)
        print(df)

    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)


    et=time.time()
    getCompetitorsFromPics_time=et-st
    print('Total execution time of GetCompetitorsFromPics.py is:',getCompetitorsFromPics_time,'seconds')
    return getCompetitorsFromPics_time,competitor_No1, competitor_No2, competitor_No3, competitor_No4, competitor_No5


#getCompetitors('ebs-paris.fr')
#getCompetitors('evs')