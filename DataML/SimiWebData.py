import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
import os


def simiWebData(url):
    st=time.time()
    print('Started executing SimiWebData.py')
    try:
        # Replace the path below with the path to your new chromedriver.exe file
        driver_path = 'DigiScore\\DataML\\chromedriver.exe'
        # Create a new instance of the Chrome options
        options = Options()

        # Add the headless argument
        options.add_argument('--headless')
        # Disable the AutomationControlled feature
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Set the user agent to a regular browser user agent
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service,options=options)

        parsed_url = urlparse(url)
        companyName = parsed_url.netloc.replace("www.", "")
        last_part = parsed_url.path.split("/")[-1]

        print(companyName)
        print(last_part)
        # Set the window size to desired size :1920x1080
        driver.set_window_size(1440, 720)

        urlScrape=f'https://www.similarweb.com/website/{companyName}/#overview'

        driver.get(urlScrape)
        # Wait for the page to load
        time.sleep(7)
        # Check if the current url contains 'search/?q'
        if 'search/' in driver.current_url:
            raise ValueError("Company not found or something went wrong")
        else:

            # Scroll the page down by 500 pixels
            driver.execute_script('window.scrollBy(0, 350)')

            # Specify the path where you want to save the screenshots
            path = os.path.join(os.getcwd(), 'DigiScore', 'DataML', 'Pics')

            # Create the directory if it doesn't exist
            if not os.path.exists(path):
                os.makedirs(path)

            # Generate a unique filename for the screenshot
            filename = f"screenshot_{len(os.listdir(path)) + 1}.png"

            # Combine the path and filename
            screenshot_path = os.path.join(path, filename)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            # Print the current directory to see where the file was saved
            print(os.getcwd())

            et=time.time()
            simiWebData_time=et-st
            print('Total execution time of SimiWebData.py is:',simiWebData_time,'seconds')
            # Close the browser window
            return simiWebData_time
    except ValueError as e:
        print(f"Invalid search URL at at :'https://www.similarweb.com/website/{companyName}/#overview': {e}")
        print(e)
        print('The companyName variable you are searching is wrong')
        et=time.time()
        simiWebData_time=et-st
        print('Total execution time of SimiWebData.py is:',simiWebData_time,'seconds')
        return simiWebData_time
    except Exception as e:
        print(f"An Error occured: {e}")
        print("Take a careful look at the problem of SimiWebData.py file")
        et=time.time()
        simiWebData_time=et-st
        print('Total execution time of SimiWebData.py is:',simiWebData_time,'seconds')
        return simiWebData_time
    finally:
        driver.quit()

#simiWebData("hhttps://www.similarweb.com/website/esg.fr/#overview")