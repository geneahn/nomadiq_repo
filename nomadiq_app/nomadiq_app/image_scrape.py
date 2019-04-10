from nomadiq_app import app

from bs4 import BeautifulSoup
import requests

def get_img(city):
    # clean
    cit = city.replace(" ","_")
    # Scrape from Wiki Travel
    page_link = "https://wikitravel.org/en/" + city
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    img_html = page_content.findAll("a", {"class":"image"})
    img_url = img_html[0].img['src']

    if img_url.startswith("/"):
        img_url = "https://wikitravel.org"+img_url

    return img_url
