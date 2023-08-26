#https://chromedriver.chromium.org/downloads
#https://googlechromelabs.github.io/chrome-for-testing/
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import os
import platform
from selenium.common.exceptions import TimeoutException

'''
import requests
import os
import shutil
import zipfile
def update_chromedriver():
    # Define the base URL for fetching the latest ChromeDriver version
    base_url = "https://commondatastorage.googleapis.com/chrome-infra/chromedriver"

    # Fetch the latest version of ChromeDriver
    latest_version = requests.get(f"{base_url}/LATEST_RELEASE").text.strip()

    # Define URLs for downloading ChromeDriver for Windows and Linux
    win_url = f"{base_url}/{latest_version}/chromedriver_win32.zip"
    linux_url = f"{base_url}/{latest_version}/chromedriver_linux64.zip"

    # Define paths where you want to save the downloaded zipped binaries
    win_dest = "chromedriver_win32.zip"
    linux_dest = "chromedriver_linux64.zip"

    # Download the binaries
    try:
        shutil.copyfileobj(requests.get(win_url, stream=True).raw, open(win_dest, 'wb'))
        shutil.copyfileobj(requests.get(linux_url, stream=True).raw, open(linux_dest, 'wb'))
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return

    # Check if the files are valid zip files
    if not zipfile.is_zipfile(win_dest):
        raise Exception("File chromedriver_win32.zip is not a valid zip file")
    if not zipfile.is_zipfile(linux_dest):
        raise Exception("File chromedriver_linux64.zip is not a valid zip file")

    # Extract the Windows ChromeDriver
    with zipfile.ZipFile(win_dest, 'r') as zip_ref:
        zip_ref.extractall("DataML")

    # Rename the chromedriver to chromedriver.exe for clarity (Windows)
    os.rename(os.path.join("DataML", "chromedriver"), os.path.join("DataML", "chromedriver.exe"))

    # Extract the Linux ChromeDriver
    with zipfile.ZipFile(linux_dest, 'r') as zip_ref:
        zip_ref.extractall("DataML")

    # Remove the zip files after extraction
    os.remove(win_dest)
    os.remove(linux_dest)

    print(f"Updated ChromeDriver to version {latest_version}")

update_chromedriver()
'''


