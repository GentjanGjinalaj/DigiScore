import glob
import os
import time
import pandas as pd
import easyocr
from IPython.display import display
from PIL import Image


def getMarketingChannelDistribution(url):
    # https://www.youtube.com/watch?v=dQw4w9WgXcQ
    st=time.time()
    #return 0
    print('Started executing getMarketingChannelDistribution.py')

    #path1='DigiScore\\DataML\\DataScreenshots'
    #new_path = "DigiScore\\test1.csv"
    path1='DataML\\DataScreenshots'
    new_path = "test1.csv"

    # Set the initial image coordinates
    x1, y1 = 0, 0
    x2, y2 = 1920, 1440
    # Define the folder path

    #picture_folder_path = 'DigiScore\\DataML\\Pics'
    picture_folder_path = 'DataML\\Pics'

    # Get a list of image files in the folder
    image_files = glob.glob(os.path.join(picture_folder_path, '*.png'))  # Change the file extension if necessary

    # Sort the image files based on their modified time
    sorted_files = sorted(image_files, key=os.path.getmtime)

    try:
        # Get the last (most recently modified) image file
        last_image_file = sorted_files[-2]
        print(last_image_file)
        # Load the image
        image = Image.open(last_image_file)
        # Display the image inline
        display(image)
    except Exception as e:
        print('Could not read a picture:',e)
        variables = ['Direct', 'Referrals', 'Organic Search', 'Paid Search', 'Social', 'Mail', 'Display']
        values = [None] * len(variables)

        try:
            print("Entered the nested try except execution")
            df = pd.read_csv(new_path)

            # Prepare the 'Competitors' row
            channelDistrib_row = pd.DataFrame([['Marketing Channel Distribution Panel'] + [''] * (df.shape[1] - 1)], columns=df.columns)

            # Create a DataFrame with the new data and the corresponding column names
            new_data = pd.DataFrame({
                'Website Data': [variables[0], variables[1], variables[2], variables[3], variables[4],variables[5],variables[6]],
                'Website Data Type': ['Direct', 'Referrals', 'Organic Search', 'Paid Search', 'Social', 'Mail', 'Display']
            })

            # Append the new data to the existing DataFrame
            df = pd.concat([df,  channelDistrib_row, new_data], ignore_index=True)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None
            et=time.time()
            #print('Total execution time of GettingDataFromPics.py is:',et-st,'seconds')


        et=time.time()
        getMarketingChannelDistribution_time=et-st
        print('Total execution time of getMarketingChannelDistribution.py is:',getMarketingChannelDistribution_time,'seconds')
        return getMarketingChannelDistribution_time


    # Construct the full file paths
    channelDistrib_path = os.path.join(path1, 'channelDistrib.png')

    # Define the ROIs
    channelDistrib_roi = (190, 235, 1250, 860)
    # Crop the image to the ROIs
    channelDistrib = image.crop(channelDistrib_roi)
    # save the PIL image as a file
    channelDistrib.save(channelDistrib_path)

    # Perform OCR on each ROI
    reader = easyocr.Reader(['en'])
    # perform OCR on the file
    text_all_data = reader.readtext(channelDistrib_path)
    print(text_all_data)


    def get_number(index, text_all_data, var_name):
        while True:
            val = text_all_data[index][1]
            val = val.replace('o', '0').replace('l', '1')  # replace 'o' with '0' and 'l' with '1'
            if val == '0pp0rtunities?' or val == '0iarWvcd':
                val='A'
            if not val[0].isdigit():
                print(f"Check the '{var_name}' in the picture")
                index += 1
                if index >= len(text_all_data):
                    print(f'No valid {var_name} found')
                    return None, None, index
            else:
                confidence = text_all_data[index][2]
                print(f'{var_name}:', val, confidence)
                index += 1  # Move to next item
                return val, confidence, index



    variables = ['Direct', 'Referrals', 'Organic Search', 'Paid Search', 'Social', 'Mail', 'Display']
    values = [None] * len(variables)
    confidences = [None] * len(variables)


    index = 0
    try:
        for i, var_name in enumerate(variables):
            values[i], confidences[i], index = get_number(index, text_all_data, var_name)
    except Exception as e:
        print(f'An error occured while trying to get the data about "{variables[i]}":', e)
        print(text_all_data)
        values[i] = None
        confidences[i] = None


    try:
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(new_path)

        # Prepare the 'Competitors' row
        channelDistrib_row = pd.DataFrame([['Marketing Channel Distribution Panel'] + [''] * (df.shape[1] - 1)], columns=df.columns)

        # Create a DataFrame with the new data and the corresponding column names
        new_data = pd.DataFrame({
            'Website Data': [values[0], values[1], values[2], values[3], values[4], values[5], values[6]],
            'Website Data Type': [variables[0], variables[1], variables[2], variables[3], variables[4], variables[5], variables[6]]
        })

        # Append the new data to the existing DataFrame
        df = pd.concat([df,  channelDistrib_row, new_data], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(new_path, index=False)
        print(df)

    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)
        df = None
        et=time.time()
        #print('Total execution time of GettingDataFromPics.py is:',et-st,'seconds')


    et=time.time()
    getMarketingChannelDistribution_time=et-st
    print('Total execution time of getMarketingChannelDistribution.py is:',getMarketingChannelDistribution_time,'seconds')
    return getMarketingChannelDistribution_time

#getMarketingChannelDistribution('verwok')



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################



