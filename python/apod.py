import os

from logger import logger
from python.util import get_file_contents, write_readme, get_readme
from util import download_image, get_date, get_source, current_date
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
root_url = os.environ.get("APOD_ROOT_URL")
api_key = os.environ.get("API_KEY")
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


def get_old_images(n: int):
    for i in range(1, n):
        target_date = get_date(days_diff=i)
        post = get_post(target_date=target_date)
        image_url = get_image_url(post)
        try:
            if image_url:
                download_image(image_url=image_url, target_folder=target_folder, open_image_app=False)
            else:
                raise FileNotFoundError(f"{target_date}: no image found sry")
        except Exception as e:
            logger.error(f"error downloading image: {e}")


def main(open_image_app: bool = True):
    page_data = get_post()
    image_url = get_image_url(page_data=page_data)
    if image_url:
        image_path = download_image(image_url=image_url, target_folder=target_folder, open_image_app=open_image_app)
        return image_path
    else:
        logger.info("no image found sry")
        return None


def update_readme():
    page_data = get_post()
    image_url = get_image_url(page_data=page_data)
    url_line = f'<img alt="apod" src="{image_url}" />\n'

    readme = get_readme()
    for idx in range(len(readme)):
        if "last updated" in readme[idx]:
            today = get_date(days_diff=0)
            readme[idx] = f"### latest images (last updated {today})\n"
        elif '<img alt="apod"' in readme[idx]:
            readme[idx] = url_line
            logger.info(f"write {url_line}")
    write_readme(file_contents=readme)


if __name__ == '__main__':
    main()
