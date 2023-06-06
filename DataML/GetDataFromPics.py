import glob
import os
import easyocr
from IPython.display import display
from PIL import Image
import cv2
import numpy as np
import time
import pandas as pd


def getDataFromPics(url):
    st=time.time()
    print('Started executing GettingDataFromPics.py')
    path1='DigiScore\\DataML\\DataScreenshots'
    path = "DigiScore\\test.csv"
    new_path = "DigiScore\\test1.csv"

    # Set the initial image coordinates
    x1, y1 = 0, 0
    x2, y2 = 1920, 1440
    # Define the folder path
    picture_folder_path = 'DigiScore\\DataML\\Pics'

    # Get a list of image files in the folder
    image_files = glob.glob(os.path.join(picture_folder_path, '*.png'))  # Change the file extension if necessary

    # Sort the image files based on their modified time
    sorted_files = sorted(image_files, key=os.path.getmtime)

    try:
        # Get the last (most recently modified) image file
        last_image_file = sorted_files[-4]
        print(last_image_file)
        # Load the image
        image = Image.open(last_image_file)
        # Display the image inline
        display(image)
    except Exception as e:
        print('Could not read a picture:',e)
        category_name=None
        category_rank=None
        total_visits=None
        bounce_rate=None
        pages_per_visit=None
        avg_visit_dur=None

        try:
            print("Entered the nested try except execution")
            # Prepare the 'Website' row
            title_row = pd.DataFrame([{'Website Data Type': 'Website Panel'}])

            # Write the 'Website' row to the CSV file
            title_row.to_csv(new_path, index=False)

            # Create a DataFrame with the new data and the corresponding column names
            new_data = pd.DataFrame({
                'Website Data': [category_name, category_rank, total_visits, bounce_rate, pages_per_visit, avg_visit_dur],
                'Website Data Type': ['Category Name', 'Category Rank', 'Total Visits', 'Bounce Rate', 'Pages per Visit', 'Average Visit Duration']
            })

            # Read the CSV file
            df = pd.read_csv(new_path)

            # Append the new data to the existing DataFrame
            df = pd.concat([df, new_data], ignore_index=True)

            # Write the updated DataFrame back to the CSV file
            df.to_csv(new_path, index=False)
            print(df)

        except Exception as e:
            print("An error occurred while reading the CSV file: ", e)
            df = None
            et=time.time()
            #print('Total execution time of GettingDataFromPics.py is:',et-st,'seconds')


        et=time.time()
        getDataFromPics_time=et-st
        print('Total execution time of GettingDataFromPics.py is:',getDataFromPics_time,'seconds')
        return getDataFromPics_time



    '''
    # Create a new image with the same dimensions as the original image
    new_image = Image.new('RGBA', image.size, (255, 255, 255, 0))

    # Draw the original image on the new image
    new_image.paste(image, (0, 0))


    # Draw the axis on the image
    def draw_axis(new_image):
        draw = ImageDraw.Draw(new_image)

        # Draw the horizontal axis
        draw.line((x1, y1, x2, y1), fill='red', width=3)
        font = ImageFont.truetype("arial.ttf", 20)
        for i in range(0, 1920, 100):
            draw.text((i, 0), str(i), font=font, fill='red')

        # Draw the vertical axis
        draw.line((x1, y1, x1, y2), fill='red', width=3)
        for i in range(0, 1440, 100):
            draw.text((0, i), str(i), font=font, fill='red')

    draw_axis(new_image)

    # Display the image with the axis inline
    display(new_image)

    '''
                ##############################

    '''
    # Define the ROIs
    category_roi = (1450, 280, 1830, 585) # 1500, 215, 1719, 512
    visits_roi = (200, 490, 450, 800)
    bounce_roi = (615, 490, 860, 800)
    page_visit_roi = (1025, 490, 1290, 800)
    avg_visit_dur_roi = (1450, 500, 1770, 800)

    # Crop the image to the ROIs
    category = image.crop(category_roi)
    visits = image.crop(visits_roi)
    bounce = image.crop(bounce_roi)
    pages_visits = image.crop(page_visit_roi)
    avg_visit_dur = image.crop(avg_visit_dur_roi)

    # Construct the full file paths
    category_path = os.path.join(path1, 'category.png')
    visits_path = os.path.join(path1, 'visits.png')
    bounce_path = os.path.join(path1, 'bounce.png' )
    pages_per_visit_path = os.path.join(path1, 'pages_visits.png')
    avg_visit_dur_path = os.path.join(path1, 'avg_visit_dur.png')


    # save the PIL image as a file
    category.save(category_path)
    visits.save(visits_path)
    bounce.save(bounce_path)
    pages_visits.save(pages_per_visit_path)
    avg_visit_dur.save(avg_visit_dur_path)'''


    ###################################################################

    # Define the ROIs
    category_roi = (1450, 280, 1830, 580)
    visits_roi = (200, 490, 450, 800)
    bounce_roi = (615, 490, 860, 800)
    page_visit_roi = (1025, 490, 1290, 800)
    avg_visit_dur_roi = (1450, 500, 1770, 800)

    # Crop the image to the ROIs
    category_image = image.crop(category_roi)
    visits_image = image.crop(visits_roi)
    bounce_image = image.crop(bounce_roi)
    page_visit_image = image.crop(page_visit_roi)
    avg_visit_dur_image = image.crop(avg_visit_dur_roi)

    # Construct the full file paths
    category_path = os.path.join(path1, 'category.png')
    visits_path = os.path.join(path1, 'visits.png')
    bounce_path = os.path.join(path1, 'bounce.png' )
    pages_per_visit_path = os.path.join(path1, 'pages_visits.png')
    avg_visit_dur_path = os.path.join(path1, 'avg_visit_dur.png')

    # Convert the PIL Images to numpy arrays
    category_np = np.array(category_image)
    visits_np = np.array(visits_image)
    bounce_np = np.array(bounce_image)
    page_visit_np = np.array(page_visit_image)
    avg_visit_dur_np = np.array(avg_visit_dur_image)

    # Convert the ROIs to grayscale
    category_gray = cv2.cvtColor(category_np, cv2.COLOR_BGR2GRAY)
    visits_gray = cv2.cvtColor(visits_np, cv2.COLOR_BGR2GRAY)
    bounce_gray = cv2.cvtColor(bounce_np, cv2.COLOR_BGR2GRAY)
    page_visit_gray = cv2.cvtColor(page_visit_np, cv2.COLOR_BGR2GRAY)
    avg_visit_dur_gray = cv2.cvtColor(avg_visit_dur_np, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale images to binary for better OCR accuracy
    category_binary = cv2.threshold(category_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    visits_binary = cv2.threshold(visits_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    bounce_binary = cv2.threshold(bounce_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    page_visit_binary = cv2.threshold(page_visit_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    avg_visit_dur_binary = cv2.threshold(avg_visit_dur_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Convert the binary images back to PIL Images
    category_image = Image.fromarray(category_binary)
    visits_image = Image.fromarray(visits_binary)
    bounce_image = Image.fromarray(bounce_binary)
    page_visit_image = Image.fromarray(page_visit_binary)
    avg_visit_dur_image = Image.fromarray(avg_visit_dur_binary)

    # Save the PIL images as files
    category_image.save(category_path)
    visits_image.save(visits_path)
    bounce_image.save(bounce_path)
    page_visit_image.save(pages_per_visit_path)
    avg_visit_dur_image.save(avg_visit_dur_path)

    #################################################################################

    # Perform OCR on each ROI
    reader = easyocr.Reader(['en'])

    # perform OCR on the file
    text_category_rank = reader.readtext(category_path)
    text_total_visits = reader.readtext(visits_path)
    text_bounce_rate = reader.readtext(bounce_path)
    text_pages_per_visit = reader.readtext(pages_per_visit_path)
    text_avg_visit_duration = reader.readtext(avg_visit_dur_path)


    # Extract the required information from ROI
    try:
        print(text_category_rank)
        # Initialize the starting index.
        index = 1

        while True:
            category_rank = text_category_rank[index][1]
            category_rank = category_rank.replace("#","").replace(" ","").replace(',','')
            if len(category_rank) == 0 or not category_rank[0].isdigit():
                print("Look at the Category Rank picture 'category.png'")
                index += 1
                if index >= len(text_category_rank):
                    print('No valid Category Rank found')
                    category_rank = None
                    confidence_category_rank = None
                    break
            else:
                confidence_category_rank = text_category_rank[index][2]
                category_name = text_category_rank[index+2][1]
                confidence_category_name = text_category_rank[index+2][2]
                if "and" in category_name and index+3 < len(text_category_rank):
                    # If the category name ends with 'and', append the next part
                    category_name += ' ' + text_category_rank[index+3][1]
                    # Calculate the average confidence
                    confidence_category_name = (confidence_category_name + text_category_rank[index+3][2]) / 2
                print('Category Rank:', category_rank, confidence_category_rank,category_name, confidence_category_name)
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Category Rank":',e)
        category_rank = None
        category_name = None



    try:
        #print(text_total_visits)
        index = 1
        while True:
            total_visits = text_total_visits[index][1]
            if not total_visits[0].isdigit():
                print("Look at the Total Visits picture 'pages_visits.png'")
                index += 1
                if index >= len(text_total_visits):
                    print('No valid Total Visits found')
                    total_visits = None
                    confidence_visits = None
                    break
            else:
                confidence_visits = text_total_visits[index][2]
                print('Total Visits:', total_visits, confidence_visits)
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Total Visits":',e)
        print(text_total_visits)
        total_visits = None

    try:
        #print(text_bounce_rate)
        index = 1

        while True:
            #print(text_bounce_rate)
            bounce_rate = text_bounce_rate[index][1]
            if not bounce_rate[0].isdigit():
                print("Look at the Bounce Rate picture 'bounce.png'")
                index += 1  # Increase the index for the next iteration.
                if index >= len(text_bounce_rate):
                    print('No valid Bounce Rate found')
                    bounce_rate = None
                    confidence_bounce_rate = None
                    break
            else:
                confidence_bounce_rate = text_bounce_rate[index][2]
                # Print the detected text
                print('Bounce Rate:', bounce_rate, confidence_bounce_rate)
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Bounce Rate":', e)
        print(text_bounce_rate)
        bounce_rate = None



    try:
        #print(text_pages_per_visit)
        index = 1
        while True:
            pages_per_visit = text_pages_per_visit[index][1]
            if not pages_per_visit[0].isdigit():
                print("Look at the Pages Per Visit picture 'pages_visits.png'")
                index += 1
                if index >= len(text_pages_per_visit):
                    print('No valid Pages per Visit found')
                    pages_per_visit = None
                    confidence_pages_per_visit = None
                    break
            else:
                confidence_pages_per_visit = text_pages_per_visit[index][2]
                print('Pages per Visit:', pages_per_visit, confidence_pages_per_visit)
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Pages per Visit":',e)
        print(text_pages_per_visit)
        pages_per_visit = None

    try:
        #print(text_avg_visit_duration)
        index = 1
        while True:
            avg_visit_dur = text_avg_visit_duration[index][1]
            avg_visit_dur = avg_visit_dur.replace(".",":")
            if not avg_visit_dur[0].isdigit():
                print(f"Look at the Average Visit Duration picture 'avg_visit_dur.png'")
                index += 1
                if index >= len(text_avg_visit_duration):
                    print('No valid Average Visit Duration found')
                    avg_visit_dur = None
                    confidence_avg_visits_dur = None
                    break
            else:
                confidence_avg_visits_dur = text_avg_visit_duration[index][2]
                print('Avarage Visit Duration:', avg_visit_dur, confidence_avg_visits_dur)
                break
    except Exception as e:
        print('An error occured while trying to get the data about "Avarage Visit Duration":',e)
        print(text_avg_visit_duration)
        avg_visit_dur=None


    try:
        # Prepare the 'Website' row
        title_row = pd.DataFrame([{'Website Data Type': 'Website Panel'}])

        # Write the 'Website' row to the CSV file
        title_row.to_csv(new_path, index=False)

        # Create a DataFrame with the new data and the corresponding column names
        new_data = pd.DataFrame({
            'Website Data Type': ['Category Name', 'Category Rank', 'Total Visits', 'Bounce Rate', 'Pages per Visit', 'Average Visit Duration'],
            'Website Data': [category_name, category_rank, total_visits, bounce_rate, pages_per_visit, avg_visit_dur]
        })

        df = pd.read_csv(new_path)
        # Concatenate the existing DataFrame with the new data
        df = pd.concat([df, new_data], ignore_index=True)

        # Write the updated DataFrame back to the CSV file
        df.to_csv(new_path, index=False)

    except Exception as e:
        print("An error occurred while reading the CSV file: ", e)
        df = None
        et=time.time()
        #print('Total execution time of GettingDataFromPics.py is:',et-st,'seconds')


    et=time.time()
    getDataFromPics_time=et-st
    print('Total execution time of GettingDataFromPics.py is:',getDataFromPics_time,'seconds')
    return getDataFromPics_time

#getDataFromPics('wefw')