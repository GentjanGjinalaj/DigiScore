import glob
import os
import time
import cv2
import easyocr
import numpy as np
from IPython.display import display
from PIL import Image
from PIL import Image
import pandas as pd


def getKeywordsNumber(url):
    st=time.time()
    #return 0
    print('Started executing GetKeywordsNumber.py')

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
        last_image_file = sorted_files[-1]
        print(last_image_file)
        # Load the image
        image = Image.open(last_image_file)
        # Display the image inline
        display(image)
    except Exception as e:
        print('Could not read a picture:',e)
        total_keywords=None
        organic_keywords_percentage=None
        paid_keywords_percentage=None

        try:
            print("Entered the nested try except execution")
            # Read the existing CSV file into a DataFrame
            df = pd.read_csv(new_path)

            # Prepare the 'Keywords' row
            keywords_row = pd.DataFrame([['Keywords Panel'] + [''] * (df.shape[1] - 1)], columns=df.columns)

            new_data = pd.DataFrame({
                'Website Data': [total_keywords, organic_keywords_percentage, paid_keywords_percentage],
                'Website Data Type': ['Total Keywords', 'Organic Keywords Percentage', 'Paid Keywords Percentage']
            })

            # Append the new data to the existing DataFrame
            df = pd.concat([df,  keywords_row, new_data], ignore_index=True)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)

        et=time.time()
        getKeywordsNumber_time=et-st
        print('Total execution time of GetKeywordsNumber.py is:',getKeywordsNumber_time,'seconds')
        return getKeywordsNumber_time


    # Define the ROIs (x1, y1, x2, y2)
    total_keywords_roi = (900, 600, 1150, 900)
    org_paid_roi = (1580, 240, 1800, 550)

    # Crop the image to the ROIs
    total_keywords_image = image.crop(total_keywords_roi)
    org_paid_image = image.crop(org_paid_roi)

    # Convert the PIL Images to numpy arrays
    total_keywords_np = np.array(total_keywords_image)
    org_paid_np = np.array(org_paid_image)

    # Convert the ROIs to grayscale
    total_keywords_gray = cv2.cvtColor(total_keywords_np, cv2.COLOR_BGR2GRAY)
    org_paid_gray = cv2.cvtColor(org_paid_np, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale images to binary for better OCR accuracy
    total_keywords_binary = cv2.threshold(total_keywords_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    org_paid_binary = cv2.threshold(org_paid_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Convert the binary images back to PIL Images
    total_keywords_image = Image.fromarray(total_keywords_binary)
    org_paid_image = Image.fromarray(org_paid_binary)

    # Construct the full file paths
    total_keywords_image_path = os.path.join(path1, 'total_keywords.png')
    org_paid_image_path = os.path.join(path1, 'org_paid.png')
    # Save the PIL images as files
    total_keywords_image.save(total_keywords_image_path)
    org_paid_image.save(org_paid_image_path)

    # Perform OCR on each ROI
    reader = easyocr.Reader(['en'])
    # perform OCR on the file
    text_total_keywords = reader.readtext(total_keywords_image_path)
    text_org_paid = reader.readtext(org_paid_image_path)
    #print(text_total_keywords)
    #print(text_org_paid)

    # For Total Keywords
    try:
        index = 1
        while True:
            total_keywords_str = text_total_keywords[index][1]
            if not total_keywords_str[0].isdigit():
                print(f"Look at the Total Keywords picture 'total_keywords.png'")
                index += 1
                if index >= len(text_total_keywords):
                    print('No valid Total Keywords found')
                    total_keywords = None
                    confidence_total_keywords = None
                    break
            else:
                confidence_total_keywords = text_total_keywords[index][2]
                print('Total Keywords #5:', total_keywords_str, confidence_total_keywords)
                total_keywords = total_keywords_str
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Total Keywords #5":', e)
        print(text_total_keywords)
        total_keywords = None

    # For Organic and Paid Keywords Percentages
    try:
        index = 1
        organic_index = None
        paid_index = None
        while index < len(text_org_paid):
            if text_org_paid[index][1][-1] == '%':
                if organic_index is None:
                    organic_index = index
                elif paid_index is None:
                    paid_index = index
                    break
            index += 1

        if organic_index is None or paid_index is None:
            print(f"Look at the Organic VS. Paid picture 'org_paid.png'")
            organic_keywords_percentage=None
            paid_keywords_percentage=None
        else:
            organic_keywords_percentage_str = text_org_paid[organic_index][1].replace('O', '0').replace('o', '0').replace('l','1')
            paid_keywords_percentage_str = text_org_paid[paid_index][1].replace('O', '0').replace('o', '0').replace('l','1')

            # Trim percentage to a single zero if it is '000%'
            if organic_keywords_percentage_str == '000%'or organic_keywords_percentage_str == '00%':
                organic_keywords_percentage_str = '0.0%'
            if paid_keywords_percentage_str == '000%' or paid_keywords_percentage_str == '00%':
                paid_keywords_percentage_str = '0.0%'
            confidence_organic_keywords_percentage = text_org_paid[organic_index][2]
            confidence_paid_keywords_percentage = text_org_paid[paid_index][2]
            print('Organic Keywords Percentage:', organic_keywords_percentage_str, confidence_organic_keywords_percentage)
            print('Paid Keywords Percentage:', paid_keywords_percentage_str, confidence_paid_keywords_percentage)
            organic_keywords_percentage = organic_keywords_percentage_str
            paid_keywords_percentage = paid_keywords_percentage_str
    except Exception as e:
        print('An error occured while trying to get the data about "Organic and Paid Keywords Percentages":', e)
        print(text_org_paid)
        organic_keywords_percentage = None
        paid_keywords_percentage = None

    try:
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(new_path)

        # Prepare the 'Keywords' row
        keywords_row = pd.DataFrame([['Keywords Panel'] + [''] * (df.shape[1] - 1)], columns=df.columns)

        new_data = pd.DataFrame({
            'Website Data': [total_keywords, organic_keywords_percentage, paid_keywords_percentage],
            'Website Data Type': ['Total Keywords #5', 'Organic Keywords Percentage', 'Paid Keywords Percentage']
        })

        # Append the new data to the existing DataFrame
        df = pd.concat([df,  keywords_row, new_data], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(new_path, index=False)
        print(df)

    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)

    et=time.time()
    getKeywordsNumber_time=et-st
    print('Total execution time of GetKeywordsNumber.py is:',getKeywordsNumber_time,'seconds')
    return getKeywordsNumber_time

#getKeywordsNumber('rtet')



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################



def getKeywordsNumberCompetitor(url,competitor_num):
    st=time.time()
    #return 0
    print('Started executing GetKeywordsNumberCompetitor.py')

    #path1=f'DigiScore\\DataML\\Competitors\\Competitor_{competitor_num}\\DataScreenshot_{competitor_num}'
    #new_path = f"DigiScore\\DataML\\Competitors\\seoCompetitor_{competitor_num}.csv"
    path1=f'DataML\\Competitors\\Competitor_{competitor_num}\\DataScreenshot_{competitor_num}'
    new_path = f"DataML\\Competitors\\seoCompetitor_{competitor_num}.csv"

    # Set the initial image coordinates
    x1, y1 = 0, 0
    x2, y2 = 1920, 1440

    #picture_folder_path = f'DataML\\Competitors\\Competitor_{competitor_num}'
    picture_folder_path = f'DataML\\Competitors\\Competitor_{competitor_num}'

    # Get a list of image files in the folder
    image_files = glob.glob(os.path.join(picture_folder_path, '*.png'))  # Change the file extension if necessary

    # Sort the image files based on their modified time
    sorted_files = sorted(image_files, key=os.path.getmtime)

    try:
        # Get the last (most recently modified) image file
        last_image_file = sorted_files[-1]
        print(last_image_file)
        # Load the image
        image = Image.open(last_image_file)
        # Display the image inline
        display(image)
    except Exception as e:
        print('Could not read a picture:',e)
        total_keywords=None
        organic_keywords_percentage=None
        paid_keywords_percentage=None

        try:
            print("Entered the nested try except execution")
            # Read the existing CSV file into a DataFrame
            df = pd.read_csv(new_path)

            # Prepare the 'Keywords' row
            keywords_row = pd.DataFrame([[f'Keywords Panel: Competitor_{competitor_num}'] + [''] * (df.shape[1] - 1)], columns=df.columns)

            new_data = pd.DataFrame({
                'Website Data': [total_keywords, organic_keywords_percentage, paid_keywords_percentage],
                'Website Data Type': ['Total Keywords', 'Organic Keywords Percentage', 'Paid Keywords Percentage']
            })

            # Append the new data to the existing DataFrame
            df = pd.concat([df,  keywords_row, new_data], ignore_index=True)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)

        et=time.time()
        getKeywordsNumberCompetitor_time=et-st
        print('Total execution time of GetKeywordsNumberCompetitor.py is:',getKeywordsNumberCompetitor_time,'seconds')
        return getKeywordsNumberCompetitor_time


    # Define the ROIs (x1, y1, x2, y2)
    total_keywords_roi = (900, 600, 1150, 900)
    org_paid_roi = (1580, 240, 1800, 550)

    # Crop the image to the ROIs
    total_keywords_image = image.crop(total_keywords_roi)
    org_paid_image = image.crop(org_paid_roi)

    # Convert the PIL Images to numpy arrays
    total_keywords_np = np.array(total_keywords_image)
    org_paid_np = np.array(org_paid_image)

    # Convert the ROIs to grayscale
    total_keywords_gray = cv2.cvtColor(total_keywords_np, cv2.COLOR_BGR2GRAY)
    org_paid_gray = cv2.cvtColor(org_paid_np, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale images to binary for better OCR accuracy
    total_keywords_binary = cv2.threshold(total_keywords_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    org_paid_binary = cv2.threshold(org_paid_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Convert the binary images back to PIL Images
    total_keywords_image = Image.fromarray(total_keywords_binary)
    org_paid_image = Image.fromarray(org_paid_binary)

    # Construct the full file paths
    total_keywords_image_path = os.path.join(path1, 'total_keywords.png')
    org_paid_image_path = os.path.join(path1, 'org_paid.png')

    # Save the PIL images as files
    total_keywords_image.save(total_keywords_image_path)
    org_paid_image.save(org_paid_image_path)

    # Perform OCR on each ROI
    reader = easyocr.Reader(['en'])
    # perform OCR on the file
    text_total_keywords = reader.readtext(total_keywords_image_path)
    text_org_paid = reader.readtext(org_paid_image_path)
    #print(text_total_keywords)
    #print(text_org_paid)

    # For Total Keywords
    try:
        index = 1
        while True:
            total_keywords_str = text_total_keywords[index][1]
            if not total_keywords_str[0].isdigit():
                print(f"Look at the Total Keywords picture 'total_keywords.png'")
                index += 1
                if index >= len(text_total_keywords):
                    print('No valid Total Keywords found')
                    total_keywords = None
                    confidence_total_keywords = None
                    break
            else:
                confidence_total_keywords = text_total_keywords[index][2]
                print('Total Keywords #5:', total_keywords_str, confidence_total_keywords)
                total_keywords = total_keywords_str
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Total Keywords #5":', e)
        print(text_total_keywords)
        total_keywords = None

    # For Organic and Paid Keywords Percentages
    try:
        index = 1
        organic_index = None
        paid_index = None
        while index < len(text_org_paid):
            if text_org_paid[index][1][-1] == '%':
                if organic_index is None:
                    organic_index = index
                elif paid_index is None:
                    paid_index = index
                    break
            index += 1

        if organic_index is None or paid_index is None:
            print(f"Look at the Organic VS. Paid picture 'org_paid.png'")
            organic_keywords_percentage=None
            paid_keywords_percentage=None
        else:
            organic_keywords_percentage_str = text_org_paid[organic_index][1].replace('O', '0').replace('o', '0').replace('l','1')
            paid_keywords_percentage_str = text_org_paid[paid_index][1].replace('O', '0').replace('o', '0').replace('l','1')

            # Trim percentage to a single zero if it is '000%'
            if organic_keywords_percentage_str == '000%'or organic_keywords_percentage_str == '00%':
                organic_keywords_percentage_str = '0.0%'
            if paid_keywords_percentage_str == '000%' or paid_keywords_percentage_str == '00%':
                paid_keywords_percentage_str = '0.0%'
            confidence_organic_keywords_percentage = text_org_paid[organic_index][2]
            confidence_paid_keywords_percentage = text_org_paid[paid_index][2]
            print('Organic Keywords Percentage:', organic_keywords_percentage_str, confidence_organic_keywords_percentage)
            print('Paid Keywords Percentage:', paid_keywords_percentage_str, confidence_paid_keywords_percentage)
            organic_keywords_percentage = organic_keywords_percentage_str
            paid_keywords_percentage = paid_keywords_percentage_str
    except Exception as e:
        print('An error occured while trying to get the data about "Organic and Paid Keywords Percentages":', e)
        print(text_org_paid)
        organic_keywords_percentage = None
        paid_keywords_percentage = None

    try:
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(new_path)

        # Prepare the 'Keywords' row
        keywords_row = pd.DataFrame([[f'Keywords Panel: Competitor_{competitor_num}'] + [''] * (df.shape[1] - 1)], columns=df.columns)

        new_data = pd.DataFrame({
            'Website Data': [total_keywords, organic_keywords_percentage, paid_keywords_percentage],
            'Website Data Type': ['Total Keywords #5', 'Organic Keywords Percentage', 'Paid Keywords Percentage']
        })

        # Append the new data to the existing DataFrame
        df = pd.concat([df,  keywords_row, new_data], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(new_path, index=False)
        print(df)

    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)

    et=time.time()
    getKeywordsNumberCompetitor_time=et-st
    print('Total execution time of GetKeywordsNumberCompetitor.py is:',getKeywordsNumberCompetitor_time,'seconds')
    return getKeywordsNumberCompetitor_time


#getKeywordsNumberCompetitor('rtet',1)