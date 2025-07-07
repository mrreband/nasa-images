import os

import apod
import iotd
from logger import logger
from util import get_date, get_file_contents, write_file_contents


def get_readme_path():
    python_folder = os.path.join(os.path.dirname(__file__))
    root_folder = os.path.dirname(python_folder)
    readme_path = os.path.join(root_folder, "README.md")
    return readme_path


def get_readme():
    readme_path = get_readme_path()
    return get_file_contents(file_path=readme_path)


def write_readme(file_contents):
    readme_path = get_readme_path()
    write_file_contents(file_path=readme_path, file_contents=file_contents)


def update_readme():
    """
    update the root README.md - set urls for the latest images, set last updated date
    """
    img_height = '"300"'

    page_data = apod.get_post()
    image_url = apod.get_image_url(page_data=page_data)
    apod_url_line = f'<a href="{image_url}"><img alt="apod" src="{image_url}" height={img_height} /></a>\n'

    last_post = iotd.get_feed(iotd.iotd_url, 1)[0]
    last_post_url = last_post["link"]
    image_url = iotd.get_iotd_image_url(last_post_url)
    iotd_url_line = f'<a href="{last_post_url}"><img alt="iotd" src="{image_url}" height={img_height} /></a>\n'

    readme = get_readme()
    for idx in range(len(readme)):
        if "last updated" in readme[idx]:
            today = get_date(days_diff=0)
            readme[idx] = f"### latest images (last updated {today})\n"
        elif '<img alt="apod"' in readme[idx]:
            readme[idx] = apod_url_line
            logger.info(f"write {apod_url_line}")
        elif '<img alt="iotd"' in readme[idx]:
            readme[idx] = iotd_url_line
            logger.info(f"write {iotd_url_line}")
    write_readme(file_contents=readme)


if __name__ == '__main__':
    update_readme()
