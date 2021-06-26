import json
import re
import requests

from bs4 import BeautifulSoup

# site address that we will parse
URL = 'https://cofix.by/cafe/'

response = requests.get(URL)

# get the page
soup = BeautifulSoup(response.content, 'html.parser')

# find all div tags
items = soup.findAll('div', class_ ='show_table')[0]

# information about the cafe is in the list, we find all the tags li
items_li = items.findAll('li')

# function to get the coordinates of the cafe by their id
def get_coordinates(full_id):

    id = full_id.split('_')[2]
    url = f'https://cofix.by/cafe/map.php?baloon={id}'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    texts = soup.findAll('script', type='text/javascript')

    for text in texts:
        
        result = re.findall(r'ymaps.Placemark.[\(,\[]\d*.?\d*\,\d*.?\d*]', str(text.string))

        if not len(result):
            continue

        result = re.findall(r'\d*.?\d*\,\d*.?\d*', result[0])

        latitude = float(result[0].split(',')[0])
        longitude = float(result[0].split(',')[1])
    
        return latitude, longitude
        
# variable for storing information
data = {}

# collecting information
for item in items_li:

    info = item.get_text(strip=True)
    split_info = info.split('Режим работы')

    adress = split_info[0][0:5] +' '+ split_info[0][5:] 

    phone_number = re.findall(r'.?\d{3}\s{1}\d{2}\s{1}\d{3}\s{1}\d{2}\s{1}\d{2}', split_info[1])[0]
    id = item.attrs['id']
    latitude, longitude = get_coordinates(id)

    data[id] = {

        'phone nomber' : phone_number,
        'adress' : adress,
        'latitude' : latitude,
        'longitude' : longitude,
    }

# save everything in list.json
with open("list.json", "w", encoding="utf-8") as file:
    json.dump(data, file)