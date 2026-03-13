import os
from datetime import datetime, timedelta

from logger import logger
from util import download_image, get_date, get_source, current_date, get_image_name
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
root_url = os.environ.get("APOD_ROOT_URL")
api_key = os.environ.get("API_KEY")
open_image = os.environ.get("OPEN_IMAGE", "False").lower() == "true"
target_folder = os.path.join(os.path.dirname(__file__), "images", "apod")


def get_post(target_date: str = current_date) -> dict:
    page_url = f"{root_url}?api_key={api_key}&date={target_date}"
    page = get_source(page_url)
    page_data = page.json()
    return page_data


def get_image_url(page_data) -> str:
    """
    look for hdurl, fallback on url
    """
    image_url = page_data.get("hdurl", page_data.get("url", ""))
    return image_url


def get_old_images(start_date: str, end_date: str = current_date, max_errors: int = 3):
    """
    Download images for a date range from end_date back to start_date (most recent to least recent)
    break if an image already exists on disk
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    errors = 0

    current = end
    while current >= start:
        target_date = current.strftime("%Y-%m-%d")
        post = get_post(target_date=target_date)
        image_url = get_image_url(post)

        if image_url:
            image_name = get_image_name(image_url)
            target_path = os.path.join(target_folder, image_name)
            if os.path.exists(target_path):
                logger.info(f"image for {target_date} already exists, short-circuiting")
                break
            try:
                download_image(image_url=image_url, target_folder=target_folder, open_image_app=False)
            except Exception as e:
                logger.error(f"error downloading image for {target_date}: {e}")
                errors += 1
                if errors >= max_errors:
                    logger.error("max errors reached, stopping")
                    break
        else:
            logger.warning(f"{target_date}: no image found")

        current -= timedelta(days=1)


def get_todays_image():
    page_data = get_post()
    image_url = get_image_url(page_data=page_data)
    if image_url:
        image_path = download_image(image_url=image_url, target_folder=target_folder, open_image_app=open_image)
        return image_path
    else:
        logger.info("no image found sry")
        return None


if __name__ == '__main__':
    get_todays_image()
    # get_old_images(start_date="2026-01-01", end_date="2026-03-02")
