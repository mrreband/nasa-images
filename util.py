import os
import subprocess

import pandas as pd
import requests

from requests_html import HTML, HTMLSession
from bs4 import BeautifulSoup


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """
    session = HTMLSession()
    response = session.get(url)
    return response


def get_feed_pd(url):
    """Return a Pandas dataframe containing the RSS feed contents.

    Args: 
        url (string): URL of the RSS feed to read.

    Returns:
        df (dataframe): Pandas dataframe containing the RSS feed contents.
    """
    
    response = get_source(url)
    
    df = pd.DataFrame(columns = ['title', 'link', 'pubDate', 'guid', 'description'])

    with response as r:
        items = r.html.find("item", first=False)
        
        for item in items:        

            title = item.find('title', first=True).text
            link = item.find('link', first=True).text
            pubDate = item.find('pubDate', first=True).text
            guid = item.find('guid', first=True).text
            description = item.find('description', first=True).text

            row = {'title': title, 'link': link, 'pubDate': pubDate, 'guid': guid, 'description': description}
            df = df.append(row, ignore_index=True)

    return df


def get_feed(url, item_count: int):
    """Return a Pandas dataframe containing the RSS feed contents.

    Args: 
        url (string): URL of the RSS feed to read.

    Returns:
        df (dataframe): Pandas dataframe containing the RSS feed contents.
    """
    response = get_source(url)
    fields = {"title": "text", "link": "html", "pubDate": "text", "guid": "text", "description": "text"}
    
    feed_items = []
    with response as r:
        response_items = r.html.find("item", first=False)
        if item_count: 
            response_items = response_items[:item_count]

        for response_item in response_items:
            feed_item = dict((k, getattr(response_item.find(k, first=True), v)) for k, v in fields.items())
            feed_item["link"] = feed_item["link"].replace("<link/>", "")
            feed_items.append(feed_item)

    return feed_items


def download_image(image_url, target_folder):
    image_name = image_url.split("/")[-1]
    target_path = os.path.join(target_folder, image_name)

    if os.path.exists(target_path):
        print(f"target file {target_path} already exists")
    else:
        print(f"{image_url} ==> {target_path}")
        import urllib.request
        urllib.request.urlretrieve(image_url, target_path)
        subprocess.call(('open', target_path))
