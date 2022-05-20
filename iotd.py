import os
import requests
from bs4 import BeautifulSoup
from util import get_feed, download_image

iotd_url = "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"
target_folder = "./images/iotd"


def get_iotd_image_url(post_url):
    last_post = requests.get(post_url)
    data = str(last_post.content)
    soup = BeautifulSoup(data, features="lxml")
    image = soup.find("meta", property="og:image")
    image_url = image.attrs.get("content", "")
    return image_url


if __name__ == '__main__':
    os.makedirs(target_folder, exist_ok=True)

    last_post_url = get_feed(iotd_url, 1)[0]["link"]
    image_url = get_iotd_image_url(last_post_url)

    if image_url:
        download_image(image_url, target_folder)
