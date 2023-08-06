from typing import List

import requests
from bs4 import BeautifulSoup

def data_extraction():
    try:
        content = requests.get('http://bmkg.go.id') #scrape from bmkg website
    except Exception:
        return None

    if content.status_code == 200: # Check if website status OK/200
        soup = BeautifulSoup(content.text, 'html.parser')
        result = soup.find('span', {'class': 'waktu'})
        result = result.text.split(', ')
        date_eq = result[0]
        time_eq = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo_eq = None
        ls = None
        bt = None
        location_place_eq = None
        location_eq = None
        depth_eq = None

        for res in result:
            if i == 1:
                magnitudo_eq = res.text
            elif i == 2:
                depth_eq = res.text
            elif i == 3:
                location_eq = res.text.split(' - ')
                ls = location_eq[0]
                bt = location_eq[1]
            elif i == 4:
                location_place_eq = res.text
            i = i +1

        scrape_result = dict()
        scrape_result['date_eq'] = date_eq #Date of earth quake
        scrape_result['time_eq'] = time_eq #Time of earth quake
        scrape_result['magnitudo_eq'] = magnitudo_eq #Magnitudo of earth quake
        scrape_result['location_place_eq'] = location_place_eq #Location of earth quake
        scrape_result['location_eq'] = {'ls': ls, 'bt': bt} #Coordinate of earth quake
        scrape_result['depth_eq'] = depth_eq # Depth of earth quake
        return scrape_result
    else:
        return None

def show_data(result):
    if result is None:
        print("Can not find earth quake data, plese check target url")
        return
    print('Latest Earth Quake')
    print(f"Date : {result['date_eq']}")
    print(f"Time : {result['time_eq']}")
    print(f"Magnitudo : {result['magnitudo_eq']}")
    print(f"Epicentrum : {result['location_place_eq']}")
    print(f"Coordinate : {result['location_eq']['ls']}, {result['location_eq']['bt']}")
    print(f"Depth : {result['depth_eq']}")
    return result

if __name__ == '__main__':
    result = data_extraction()
    show_data(result)
