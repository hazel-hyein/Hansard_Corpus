"""
Acquire search results from the British Newspaper Archive website.
In particular, extract the URL, published date, newspaper name, and county for each search result.
"""

__date__ = "2024-09-07"
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
import pandas as pd


def get_search_result_data(driver):
    results = []

    # Find all search result containers (assuming they are in "bna-card__content")
    search_results = driver.find_elements(By.CSS_SELECTOR, ".bna-card__content")

    for result in search_results:
        try:
            # Extract the URL from the search result
            link_element = result.find_element(By.CSS_SELECTOR, "h4.bna-card__title a")
            result_url = link_element.get_attribute("href")

            # Extract the metadata: Published Date, Newspaper, County
            published_date = (
                result.find_element(
                    By.CSS_SELECTOR, ".bna-card__meta span:nth-of-type(1)"
                )
                .text.replace("Published:", "")
                .strip()
            )
            newspaper_name = result.find_element(
                By.CSS_SELECTOR, ".bna-card__meta span:nth-of-type(2) a"
            ).text.strip()
            county = (
                result.find_element(
                    By.CSS_SELECTOR, ".bna-card__meta span:nth-of-type(3)"
                )
                .text.replace("County:", "")
                .strip()
            )

            # Store the extracted data
            result_data = {
                "url": result_url,
                "published_date": published_date,
                "newspaper_name": newspaper_name,
                "county": county,
            }
            results.append(result_data)

        except Exception as e:
            print(f"An error occurred while extracting metadata for a result: {str(e)}")
            continue

    return results


def get_all_search_results(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Install the correct version of ChromeDriver
    chromedriver_autoinstaller.install()

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    all_results = []

    try:
        # Navigate to the search results page
        driver.get(url)
        print("Navigated to search results page")

        # Handle cookie consent or overlay if present
        try:
            cookie_consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_consent_button.click()  # Click the "That's fine" button
            print("Cookie consent dismissed")
        except Exception as e:
            print(f"No cookie consent overlay found or error: {str(e)}")

        # Extract data from the first page
        results = get_search_result_data(driver)
        all_results.extend(results)

        # Handle pagination
        while True:
            try:
                # Find and click the 'Next' button (pagination-next is the forward arrow '&#187;')
                next_button = driver.find_element(
                    By.CSS_SELECTOR, "a[title='Forward one page']"
                )

                # # Scroll to the "Next" button to ensure it is visible
                # driver.execute_script("arguments[0].scrollIntoView(true);", next_button)

                next_button.click()
                print("Clicked next page")

                # Wait for new search results to load
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "bna-card__content"))
                )

                # Extract data from the next page
                results = get_search_result_data(driver)
                all_results.extend(results)

            except Exception as e:
                print("No more pages found or an error occurred:", e)
                break

    finally:
        driver.quit()

    return all_results


# Usage
url = "https://www.britishnewspaperarchive.co.uk/search/results/1849-01-01/1853-01-01?AccessType=Free+To+View&FreeSearch=great+exhibition&PhraseSearch=&SomeSearch=&AnySearch=&NotSearch=&SortOrder=score&FrontPage=&Region=&County=&Place=&NewspaperTitle=&PublicTag=&IssueId=&ContentType=#"
search_result_data = get_all_search_results(url)


# %% --------------------------------------------------------------------------
# Store as dataframe
df = pd.DataFrame(search_result_data)
df.to_csv("British_Archive/search_results.csv", index=False)


# %%
