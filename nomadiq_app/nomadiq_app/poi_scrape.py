from nomadiq_app import app

from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import http.cookiejar
import json
import urllib.request, urllib.error, urllib.parse

def get_poi_img(city,k):
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    query = city
    query = query.replace(" ","+")
    url="http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request("http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2",headers=header)), 'html.parser')

    image_urls = []
    for a in soup.find_all("a",{"class":"iusc"})[:k]:
        mad = json.loads(a["m"])
        murl = mad["murl"]
        print(murl)
        image_urls.append(murl)
    return image_urls[:k]

def get_ig_most_recent(city,k):
    # clean
    city = city.replace(" ","_")
    ig_img_urls = []
    # Scrape from Wiki Travel
    page_link = "https://www.instagram.com/explore/tags/" + city
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    script = page_content.find('script', text=lambda t: \
                           t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)
    for post in data['entry_data']['TagPage'][0]['graphql'
            ]['hashtag']['edge_hashtag_to_media']['edges'][:k]:
        image_src = post['node']['thumbnail_src']
        ig_img_urls.append(image_src)

    return ig_img_urls
