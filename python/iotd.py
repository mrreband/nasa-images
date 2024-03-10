import os
import requests

from logger import logger, log_fn
from util import get_feed, download_image

iotd_url = "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss"
target_folder = os.path.join(os.path.dirname(__file__), "images", "iotd")


def get_image_from_html(last_post):
    """
    get the img src url embedded in the html
    """
    from bs4 import BeautifulSoup

    data = str(last_post.content)
    soup = BeautifulSoup(data, features="lxml")
    image = soup.find("meta", property="og:image")
    image_url = image.attrs.get("content", None)
    return image_url


@log_fn
def get_iotd_image_url(post_url):
    """
    find the api url in the post metadata - make a request to that endpoint and extract the image url from the response
    """
    last_post = requests.get(post_url)
    try:
        alternate_link = last_post.links["alternate"]
        api_link = alternate_link["url"]
        logger.info(f"api_link = {api_link}")
        api_response = requests.get(api_link).json()

        image_guid = api_response["guid"]
        image_url = image_guid["rendered"]
        return image_url
    except KeyError as ex:
        logger.info(f"KeyError: {ex} - Key not found: {ex.args[0]}")
        return get_image_from_html(last_post=last_post)


def main(open_image_app: bool = True):
    os.makedirs(target_folder, exist_ok=True)

    last_post = get_feed(iotd_url, 1)[0]
    last_post_url = last_post["link"]
    image_url = get_iotd_image_url(last_post_url)

    if image_url:
        image_path = download_image(image_url, target_folder, open_image_app=open_image_app)
        return image_path
    return None


if __name__ == '__main__':
    main()
