

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

# %% --------------------------------------------------------------------------
# Fetch Hansard Commons URLs
# -----------------------------------------------------------------------------

BASE_URL = 'https://api.parliament.uk/historic-hansard/commons'

month_list = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
date_list = [str(i).zfill(2) for i in range(1,32)]

#def fetch_hansard_urls(start_year, end_year):
urls = []
start_year = 1851
end_year = 1860
start_month = 1
end_month = 12
title_list = []
content_dict = {}

for year in range(start_year, end_year + 1):
    for month in month_list[int(start_month)-1:int(end_month)]:
        for date in date_list:
            try:
                specific_date = f"{year}/{month}/{date}"
                url = f"{BASE_URL}/{year}/{month}/{date}.js"
                response = requests.get(url)
            except:
                continue
            if response.status_code == 200:
                    data = response.json()
                    for sec in data[0]['house_of_commons_sitting']['top_level_sections']:
                        title_list.append(sec['section']['slug'])
                    for title in title_list:
                        title_url = url[0:-3] + '/' + title
                        content_response = requests.get(title_url)
                        soup = BeautifulSoup(content_response.content, 'html.parser')
                        text = soup.get_text(strip=True)
                        content_dict[specific_date] = {title: text}
            print(year,date,month,'is completed')


# %%

# %% --------------------------------------------------------------------------
# Save to csv
# -----------------------------------------------------------------------------
import csv

with open('Commons_1850.csv', 'w', newline='', encoding = 'utf-8') as f:
     writer = csv.writer(f)
     writer.writerow(['Date', "Title", 'Content'])
     for year in range(start_year, end_year + 1):
          for month in month_list[int(start_month)-1:int(end_month)]:
               for date in date_list:
                    specific_date = f"{year}/{month}/{date}"
                    if specific_date in content_dict:
                        for title, text in content_dict[specific_date].items(): 
                            writer.writerow([specific_date, title ,text])
# %%

"""
Enter script name

Enter short description of the script
"""

__date__ = "2024-07-01"
__author__ = "HyeinKim"
__version__ = "0.1"



# %% --------------------------------------------------------------------------
# Import Modules
import requests
from bs4 import BeautifulSoup
import csv
# -----------------------------------------------------------------------------

# %% --------------------------------------------------------------------------
# Fetch Hansard Lords URLs
# -----------------------------------------------------------------------------
BASE_URL = 'https://api.parliament.uk/historic-hansard/lords'

month_list = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
date_list = [str(i).zfill(2) for i in range(1,32)]

#def fetch_hansard_urls(start_year, end_year):
urls = []
start_year = 1850
end_year = 1850
start_month = 1
end_month = 12
title_list = []
content_dict = {}

for year in range(start_year, end_year + 1):
    for month in month_list[int(start_month)-1:int(end_month)]:
        for date in date_list:
            try:
                specific_date = f"{year}/{month}/{date}"
                url = f"{BASE_URL}/{year}/{month}/{date}.js"
                response = requests.get(url)
            except:
                continue
            if response.status_code == 200:
                    data = response.json()
                    for sec in data[0]['house_of_lords_sitting']['top_level_sections']:
                        title_list.append(sec['section']['slug'])
                    for title in title_list:
                        title_url = url[0:-3] + '/' + title
                        content_response = requests.get(title_url)
                        soup = BeautifulSoup(content_response.content, 'html.parser')
                        text = soup.get_text(strip=True)
                        content_dict[specific_date] = {title: text}
            print(year,month,date,'is completed')



# %% --------------------------------------------------------------------------
# Save to csv
# -----------------------------------------------------------------------------
import csv

with open('Lords_1850.csv', 'w', newline='', encoding = 'utf-8') as f:
     writer = csv.writer(f)
     writer.writerow(['Date', "Title", 'Content'])
     for year in range(start_year, end_year + 1):
          for month in month_list[int(start_month)-1:int(end_month)]:
               for date in date_list:
                    specific_date = f"{year}/{month}/{date}"
                    if specific_date in content_dict:
                        for title, text in content_dict[specific_date].items(): 
                            writer.writerow([specific_date, title ,text])
# %%
