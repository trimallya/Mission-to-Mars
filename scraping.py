# Import Splinter, BeautifulSoup, and Pandas
from sys import executable
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Set up the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


# ## JPL Space Images Features Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # Scrape entire facts table into a df
        df = pd.read_html('https://galaxyfacts-mars.com/')[0] 

    except BaseException:
        return None

    # Assign columns and set index of df
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert to html-ready code
    return df.to_html()

def hemi_data(browser):
    
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    hemis = hemi_soup.find_all('div', class_='item')
    hemi_titles = []
    hemispheres = {}
    for hemi in hemis:
        title = hemi.find('h3').text
        hemi_titles.append(title)
    for x in range(0,4):
        
        link = browser.find_by_css('.thumb')[x]
        link.click()
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        hemi_sample = img_soup.find('div', class_='downloads')
        hemi_url = hemi_sample.find('a').get('href')
        browser.back()
        hemispheres = {'img_url': hemi_url, 'title': hemi_titles[x]}
        hemisphere_image_urls.append(hemispheres)

    # 4. Print the list that holds the dictionary of each image url and title.
    hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()

    return hemisphere_image_urls

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Set variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last modified": dt.datetime.now(),
        "hemisphere images": hemi_data(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())