def getMarketingChannelDistributionCompetitor(url,competitor_num):
    # https://www.youtube.com/watch?v=dQw4w9WgXcQ
    st=time.time()
    #return 0
    print('Started executing getMarketingChannelDistributionCompetitor.py')

    #path1=f'DigiScore\\DataML\\Competitors\\Competitor_{competitor_num}\\DataScreenshot_{competitor_num}'
    #new_path = f"DigiScore\\DataML\\Competitors\\seoCompetitor_{competitor_num}.csv"
    path1=f'DataML\\Competitors\\Competitor_{competitor_num}\\DataScreenshot_{competitor_num}'
    new_path = f"DataML\\Competitors\\seoCompetitor_{competitor_num}.csv"

    # Set the initial image coordinates
    x1, y1 = 0, 0
    x2, y2 = 1920, 1440
    # Define the folder path

    #picture_folder_path = f'DigiScore\\DataML\\Competitors\\Competitor_{competitor_num}'
    picture_folder_path = f'DataML\\Competitors\\Competitor_{competitor_num}'

    # Get a list of image files in the folder
    image_files = glob.glob(os.path.join(picture_folder_path, '*.png'))  # Change the file extension if necessary

    # Sort the image files based on their modified time
    sorted_files = sorted(image_files, key=os.path.getmtime)

    try:
        # Get the last (most recently modified) image file
        last_image_file = sorted_files[-2]
        print(last_image_file)
        # Load the image
        image = Image.open(last_image_file)
        # Display the image inline
        display(image)
    except Exception as e:
        print('Could not read a picture:',e)
        variables = ['Direct', 'Referrals', 'Organic Search', 'Paid Search', 'Social', 'Mail', 'Display']
        values = [None] * len(variables)

        try:
            print("Entered the nested try except execution")
            df = pd.read_csv(new_path)

            # Prepare the 'Competitors' row
            channelDistrib_row = pd.DataFrame([[f'Marketing Channel Distribution Panel: Competitor_{competitor_num}'] + [''] * (df.shape[1] - 1)], columns=df.columns)

            # Create a DataFrame with the new data and the corresponding column names
            new_data = pd.DataFrame({
                'Website Data': [variables[0], variables[1], variables[2], variables[3], variables[4],variables[5],variables[6]],
                'Website Data Type': ['Direct', 'Referrals', 'Organic Search', 'Paid Search', 'Social', 'Mail', 'Display']
            })

            # Append the new data to the existing DataFrame
            df = pd.concat([df,  channelDistrib_row, new_data], ignore_index=True)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None
            et=time.time()
            #print('Total execution time of GettingDataFromPics.py is:',et-st,'seconds')


        et=time.time()
        getMarketingChannelDistributionCompetitor_time=et-st
        print('Total execution time of getMarketingChannelDistributionCompetitor.py is:',getMarketingChannelDistributionCompetitor_time,'seconds')
        return getMarketingChannelDistributionCompetitor_time


    # Construct the full file paths
    channelDistrib_path = os.path.join(path1, 'channelDistrib.png')

    # Define the ROIs
    channelDistrib_roi = (190, 235, 1250, 860)
    # Crop the image to the ROIs
    channelDistrib = image.crop(channelDistrib_roi)
    # save the PIL image as a file
    channelDistrib.save(channelDistrib_path)

    # Perform OCR on each ROI
    reader = easyocr.Reader(['en'])
    # perform OCR on the file
    text_all_data = reader.readtext(channelDistrib_path)
    print(text_all_data)


    def get_number(index, text_all_data, var_name):
        while True:
            val = text_all_data[index][1]
            val = val.replace('o', '0').replace('l', '1').replace('O','0')  # replace 'o' with '0' and 'l' with '1'
            if val == '0pp0rtunities?' or val == '0iarWvcd':
                val='A'
            if not val[0].isdigit():
                print(f"Check the '{var_name}' in the picture")
                index += 1
                if index >= len(text_all_data):
                    print(f'No valid {var_name} found')
                    return None, None, index
            else:
                confidence = text_all_data[index][2]
                print(f'{var_name}:', val, confidence)
                index += 1  # Move to next item
                return val, confidence, index



    variables = ['Direct', 'Referrals', 'Organic Search', 'Paid Search', 'Social', 'Mail', 'Display']
    values = [None] * len(variables)
    confidences = [None] * len(variables)


    index = 0
    try:
        for i, var_name in enumerate(variables):
            values[i], confidences[i], index = get_number(index, text_all_data, var_name)
    except Exception as e:
        print(f'An error occured while trying to get the data about "{variables[i]}":', e)
        print(text_all_data)
        values[i] = None
        confidences[i] = None


    try:
        # Read the existing CSV file into a DataFrame
        df = pd.read_csv(new_path)

        # Prepare the 'Competitors' row
        channelDistrib_row = pd.DataFrame([[f'Marketing Channel Distribution Panel: Competitor_{competitor_num}'] + [''] * (df.shape[1] - 1)], columns=df.columns)

        # Create a DataFrame with the new data and the corresponding column names
        new_data = pd.DataFrame({
            'Website Data': [values[0], values[1], values[2], values[3], values[4], values[5], values[6]],
            'Website Data Type': [variables[0], variables[1], variables[2], variables[3], variables[4], variables[5], variables[6]]
        })

        # Append the new data to the existing DataFrame
        df = pd.concat([df,  channelDistrib_row, new_data], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(new_path, index=False)
        print(df)

    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)
        df = None
        et=time.time()
        #print('Total execution time of GettingDataFromPics.py is:',et-st,'seconds')


    et=time.time()
    getMarketingChannelDistributionCompetitor_time=et-st
    print('Total execution time of getMarketingChannelDistributionCompetitor.py is:',getMarketingChannelDistributionCompetitor_time,'seconds')
    return getMarketingChannelDistributionCompetitor_time


#getMarketingChannelDistributionCompetitor('verwok',1)