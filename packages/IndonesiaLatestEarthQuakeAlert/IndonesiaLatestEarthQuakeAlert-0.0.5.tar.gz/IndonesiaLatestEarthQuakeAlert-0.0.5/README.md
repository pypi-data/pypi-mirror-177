# Indonesia-Eartquake-Alert

This package contain latest information of earth quake in Indonesia from two government sources
- bmkg.go.id (Indonesia Meteorological, Climatological, and Geophysical Agency)
- usgs.gov (United States Geological Survey) -- coming soon

This package will use BeautifulSoup4 and Requests to produce output in JSON and it ready to use in web or mobile application

# Requirements
This package needs:
- Python
- BeautifulSoup4

# How To Use
import earthquake_alert

if __name__ == '__main__':
    result = earthquake_alert.data_extraction()
    earthquake_alert.show_data(result)

Version:
0.0.5 Change data source to https://warning.bmkg.go.id
0.0.4 Bug fix
0.0.3 Bug fix
0.0.2 Bug fix
0.0.1 Create new application with data source https://www.bmkg.go.id

Note:
* Maybe there is different magnitudo between those two information
