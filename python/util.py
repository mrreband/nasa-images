import os
import platform
import subprocess

import urllib.request
from datetime import datetime, timedelta

import feedparser
import requests

from logger import logger

current_date = datetime.now().strftime("%Y-%m-%d")


def get_date(days_diff: int):
    return (datetime.now() - timedelta(days=abs(days_diff))).strftime("%Y-%m-%d")


def get_source(url):
    """Return the source code for the provided URL.

    Args:
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html.
    """
    response = requests.get(url)
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


def open_image(file_path):
    """
    open a file with the default OS app
    """
    system = platform.system()
    if system == 'Linux':
        subprocess.run(['xdg-open', file_path])
    elif system == 'Darwin':  # macOS
        subprocess.run(['open', file_path])
    elif system == 'Windows':
        subprocess.run(['start', '', file_path], shell=True)
    else:
        logger.error("Unsupported operating system. Cannot open the file.")


def download_image(image_url, target_folder, open_image_app: bool = False):
    image_name = image_url.split("/")[-1]
    target_path = os.path.join(target_folder, image_name)
    if os.path.exists(target_path):
        logger.info(f"{current_date}: target file {target_path} already exists")
    else:
        os.makedirs(target_folder, exist_ok=True)
        logger.info(f"{current_date}: {image_url} ==> {target_path}")
        urllib.request.urlretrieve(image_url, target_path)

    if open_image_app:
        open_image(target_path)
    return target_path


def set_wallpaper(file_path):
    from appscript import app, mactypes
    logger.info(f"set_wallpaper: {file_path}")
    app('Finder').desktop_picture.set(mactypes.File(file_path))
