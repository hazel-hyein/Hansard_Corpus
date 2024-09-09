"""
Capture OCR text from British Newspaper Archive search results
"""

__date__ = "2024-09-06"
__author__ = "NedeeshaWeerasuriya"
__version__ = "0.1"


# %% --------------------------------------------------------------------------
# Import Modules
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller


def login_to_bna(driver: webdriver.Chrome, email: str, password: str) -> None:
    """
    Log in to the British Newspaper Archive website.

    Args:
        driver: The Selenium WebDriver instance
        email: The email address for the account
        password: The password for the account
    """
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


def select_article_by_keyword(driver: webdriver.Chrome, keyword: str) -> str:
    """
    Find an article containing the specified keyword and click on it.

    Args:
        driver: The Selenium WebDriver instance
        keyword: The keyword to search for in the article titles

    Returns:
        The title of the article that was clicked, or False if no article was found    
    """
    try:
        # Wait for the list of articles to be present
        article_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#allItems a"))
        )

        # Loop through the articles and find one containing the keyword
        for article in article_list:
            article_title = article.text
            if keyword.lower() in article_title.lower():
                article.click()
                return article_title

        print(f"No article found containing the keyword '{keyword}'")
        return False

    except Exception as e:
        print(f"An error occurred while selecting an article: {str(e)}")
        return False


def extract_article_text(
    df: pd.DataFrame, email: str, password: str, keyword: str = "exhibit"
) -> pd.DataFrame:
    """
    Extract the OCR text from the specified articles in the DataFrame.

    Args:
        df: The DataFrame containing the article URLs
        email: The email address for the British Newspaper Archive account
        password: The password for the British Newspaper Archive account
        keyword: The keyword to search for in the article titles

    Returns:
        A new DataFrame with the extracted article text appended as a new column
    """
    # Set up the Chrome WebDriver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Comment this out for debugging
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chromedriver_autoinstaller.install()  # Install the correct version of ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Extract the URLs from the DataFrame
    url_df = df["url"]
    rows = []

    try:
        print(f"Chrome version: {driver.capabilities['browserVersion']}")
        print(
            f"ChromeDriver version: {driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]}"
        )

        # Log in to the British Newspaper Archive
        login_to_bna(driver, email, password)

        for url in url_df:
            # Navigate to the article page
            driver.get(url)

            # Select the article containing the keyword
            article_title = select_article_by_keyword(driver, keyword)
            if not article_title:
                rows.append({"article_text": None})
                continue

            # wait 3 seconds for the OCR text to load
            time.sleep(2)

            # Wait for the "Show Article Text" button to be clickable and click it
            show_article_text_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, "copyOcr"))
            )
            show_article_text_button.click()
            time.sleep(1)

            # Wait for the OCR text to appear
            ocr_text_div = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "ocr"))
            )
            # Check if the OCR text div contains any text
            ocr_text = ocr_text_div.text
            # Append the article title and text to the rows list
            rows.append({"article_text": ocr_text})

        final_df = df.copy()
        rows_df = pd.DataFrame(rows, index=final_df.index)
        final_df["article_text"] = rows_df["article_text"]
        return final_df

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        final_df = df.copy()
        rows_df = pd.DataFrame(rows, index=final_df.index)
        final_df["article_text"] = rows_df["article_text"]
        return final_df

    finally:
        driver.quit()


# Usage
df = pd.read_csv("British_Archive/search_results.csv")
email = "nedeeshaw@virginmedia.com"
password = ######
extracted_text_df = extract_article_text(
    df[471:1000], email, password
)  # Only 10 rows for testing


# %%
# Save the extracted text to a CSV file
extracted_text_df.to_csv("British_Archive/extracted_text_493.csv", index=False)

# %%
