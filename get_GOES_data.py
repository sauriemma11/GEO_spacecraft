import requests
from bs4 import BeautifulSoup
import os
import time

"""
Script downloads daily (for selected month) netcdf data from noaa.gov website for GOES 17/18
Change year, month, goes number, data product, and local directory
Created by Sarah.Auriemma@noaa.gov 3/2023
"""
############################### User input:

# Data to download:
year = '2022'
month = '11'

# GOES 17 or 18?
goes_number = '17'

# What Data Product do you want?
# Enter: Orbit or Mag
select_data_prod = 'mag'

################################### Do not edit below this line

data_prod_array = ['ephe-l2-orb1m', 'magn-l2-avg1m']
if select_data_prod.lower() == 'mag':
    data_prod = data_prod_array[1]
else:
    data_prod = data_prod_array[0]


# Define the base URL
base_url = 'https://data.ngdc.noaa.gov/platforms/solar-space-observing-satellites/goes/goes'+goes_number+'/l2/data/'+data_prod+'/'+year+'/'+month+'/'
# Define the local download directory
download_dir = 'C:/Users/Sarah/Documents/CIRES Python/wget/GOES/GOES'+goes_number+'/'

#Make sure the download directory exists
download_dir_month = download_dir + year + '/' + month + '/' + data_prod + '/'
# download_dir_month = str(download_dir + year + f'/{month:02}/' + data_prod + '/')
os.makedirs(download_dir_month, exist_ok=True)

# Construct the URL for the current month
url = str(base_url)

# Get the HTML content of the URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all links on the page
links = soup.find_all('a')

#file name:
starts_with_str = str('dn_' + data_prod)

# Iterate over the links and download the files with the specified name
for link in links:
    if link.get('href').startswith(starts_with_str) and link.get('href').endswith('.nc'):
        file_url = url + link.get('href')
        file_path = os.path.join(download_dir_month, link.get('href'))
        file_name = link.get('href').split('/')[-1]
        if os.path.exists(file_path):
            print(f'{file_name} already exists, skipping download')
            continue
        try:
            response = requests.get(file_url)
            with open(file_path, 'wb') as f:
                print(f'Downloading {file_name}...')
                f.write(response.content)
        except requests.exceptions.ConnectionError:
            print(f'Connection error while downloading {file_name}, retrying in 5 seconds...')
            time.sleep(5)
            response = requests.get(file_url)
            with open(file_path, 'wb') as f:
                print(f'Retrying download of {file_name}...')
                f.write(response.content)
