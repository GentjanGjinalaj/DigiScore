import glob
import os
import re
import easyocr
from IPython.display import display
from PIL import Image
import cv2
import numpy as np
import time
import pandas as pd

def getCompetitors(url):
    st=time.time()

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
        print('Total execution time of GettingCompetitorsFromPics.py is:',getCompetitorsFromPics_time,'seconds')
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


        # Replace 'L' at the end of the string with '...'
        if url.endswith('L'):
            url = url[:-1] + '...'

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
    print('Total execution time of GettingCompetitorsFromPics.py is:',getCompetitorsFromPics_time,'seconds')
    return getCompetitorsFromPics_time


#getCompetitors('ewtw')