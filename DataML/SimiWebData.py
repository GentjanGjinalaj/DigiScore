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


def simiWebData(url):
    st=time.time()
    #return 0
    print('Started executing SimiWebData.py')
    driverr=None
    companyName=None
    try:
        # Replace the path below with the path to your new chromedriver.exe file

        #driver_path = 'DigiScore\\DataML\\chromedriver.exe'
        driver_path = 'DataML\\chromedriver.exe'
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
        driver.set_window_size(1920, 1080)

        urlScrape=f'https://www.similarweb.com/website/{companyName}/#overview'

        driver.get(urlScrape)
        # Wait for the page to load
        time.sleep(7)
        # Check if the current url contains 'search/?q'
        if 'search/' in driver.current_url:
            raise ValueError("Company not found or something went wrong")
        else:

            # Scroll the page down by 500 pixels
            ###driver.execute_script('window.scrollBy(0, 350)')
            # Scroll to the specified location using 100dvh
            #driver.execute_script("window.scrollTo(0, (document.documentElement.scrollHeight - document.documentElement.clientHeight) * 0.01 * 100)")

            # Accept Cookies Button
            wait = WebDriverWait(driver, 1)
            accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            # Click the "Accept All Cookies" button
            accept_button.click()


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
            driver.execute_script('window.scrollBy(0, 6280)') #competitors 6772           6292           6325 for small
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
            driver.execute_script("window.scrollBy(0, 1713)") #marketingChannelDistrib 8470       1698          1668 for small
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
            return error_message
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



##########################################################################################################################################
#COMPETITORS FUNCTION
##########################################################################################################################################



def simiWebDataCompetitor(competitorURL,competitor_num):
    st=time.time()
    #return 0
    print('Started executing SimiWebDataCompetitor.py')
    driverr=None
    companyName=None
    try:
        # Replace the path below with the path to your new chromedriver.exe file

        #driver_path = 'DigiScore\\DataML\\chromedriver.exe'
        driver_path = 'DataML\\chromedriver.exe'
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

        parsed_url = urlparse(competitorURL)
        companyName = parsed_url.netloc.replace("www.", "")
        last_part = parsed_url.path.split("/")[-1]

        print(companyName)
        print(last_part)
        # Set the window size to desired size :1920x1080
        driver.set_window_size(1920, 1080)

        urlScrape=f'https://www.similarweb.com/website/{companyName}/#overview'

        driver.get(urlScrape)
        # Wait for the page to load
        time.sleep(7)
        # Check if the current url contains 'search/?q'
        if 'search/' in driver.current_url:
            raise ValueError("Company not found or something went wrong")
        else:

            # Scroll the page down by 500 pixels
            ###driver.execute_script('window.scrollBy(0, 350)')
            # Scroll to the specified location using 100dvh
            #driver.execute_script("window.scrollTo(0, (document.documentElement.scrollHeight - document.documentElement.clientHeight) * 0.01 * 100)")

            # Accept Cookies Button
            wait = WebDriverWait(driver, 1)
            accept_button = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            # Click the "Accept All Cookies" button
            accept_button.click()

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