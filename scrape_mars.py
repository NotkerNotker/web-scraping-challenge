from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scraping():

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    # scrape top article
    MarsContent = {}
    MarsContent['article_title'] = soup.find('div', class_ = 'content_title').text
    MarsContent['article_description']= soup.find('div', class_ = 'rollover_description_inner').text

    # scrape featured image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    response = requests.get(url2)
    soup2 = bs(response.text, 'lxml')

    headerimagestuff = soup2.find('article', class_ = 'carousel_item')
    imageurl = headerimagestuff.find('a')['data-fancybox-href']
    featuredurl = 'https://www.jpl.nasa.gov' + imageurl
    MarsContent['featured_url'] = featuredurl

    # scrape info from twitter page
    url3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url3)
    soup3 = bs(response.text, 'lxml')

    tweet = soup3.find("div", class_ = "js-tweet-text-container")
    mars_weather = tweet.text
    MarsContent['mars_weather'] = mars_weather

    #pull and create space facts table
    url4 = 'https://space-facts.com/mars/'
    factsTable = pd.read_html(url4)
    factsDf = factsTable[0]
    facts = factsDf .to_html()
    MarsContent['table'] = facts

    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response5 = requests.get(url5)
    
    soup5 = bs(response5.text, 'lxml')

    executable_path = {'executable_path': 'C:\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url5)  
    hemiUrls = []
    items = soup5.find_all('div', class_='item')
    coreurl = 'https://astrogeology.usgs.gov' 

    for stuff in items: 
        
        title = stuff.find('h3').text
        imageurl = stuff.find('a', class_='itemLink product-item')['href']
        
        browser.visit(coreurl + imageurl)
        
        hhtml = browser.html
        
        soup = bs(hhtml, 'lxml')
            
        img_url = coreurl + soup.find('img', class_='wide-image')['src']
            
        hemiUrls.append({"title":title,"img_url":img_url})
    
    MarsContent['Hemisphere_Images'] = hemiUrls
    browser.quit()
    return MarsContent