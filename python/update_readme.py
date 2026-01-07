import os

import apod
import iotd
from logger import logger
from util import get_date, get_file_contents, write_file_contents
from requests.exceptions import HTTPError


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


def get_apod(img_height):
    try:
        page_data = apod.get_post()
        image_url = apod.get_image_url(page_data=page_data)
        update_apod = True
        apod_url_line = f'<a href="{image_url}"><img alt="apod" src="{image_url}" height={img_height} /></a>\n'
        apod_error = None
    except HTTPError as ex:
        update_apod = False
        apod_url_line = None
        apod_error = f"{ex.response.status_code} - {ex.response.reason}"
    return {"update": update_apod, "url": apod_url_line, "error": apod_error}


def get_iotd(img_height):
    try:
        last_post = iotd.get_feed(iotd.iotd_url, 1)[0]
        last_post_url = last_post["link"]
        image_url = iotd.get_iotd_image_url(last_post_url)
        iotd_url_line = f'<a href="{last_post_url}"><img alt="iotd" src="{image_url}" height={img_height} /></a>\n'
        iotd_error = None
        update_iotd = True
    except HTTPError as ex:
        iotd_error = f"{ex.response.status_code} - {ex.response.reason}"
        update_iotd = False
        iotd_url_line = None
    return {"update": update_iotd, "url": iotd_url_line, "error": iotd_error}


def update_image_section(readme, image_type, image_data, today):
    """
    Update README lines for a specific image type (apod or iotd)
    """
    for idx in range(len(readme)):
        if readme[idx].startswith(f"{image_type.upper()} image: <!-- {image_type}_last_update_date -->") and image_data["update"]:
            readme[idx] = f"{image_type.upper()} image: <!-- {image_type}_last_update_date --> (last updated {today})\n"
        elif readme[idx].startswith(f"<!-- {image_type}_last_update_status -->"):
            if image_data["error"]:
                readme[idx] = f"<!-- {image_type}_last_update_status --><i>(attempted {today} with error {image_data['error']})</i>\n"
            else:
                readme[idx] = f"<!-- {image_type}_last_update_status -->\n"
        elif f'<img alt="{image_type}"' in readme[idx] and image_data["update"]:
            readme[idx] = image_data["url"]
            logger.info(f"write {image_data['url']}")


def update_readme():
    """
    update the root README.md - set urls for the latest images, set last updated date
    """
    img_height = '"300"'

    apod = get_apod(img_height)
    iotd = get_iotd(img_height)

    readme = get_readme()
    for idx in range(len(readme)):
        today = get_date(days_diff=0)
        if readme[idx].startswith("APOD image: <!-- apod_last_update_date -->") and apod["update"]:
            readme[idx] = f"APOD image: <!-- apod_last_update_date --> (last updated {today})\n"
        elif readme[idx].startswith("<!-- apod_last_update_status -->"):
            if apod["error"]:
                readme[idx] = f"<!-- apod_last_update_status --><i>(attempted {today} with error {apod['error']})</i>\n"
            else:
                readme[idx] = "<!-- apod_last_update_status -->\n"
        elif '<img alt="apod"' in readme[idx] and apod["update"]:
            readme[idx] = apod["url"]
            logger.info(f"write {apod['url']}")

        if readme[idx].startswith("IOTD image: <!-- iotd_last_update_date -->") and iotd["update"]:
            readme[idx] = f"IOTD image: <!-- iotd_last_update_date --> (last updated {today})\n"
        elif readme[idx].startswith("<!-- iotd_last_update_status -->"):
            if iotd["error"]:
                readme[idx] = f"<!-- iotd_last_update_status --><i>(attempted {today} with error {iotd['error']})</i>\n"
            else:
                readme[idx] = "<!-- iotd_last_update_status -->\n"
        elif '<img alt="iotd"' in readme[idx] and iotd["update"]:
            readme[idx] = iotd["url"]
            logger.info(f"write {iotd['url']}")
    write_readme(file_contents=readme)


if __name__ == '__main__':
    update_readme()
