import apod
import iotd
from util import set_wallpaper


if __name__ == '__main__':
    open_image_app = False
    apod_image_url = apod.main(open_image_app=open_image_app)
    iotd_image_url = iotd.main(open_image_app=open_image_app)
    set_wallpaper(iotd_image_url)
