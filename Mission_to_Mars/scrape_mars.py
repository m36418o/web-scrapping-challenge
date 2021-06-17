# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # setting NASA url
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # grabbing a response
    response = requests.get(nasa_url)
    # creating a Soup object with html parser
    soup = bs(response.text, 'html.parser')
    # grab the latest news title and paragraphs
    latest_title = soup.find_all('div', class_="content_title")[0].text
    latest_paragraph = soup.find_all('div', class_="rollover_description_inner")[0].text
    # JPL featured image url
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    jpl_space_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    browser.visit(jpl_url)
    # finding featured image direct url
    html = browser.html
    img_soup = bs(html, 'html.parser')
    img_src = jpl_space_url + img_soup.find_all('img', class_='headerimage fade-in')[0]['src']
    # Mars fact url
    mars_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_url)[0]
    # setting urls and containers
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    usgs_base_url = "https://astrogeology.usgs.gov"
    url_to_pages = []
    img_urls = []
    # turning on brower and navigate to url
    browser.visit(usgs_url)
    html = browser.html
    usgs_soup = bs(html, 'html.parser')
    # grabbing titles
    titles = usgs_soup.find_all('h3')
    titles = [title.text for title in titles]
    # grabbing urls to each pages
    for i in range(8):
        temp_url = usgs_soup.find_all('a', class_="itemLink product-item")[i]['href']
        if temp_url not in url_to_pages:
            url_to_pages.append(temp_url)
    # going to each pages to grab image urls
    for i in range(4):
        page_url = usgs_base_url + url_to_pages[i]
        browser.visit(page_url)
        html = browser.html
        mars_soup = bs(html, 'html.parser')
        img_urls.append(usgs_base_url + mars_soup.find('img', class_="wide-image")['src'])
    # appending title and url to a list of dictionaries
    hemi_img_urls = []
    for i in range(4):
        hemi_img_urls.append({'title': titles[i], 'img_url': img_urls[i]})

    mars_dict = {
        'latest_title': latest_title,
        'latest_paragraph': latest_paragraph,
        'featured_img': img_src,
        'mars_facts': mars_facts,
        'hemisphere_img_urls': hemi_img_urls
    }

    return mars_dict

def main():
    scrape()

if __name__ == '__main__':
    main() 