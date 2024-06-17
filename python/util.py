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
    # todo: set SYSTEM as a const at the top - it's also used in open_image
    #       rename current_date to CURRENT_DATE for clarity (it is a constant)
    if not os.path.exists(file_path):
        logger.error(f"Wallpaper file does not exist: {file_path}")
        return

    system = platform.system()
    if system == "darwin":
        from appscript import app, mactypes
        logger.info(f"set_wallpaper: {file_path}")
        app('Finder').desktop_picture.set(mactypes.File(file_path))
    elif system == "Windows":
        import ctypes
        import winreg as reg

        # Update the registry
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, reg.KEY_WRITE)
        reg.SetValueEx(key, "Wallpaper", 0, reg.REG_SZ, file_path)
        reg.CloseKey(key)

        # Notify the system to update the desktop background
        SPI_SETDESKWALLPAPER = 20
        SPIF_UPDATEINIFILE = 1
        SPIF_SENDCHANGE = 2
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, file_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
