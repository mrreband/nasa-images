import os
import subprocess

import urllib.request
import pandas as pd
import feedparser

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


def get_feed(url: str, item_count: int):
    """
    get the latest n entries from an rss feed

    rtype: dict
    """
    feed = feedparser.parse(url)
    feed_items = feed.entries[:item_count]
    fields = ["title", "link", "published", "id", "summary"]
    feed_items = [dict((k, v) for fi in feed_items for k, v in fi.items() if k in fields)]
    return feed_items


def get_feed_pd(url: str, item_count: int):
    """
    get the latest n entries from an rss feed, returned as a pandas dataframe

    :rtype: pd.DataFrame
    """
    feed_items = get_feed(url=url, item_count=item_count)
    df = pd.DataFrame(columns = ['title', 'link', 'pubDate', 'guid', 'description'])

    for item in feed_items:
        df = df.append(item, ignore_index=True)

    return df


def download_image(image_url, target_folder):
    image_name = image_url.split("/")[-1]
    target_path = os.path.join(target_folder, image_name)
    if os.path.exists(target_path):
        print(f"target file {target_path} already exists")
    else:
        os.makedirs(target_folder, exist_ok=True)
        print(f"{image_url} ==> {target_path}")
        urllib.request.urlretrieve(image_url, target_path)
        subprocess.call(('open', target_path))