def simiWebData(url):
    st=time.time()
    time.sleep(7)
    #return 0
    print('Started executing SimiWebData.py')
    driver=None
    companyName=None
    try:
        # Replace the path below with the path to your new chromedriver.exe file

        #driver_path = 'DigiScore\\DataML\\chromedriver.exe'
        #driver_path = 'DataML\\chromedriver.exe'

        # Detect the operating system
        os_type = platform.system()
        print(os_type)

        # Set the driver path according to the OS
        if os_type == "Windows":
            driver_path = os.path.join('DataML', 'chromedriver.exe')
            service_log_path = os.path.join('DataML', 'chromedriver.log')
        elif os_type == "Linux":
            driver_path = os.path.join('DataML', 'chromedriver')  # Adjust this if your path is different in Linux
            service_log_path = "/home/ubuntu/DigiScore/DataML/chromedriver.log"
            service = Service(driver_path, log_path=service_log_path)

        else:
            raise Exception("Unsupported OS")

        print(f"Using driver at path: {driver_path}")

        # Create a new instance of the Chrome options
        options = Options()

        # Add the headless argument
        options.add_argument('--headless')
        # Disable the AutomationControlled feature
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Set the user agent to a regular browser user agent
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

        # Create service object
        if os_type == "Linux":
            service = Service(driver_path, log_path=service_log_path)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--headless')
            # Disable the AutomationControlled feature
            options.add_argument('--disable-blink-features=AutomationControlled')
            # Set the user agent to a regular browser user agent
            options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.22 Safari/537.36')
            options.add_argument('--incognito')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-webgl')
            options.add_argument('--disable-extensions')
            options.add_argument('Referer: https://www.google.com/')
        else:
            service = Service(driver_path)

        try:
            #service = Service(driver_path)
            driver = webdriver.Chrome(service=service,options=options)
            print("Webdriver initialized successfully")
        except Exception as e:
            print(f"Error initializing webdriver: {e}")
            raise e

        parsed_url = urlparse(url)
        companyName = parsed_url.netloc.replace("www.", "")
        last_part = parsed_url.path.split("/")[-1]

        print(companyName)
        print(last_part)
        # Set the window size to desired size :1920x1080
        driver.set_window_size(1920, 1080)

        urlScrape=f'https://www.similarweb.com/website/{companyName}/#overview'

        driver.get(urlScrape)
        print("Website loaded")
        print("Before time.sleep")
        # Wait for the page to load
        time.sleep(7)
        print("After time.sleep")
        # Check if the current url contains 'search/?q'
        if 'search/' in driver.current_url:
            print('Company not found or something went wrong')
            raise ValueError("Company not found or something went wrong")
        else:
            print('Things look good')
            # Scroll the page down by 500 pixels
            ###driver.execute_script('window.scrollBy(0, 350)')
            # Scroll to the specified location using 100dvh
            #driver.execute_script("window.scrollTo(0, (document.documentElement.scrollHeight - document.documentElement.clientHeight) * 0.01 * 100)")

            # Accept Cookies Button
            wait = WebDriverWait(driver, 10)
            try:
                accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
                print("Accept button found and is clickable!")
            except TimeoutException:
                print("Accept button either not found or not clickable.")
                raise ValueError("Accept button not found or not clickable within the wait time.")

            # Click the "Accept All Cookies" button
            try:
                accept_button.click()
                print("Cookies accepted.")
            except Exception as e:
                print(f"Error accepting cookies: {e}")

            driver.execute_script('window.scrollBy(0, 500)') # 480
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")

            # Specify the path where you want to save the screenshots
            #pathscr = os.path.join(os.getcwd(), 'DigiScore', 'DataML', 'Pics')
            pathscr = os.path.join(os.getcwd(), 'DataML', 'Pics')

            # Create the directory if it doesn't exist
            if not os.path.exists(pathscr):
                os.makedirs(pathscr)

            # Generate a unique filename for the screenshot
                #filename = f"screenshot_{len(os.listdir(path)) + 1}.png"
            filename = f'{companyName}'
            str(filename)
            filename = filename.replace(".",'_')
            filename = filename + '.png'
            print(filename)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            # Print the current directory to see where the file was saved
            print(os.getcwd())

            time.sleep(0.5)
            driver.execute_script('window.scrollBy(0, 6275)') #competitors 6772           6292           6325 for small
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")

            # Generate a unique filename for the screenshot
            #filename = f"screenshotComp_{len(os.listdir(path)) + companyName + 'Competitors' }.png"
            filename1 = f'{companyName}'
            str(filename1)
            filename = filename1.replace(".",'_')
            filename1 = filename1 + '_Competitors.png'
            print(filename1)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename1)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            # Print the current directory to see where the file was saved
            print(os.getcwd())

            time.sleep(0.5)
            driver.execute_script("window.scrollBy(0, 1718)") #marketingChannelDistrib 8470       1698          1668 for small
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")
            filename1 = f'{companyName}'
            str(filename1)
            filename = filename1.replace(".",'_')
            filename1 = filename1 + '_channelDistrib.png'
            print(filename1)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename1)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            # Print the current directory to see where the file was saved
            print(os.getcwd())

            time.sleep(0.5)
            driver.execute_script("window.scrollBy(0, 650)") #keywords 9150      680         650 for small
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")

            filename1 = f'{companyName}'
            str(filename1)
            filename = filename1.replace(".",'_')
            filename1 = filename1 + '_Keywords.png'
            print(filename1)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename1)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

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

    except WebDriverException as e:
        if 'session not created' in str(e):
            print(f"Browser or driver version issue: {e}")
            print("Please check your browser or driver version.")
            et=time.time()
            simiWebData_time=et-st
            print('Total execution time of SimiWebData.py is:',simiWebData_time,'seconds')
            error_message = "Browser or driver version issue. Please check your browser or driver version. It seems the ChromeDriver needs updating."
            print(error_message)
            return -999  # error code for version mismatch

        else:
            error_message = f"An unexpected WebDriverException occurred: {e}"
            return error_message

    except Exception as e:
        print(f"An Error occured: {e}")
        print("Take a careful look at the problem of SimiWebData.py file")
        '''et=time.time()
        simiWebData_time=et-st
        print('Total execution time of SimiWebData.py is:',simiWebData_time,'seconds')
        return simiWebData_time'''
        error_message = f"An unexpected error occurred: {e}"
        return error_message
    finally:
        if driver:
            driver.quit()


