import os

from PIL import Image
import Quartz


image_dir = os.path.join(os.path.dirname(__file__), "images")
spanned_dir = os.path.join(image_dir, "spanned")
os.makedirs(spanned_dir, exist_ok=True)
apod_path = os.path.join(image_dir, "apod")
iotd_path = os.path.join(image_dir, "iotd")


def get_monitor_info():
    max_displays = 2
    err, display_ids, display_count = Quartz.CGGetActiveDisplayList(max_displays, None, None)
    if err != 0:
        raise RuntimeError(f"Error getting active display list: {err}")

    monitors = []
    for i in range(display_count):
        display_id = display_ids[i]
        bounds = Quartz.CGDisplayBounds(display_id)
        monitor_info = {
            'id': display_id,
            'x': int(bounds.origin.x),
            'y': int(bounds.origin.y),
            'width': int(bounds.size.width),
            'height': int(bounds.size.height)
        }
        monitors.append(monitor_info)
    return monitors


def create_spanned_wallpapers(source_path, monitor_info, output_dir):
    """
    split an image into separate images for each monitor
    """
    min_x = min(m['x'] for m in monitor_info)
    min_y = min(m['y'] for m in monitor_info)
    max_x = max(m['x'] + m['width'] for m in monitor_info)
    max_y = max(m['y'] + m['height'] for m in monitor_info)
    total_width = max_x - min_x
    total_height = max_y - min_y

    src_img = Image.open(source_path).resize((total_width, total_height))

    for idx, monitor in enumerate(monitor_info):
        left = monitor['x'] - min_x
        top = monitor['y'] - min_y
        right = left + monitor['width']
        bottom = top + monitor['height']
        box = (left, top, right, bottom)
        cropped = src_img.crop(box)
        output_path = f"{output_dir}/wallpaper_monitor_{idx + 1}.png"
        cropped.save(output_path)
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    image_path = os.path.join(apod_path, "ScyllaB_LerouxGere_2094.jpg")
    monitors = get_monitor_info()
    create_spanned_wallpapers(source_path=image_path, monitor_info=monitors, output_dir=spanned_dir)

