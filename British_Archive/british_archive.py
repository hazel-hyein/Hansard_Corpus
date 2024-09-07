"""
Capture OCR text from British Newspaper Archive search results
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
import chromedriver_autoinstaller


def login_to_bna(driver, email, password):
    try:
        # Navigate to login page
        driver.get("https://www.britishnewspaperarchive.co.uk/account/login")
        print("Navigated to login page")

        # Wait for the Username field to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "Username"))
        )

        # Handle cookie consent or overlay if present
        try:
            cookie_consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_consent_button.click()  # Click the "That's fine" button
            print("Cookie consent dismissed")
        except Exception as e:
            print(f"No cookie consent overlay found or error: {str(e)}")

        # Enter email and password
        email_input = driver.find_element(By.ID, "Username")
        password_input = driver.find_element(By.ID, "Password")

        email_input.send_keys(email)
        print("Entered email")

        password_input.send_keys(password)
        print("Entered password")

        # Optionally handle "Remember Me" checkbox if needed
        remember_me_checkbox = driver.find_element(By.ID, "RememberMe")
        remember_me_checkbox.click()  # Check the "Remember Me" checkbox

        # Submit the form
        sign_in_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "login-form-log-in"))
        )
        sign_in_button.click()
        print("Login button clicked, waiting for redirection...")

        # Wait for a redirection after login
        WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))
        print(f"Redirected to: {driver.current_url}")

        print("Login successful")

    except Exception as e:
        print(f"An error occurred during login: {str(e)}")


def select_article_by_keyword(driver, keyword):
    try:
        # Wait for the list of articles to be present
        article_list = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#allItems a"))
        )
        print(f"Found {len(article_list)} articles")

        # Loop through the articles and find one containing the keyword
        for article in article_list:
            article_title = article.text
            if keyword.lower() in article_title.lower():
                print(f"Article found with keyword '{keyword}': {article_title}")
                article.click()
                return article_title

        print(f"No article found containing the keyword '{keyword}'")
        return False

    except Exception as e:
        print(f"An error occurred while selecting an article: {str(e)}")
        return False


def extract_article_text(url, email, password, keyword="exhibition"):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Comment this out for debugging
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    chromedriver_autoinstaller.install()  # Install the correct version of ChromeDriver

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"Chrome version: {driver.capabilities['browserVersion']}")
        print(
            f"ChromeDriver version: {driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}"
        )

        # Log in to the British Newspaper Archive
        login_to_bna(driver, email, password)

        # Navigate to the article page
        driver.get(url)
        print("Navigated to article page")

        # Select the article containing the keyword
        article_title = select_article_by_keyword(driver, keyword)
        if not article_title:
            return None

        # Wait for the "Show Article Text" button to be clickable and click it
        show_article_text_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "copyOcr"))
        )
        show_article_text_button.click()
        print("Clicked 'Show Article Text' button")

        # Wait for the OCR text to appear
        ocr_text = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "ocr"))
        )

        # Extract the text from the OCR div
        article_text = ocr_text.text

        return article_title, article_text

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

    finally:
        driver.quit()


# TODO: Change script to run for a series of URLs and merge into a single dataframe
# Usage
url = "https://www.britishnewspaperarchive.co.uk/viewer/bl/0000252/18510426/052/0006"
email = ## YOUR EMAIL HERE ##
password = ## YOUR PASSWORD HERE ##
article_title, article_text = extract_article_text(url, email, password)
print(article_text if article_text else "Failed to extract article text")


# %%
# create and save to json
import json

data = {
    "article_title": article_title,
    "article_text": article_text,
}

with open("article_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Data saved to 'article_data.json'")


# %%
