from bs4 import BeautifulSoup
import requests
import re
# import sys
# import os
import http.cookiejar
import json
import pandas as pd
import urllib.request, urllib.error, urllib.parse
from unidecode import unidecode



def get_poi_img(city,k=3):
    # try:
    #         bing_urls = pd.read_csv("nomadiq_app/static/data/bing_urls.csv")
    #         image_urls = bing_urls.loc[bing_urls['city'].str.lower().isin([city])]
    #
    #         return image_urls.values.tolist()[0][1:k+1]
    # except:
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    query = unidecode(city)
    query = query.replace(" ","+")
    url="http://www.bing.com/images/search?q=" + query + "travel+city&FORM=HDRSC2"
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), 'html.parser')

    image_urls = []
    for a in soup.find_all("a",{"class":"iusc"})[:k]:
        mad = json.loads(a["m"])
        murl = mad["murl"]
        # print(murl)
        image_urls.append(murl)

    return image_urls

def get_poi_img2(city,TRAVELWORDS):
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    image_urls = []
    city = unidecode(city).replace(" ","+")


    for word in TRAVELWORDS:
        word = word.replace(" ","+")
        url="http://www.bing.com/images/search?q=" + city + "+" + word +"+travel+city&FORM=HDRSC2"
        print(url)
        soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), 'html.parser')
        a = list(soup.find_all("a",{"class":"iusc"}))[0] #[:k]
        mad = json.loads(a["m"])
        murl = mad["murl"]
        # print(murl)
        image_urls.append(murl)
    return image_urls

def get_poi_img_words(city,word_list,k=3):
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    image_urls = []
    city = unidecode(city).replace(" ","+")


    for word in word_list:
        word = word.replace(" ","+")
        url="http://www.bing.com/images/search?q=" + city + "+" + word +"+travel+city&FORM=HDRSC2"
        print(url)
        soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), 'html.parser')
        a = list(soup.find_all("a",{"class":"iusc"}))[0]
        mad = json.loads(a["m"])
        murl = mad["murl"]
        # print(murl)
        image_urls.append(murl)
    return image_urls

def get_poi_imgk(city,keyword,k=3):
    # try:
    #         bing_urls = pd.read_csv("nomadiq_app/static/data/bing_urls.csv")
    #         image_urls = bing_urls.loc[bing_urls['city'].str.lower().isin([city])]
    #
    #         return image_urls.values.tolist()[0][1:k+1]
    # except:
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    city = unidecode(city).replace(" ","+")
    query = keyword.replace(" ","+")
    print(query)
    url="http://www.bing.com/images/search?q=" + city + "+" + query +"travel+city&FORM=HDRSC2"
    soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)), 'html.parser')

    image_urls = []
    for a in soup.find_all("a",{"class":"iusc"})[:k]:
        mad = json.loads(a["m"])
        murl = mad["murl"]
        # print(murl)
        image_urls.append(murl)

    return image_urls
