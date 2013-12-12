#!/usr/bin/env python

#workaround to install new packages without being root
import sys
sys.path.append('/home/username/py_libs/')

import web
import requests
from xml.dom import minidom

urls = (
    '/', 'index'
)

render = web.template.render('templates/')

WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
raincodes = ["3", "4", "5", "6", "8", "9", "10", "11", "12", "35", "37", "38", "39", "40", "45", "46", "47"]

class index:
    def GET(self):
        webpage = requests.get('http://weather.yahooapis.com/forecastrss?w=1968222')
        if webpage.status_code == requests.codes.ok:
            dom = minidom.parseString(webpage.content)
            conditions = dom.getElementsByTagNameNS(WEATHER_NS, 'condition')[0]
            weathercode = conditions.getAttribute('code')
            currweather = conditions.getAttribute('text')
	    degrees = conditions.getAttribute('temp')
            if weathercode in raincodes:
                israining = "YES"
            else:
                israining = "NO"
            return render.index(israining, currweather, degrees)
        else:
            return "Error fetching weather data. Try again later."

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

"""
Applicable weather codes, for reference: 
3	severe thunderstorms
4	thunderstorms
5	mixed rain and snow
6	mixed rain and sleet
8	freezing drizzle
9	drizzle
10	freezing rain
11	showers
12	showers
35	mixed rain and hail
37	isolated thunderstorms
38	scattered thunderstorms
39	scattered thunderstorms
40	scattered showers
45	thundershowers
46	snow showers
47	isolated thundershowers
"""
