#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup


# In[2]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ## Scraping for News Title and News Paragraph text

# In[3]:


url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(url)


# In[4]:


html = browser.html
soup = BeautifulSoup(html, "html.parser")

news_list = soup.find("ul", class_= "item_list")
news_item = news_list.find("li", class_= "slide")

news_title = news_item.find("div", class_ = "content_title").text

news_p = news_item.find("div", class_ = "article_teaser_body").text

print(news_title)
print(news_p)


# ## Scraping for Mars Image

# In[5]:


url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)


# In[6]:


html = browser.html
soup = BeautifulSoup(html, "html.parser")

feature = soup.find("div", class_ = "carousel_items")("article")[0]["style"].replace("background-image: url('", "").replace("');","")
image_url = "https://www.jpl.nasa.gov"

featured_image_url = image_url + feature

featured_image_url


# ## Scraping for Mars Weather - Twitter

# In[7]:


import re


# In[8]:


url = "https://twitter.com/marswxreport?lang=en"
browser.visit(url)


# In[9]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[10]:


mars_weather_tweet = soup.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })


# In[11]:


try:
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    mars_weather

except AttributeError:
    pattern = re.compile(r'sol')
    mars_weather = soup.find('span', text=pattern).text
    mars_weather
    
mars_weather = mars_weather.replace("InSight","").replace("sol", "Sol")

print(mars_weather)


# In[ ]:


#<span class="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0">InSight sol 670 (2020-10-15) low -95.8ºC (-140.5ºF) high -15.8ºC (3.5ºF)
#winds from the WNW at 8.2 m/s (18.3 mph) gusting to 23.1 m/s (51.6 mph)
#pressure at 7.50 hPa</span>


# In[ ]:


#mars_weather = soup.find("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").text
#mars_weather


# ## Mars Facts

# In[12]:


facts_url = "https://space-facts.com/mars/"


# In[13]:


tables = pd.read_html(facts_url)
tables


# In[14]:


facts_df = tables[0]
facts_df.rename(columns={0:"Description", 1:"Value"}, inplace=True)
facts_df.set_index("Description", inplace=True)

facts_df


# In[15]:


facts_html = facts_df.to_html()
facts_html


# ## Mars Hemispheres

# In[16]:


url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)

image_url = "https://astrogeology.usgs.gov"


# In[17]:


html = browser.html
soup = BeautifulSoup(html, "html.parser")

hemisphere_image_urls = []

hemispheres = soup.find_all("div", class_= "item")

#print(hemispheres)

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


# In[18]:


hemisphere_image_urls


# ## Complete Mars Dictionary

# In[19]:


Mars_Dict = {
    "news_title":news_title,
    "news_p":news_p,
    "featured_image_url":featured_image_url,
    "mars_weather":mars_weather,
    "facts":facts_html,
    "hemisphre_image_urls":hemisphere_image_urls
}


# In[20]:


Mars_Dict


# In[ ]:




