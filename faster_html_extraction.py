"""
Enter script name

Enter short description of the script
"""

__date__ = "2024-06-30"
__author__ = "HyeinKim"
__version__ = "0.1"



# %% --------------------------------------------------------------------------
# Import Modules
# -----------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# %% --------------------------------------------------------------------------
# Faster version of the code
# -----------------------------------------------------------------------------

BASE_URL = 'https://api.parliament.uk/historic-hansard/commons'
month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
date_list = [str(i).zfill(2) for i in range(1, 32)]

start_year = 1861
end_year = 1870
start_month = 1
end_month = 12
content_dict = {}

# Initialize a session
session = requests.Session()

def fetch_data_for_date(year, month, date):
    title_list = []
    specific_date = f"{year}/{month}/{date}"
    url = f"{BASE_URL}/{year}/{month}/{date}.js"
    try:
        response = session.get(url)
        if response.status_code == 200:
            data = response.json()
            for sec in data[0]['house_of_commons_sitting']['top_level_sections']:
                title_list.append(sec['section']['slug'])
            for title in title_list:
                title_url = url[0:-3] + '/' + title
                content_response = session.get(title_url)
                soup = BeautifulSoup(content_response.content, 'html.parser')
                text = soup.get_text(strip=True)
                if specific_date in content_dict:
                    content_dict[specific_date][title] = text
                else:
                    content_dict[specific_date] = {title: text}
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {specific_date}: {e}")
    print(f"{year}, {date}, {month} is completed")

# Use ThreadPoolExecutor to fetch data in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_date = {executor.submit(fetch_data_for_date, year, month, date): (year, month, date)
                      for year in range(start_year, end_year + 1)
                      for month in month_list[int(start_month)-1:int(end_month)]
                      for date in date_list}

    for future in as_completed(future_to_date):
        year, month, date = future_to_date[future]
        try:
            data = future.result()
        except Exception as exc:
            print(f"{year}/{month}/{date} generated an exception: {exc}")


# %% --------------------------------------------------------------------------
# Save to csv
# -----------------------------------------------------------------------------
import csv

with open('Commons_1861-1870.csv', 'w', newline='', encoding = 'utf-8') as f:
     writer = csv.writer(f)
     writer.writerow(['Date', "Title", 'Content'])
     for year in range(start_year, end_year + 1):
          for month in month_list[int(start_month)-1:int(end_month)]:
               for date in date_list:
                    specific_date = f"{year}/{month}/{date}"
                    if specific_date in content_dict:
                        for title, text in content_dict[specific_date].items(): 
                            writer.writerow([specific_date, title ,text])