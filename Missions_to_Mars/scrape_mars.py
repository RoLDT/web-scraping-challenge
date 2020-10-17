import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import re

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

    browser = init_browser()
    Mars_Dict ={}

    # ## Scraping for News Title and News Paragraph text

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_list = soup.find("ul", class_= "item_list")
    news_item = news_list.find("li", class_= "slide")

    news_title = news_item.find("div", class_ = "content_title").text
    news_p = news_item.find("div", class_ = "article_teaser_body").text

    # ## Scraping for Mars Image

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    feature = soup.find("div", class_ = "carousel_items")("article")[0]["style"].replace("background-image: url('", "").replace("');","")
    image_url = "https://www.jpl.nasa.gov"
    
    featured_image_url = image_url + feature

    # ## Scraping for Mars Weather - Twitter

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather_tweet = soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})

    try:
        mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
        mars_weather

    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = soup.find('span', text=pattern).text
        mars_weather
    
    mars_weather = mars_weather.replace("InSight","").replace("sol", "Sol")

    # ## Mars Facts

    facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(facts_url)
    tables

    facts_df = tables[0]
    facts_df.rename(columns={0:"Description", 1:"Value"}, inplace=True)
    facts_df.set_index("Description", inplace=True)
    
    facts_html = facts_df.to_html()
    facts_html.replace("\n","")

    # ## Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    image_url = "https://astrogeology.usgs.gov"

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    hemisphere_image_urls = []
    
    hemispheres = soup.find_all("div", class_= "item")

    for h in hemispheres:
        #Get title
        title = h.find("h3").text
        #Get url to visit
        incomp_img = h.find("a")["href"]
        url_visit = image_url+incomp_img
        #Go to web page for full image
        browser.visit(url_visit)
        new_html = browser.html
        soup = BeautifulSoup(new_html, "html.parser")
        #Get full image
        comp_img = image_url+ soup.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls.append({"title" : title, "img_url" : comp_img})

    Mars_Dict = {
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "mars_weather":mars_weather,
    "facts":facts_html,
    "hemisphre_image_urls":hemisphere_image_urls
    }

    return Mars_Dict