#simiWebData("https://www.esg.fr/")
#simiWebData("https://www.junto.fr/")
#simiWebData("https://www.iscid-co.fr/")
#simiWebData("https://www.adcreative.ai/")
#simiWebData("https://www.ads-up.fr/")
#simiWebData("https://www.icd-ecoles.com/")



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################



def simiWebDataCompetitor(competitorURL,competitor_num):
    st=time.time()
    #return 0
    print('Started executing SimiWebDataCompetitor.py')
    driver=None
    companyName=None
    try:
        # Replace the path below with the path to your new chromedriver.exe file

        #driver_path = 'DigiScore\\DataML\\chromedriver.exe'
        #driver_path = 'DataML\\chromedriver.exe'
        # Detect the operating system
        os_type = platform.system()
        print(os_type)

        # Set the driver path according to the OS
        if os_type == "Windows":
            driver_path = os.path.join('DataML', 'chromedriver.exe')
            service_log_path = os.path.join('DataML', 'chromedriver.log')
        elif os_type == "Linux":
            driver_path = os.path.join('DataML', 'chromedriver')  # Adjust this if your path is different in Linux
            service_log_path = "/home/ubuntu/DigiScore/DataML/chromedriver.log"
            service = Service(driver_path, log_path=service_log_path)

        else:
            raise Exception("Unsupported OS")

        print(f"Using driver at path: {driver_path}")

        # Create a new instance of the Chrome options
        options = Options()

        # Add the headless argument
        options.add_argument('--headless')
        # Disable the AutomationControlled feature
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Set the user agent to a regular browser user agent
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36')

        # Create service object
        if os_type == "Linux":
            service = Service(driver_path, log_path=service_log_path)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument('--headless')
            # Disable the AutomationControlled feature
            options.add_argument('--disable-blink-features=AutomationControlled')
            # Set the user agent to a regular browser user agent
            options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.22 Safari/537.36')
            options.add_argument('--incognito')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-webgl')
            options.add_argument('--disable-extensions')
            options.add_argument('Referer: https://www.google.com/')
        else:
            service = Service(driver_path)

        try:
            #service = Service(driver_path)
            driver = webdriver.Chrome(service=service,options=options)
            print("Webdriver initialized successfully")
        except Exception as e:
            print(f"Error initializing webdriver: {e}")
            raise e

        parsed_url = urlparse(competitorURL)
        companyName = parsed_url.netloc.replace("www.", "")
        last_part = parsed_url.path.split("/")[-1]

        print(companyName)
        print(last_part)
        # Set the window size to desired size :1920x1080
        driver.set_window_size(1920, 1080)

        urlScrape=f'https://www.similarweb.com/website/{companyName}/#overview'

        driver.get(urlScrape)
        print("Website loaded")
        print("Before time.sleep")
        # Wait for the page to load
        time.sleep(7)
        print("After time.sleep")
        # Check if the current url contains 'search/?q'
        if 'search/' in driver.current_url:
            print('Company not found or something went wrong')
            raise ValueError("Company not found or something went wrong")
        else:
            print('Things look good')
            # Scroll the page down by 500 pixels
            ###driver.execute_script('window.scrollBy(0, 350)')
            # Scroll to the specified location using 100dvh
            #driver.execute_script("window.scrollTo(0, (document.documentElement.scrollHeight - document.documentElement.clientHeight) * 0.01 * 100)")

            # Accept Cookies Button
            wait = WebDriverWait(driver, 10)
            try:
                accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
                print("Accept button found and is clickable!")
            except TimeoutException:
                print("Accept button either not found or not clickable.")
                raise ValueError("Accept button not found or not clickable within the wait time.")

            # Click the "Accept All Cookies" button
            try:
                accept_button.click()
                print("Cookies accepted.")
            except Exception as e:
                print(f"Error accepting cookies: {e}")

            driver.execute_script('window.scrollBy(0, 500)') # 480
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")

            # Specify the path where you want to save the screenshots
            #pathscr = os.path.join(os.getcwd(), 'DigiScore', 'Competitors', 'Competitor_{}'.format(competitor_num))
            pathscr = os.path.join(os.getcwd(), 'DataML', 'Competitors', 'Competitor_{}'.format(competitor_num))

            # Create the directory if it doesn't exist
            if not os.path.exists(pathscr):
                os.makedirs(pathscr)

            # Generate a unique filename for the screenshot
                #filename = f"screenshot_{len(os.listdir(path)) + 1}.png"
            filename = f'{companyName}'
            str(filename)
            filename = filename.replace(".",'_')
            filename = filename + '.png'
            print(filename)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            # Print the current directory to see where the file was saved
            print(os.getcwd())

            time.sleep(0.5)
            driver.execute_script('window.scrollBy(0, 6280)') #competitors 6772           6292         6325
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")

            driver.execute_script("window.scrollBy(0, 1713)") #marketingChannelDistrib 8470       1698        1668
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")
            filename1 = f'{companyName}'
            str(filename1)
            filename = filename1.replace(".",'_')
            filename1 = filename1 + '_channelDistrib.png'
            print(filename1)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename1)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            # Print the current directory to see where the file was saved
            print(os.getcwd())

            time.sleep(0.5)
            driver.execute_script("window.scrollBy(0, 650)") #keywords 9150      680
            driver.execute_script("document.body.style.zoom='140%'")
            driver.execute_script("window.devicePixelRatio = 2")

            filename1 = f'{companyName}'
            str(filename1)
            filename = filename1.replace(".",'_')
            filename1 = filename1 + '_Keywords.png'
            print(filename1)

            # Combine the path and filename
            screenshot_path = os.path.join(pathscr, filename1)

            # Take a screenshot and save it to the specified location
            driver.save_screenshot(screenshot_path)

            et=time.time()
            simiWebDataCompetitor_time=et-st
            print('Total execution time of SimiWebDataCompetitors.py is:',simiWebDataCompetitor_time,'seconds')
            # Close the browser window
            return simiWebDataCompetitor_time


    except ValueError as e:
        print(f"Invalid search URL at at :'https://www.similarweb.com/website/{companyName}/#overview': {e}")
        print(e)
        print('The companyName variable you are searching is wrong')
        et=time.time()
        simiWebDataCompetitor_time=et-st
        print('Total execution time of SimiWebDataCompetitor.py is:',simiWebDataCompetitor_time,'seconds')
        return simiWebDataCompetitor_time

    except WebDriverException as e:
        if 'session not created' in str(e):
            print(f"Browser or driver version issue: {e}")
            print("Please check your browser or driver version.")
            et=time.time()
            simiWebDataCompetitor_time=et-st
            print('Total execution time of SimiWebDataCompetitor.py is:',simiWebDataCompetitor_time,'seconds')
            error_message = "Browser or driver version issue. Please check your browser or driver version. It seems the ChromeDriver needs updating."
            return error_message
        else:
            error_message = f"An unexpected WebDriverException occurred: {e}"
            return error_message

    except Exception as e:
        print(f"An Error occured: {e}")
        print("Take a careful look at the problem of SimiWebDataCompetitors.py file")
        '''et=time.time()
        simiWebData_time=et-st
        print('Total execution time of SimiWebDataCompetitor.py is:',simiWebData_time,'seconds')
        return simiWebData_time'''
        error_message = f"An unexpected error occurred: {e}"
        return error_message
    finally:
        if driver:
            driver.quit()

#simiWebDataCompetitor("https://www.esg.fr/",1)
#simiWebDataCompetitor("https://www.junto.fr/")
#simiWebDataCompetitor("https://www.iscid-co.fr/",1)
#simiWebDataCompetitor("https://www.adcreative.ai/",1)
#simiWebDataCompetitor("https://www.ads-up.fr/")