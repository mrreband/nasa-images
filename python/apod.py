import os

from logger import logger
from util import download_image, get_source, current_date
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
root_url = os.environ.get("APOD_ROOT_URL")
api_key = os.environ.get("API_KEY")
target_folder = os.path.join(os.path.dirname(__file__), "images", "apod")


def get_latest_post() -> dict:
    page_url = f"{root_url}?api_key={api_key}&date={current_date}"
    page = get_source(page_url)
    page_data = page.json()
    return page_data


def get_image_url(page_data) -> str:
    """
    look for hdurl, fallback on url
    """
    image_url = page_data.get("hdurl", page_data.get("url", ""))
    return image_url


def main(open_image_app: bool = True):
    page_data = get_latest_post()
    image_url = get_image_url(page_data=page_data)
    if image_url:
        image_path = download_image(image_url=image_url, target_folder=target_folder, open_image_app=open_image_app)
        return image_path
    else:
        logger.info("no image found sry")
        return None


if __name__ == '__main__':
    main()
