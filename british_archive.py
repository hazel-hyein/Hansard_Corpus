"""
Enter script name

Enter short description of the script
"""

__date__ = "2024-09-06"
__author__ = "NedeeshaWeerasuriya"
__version__ = "0.1"



# %% --------------------------------------------------------------------------
# Import Modules

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import chromedriver_autoinstaller




def extract_newspaper_text(url):
    # Set up Chrome options
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)

    chromedriver_autoinstaller.install(True)  

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Print Chrome and ChromeDriver versions for debugging
        print(f"Chrome version: {driver.capabilities['browserVersion']}")
        print(f"ChromeDriver version: {driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}")

        # Navigate to the page
        driver.get(url)

        # Wait for the content to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bna-page-div"))
        )

        # Allow some time for JavaScript to fully render the page
        time.sleep(5)

        # Find and click the "Show Article Text" button
        show_article_text_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "copyOcr"))
        )
        show_article_text_button.click()

        # Wait for the OCR text to load in the popup
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ocr"))
        )

        # Extract the text from the OCR div
        ocr_div = driver.find_element(By.ID, "ocr")
        article_text = ocr_div.text

        return article_text

    except Exception as e:
        return f"An error occurred: {str(e)}"

    finally:
        driver.quit()

# Usage
url = "https://www.britishnewspaperarchive.co.uk/viewer/bl/0000252/18510426/052/0006"
newspaper_text = extract_newspaper_text(url)
print(newspaper_text)
# %%
