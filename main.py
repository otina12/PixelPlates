from pixelify import pixel_artify

INPUT_IMAGE_PATH = "input"
PIXELS_PER_EDGE = [8, 16, 32, 64, 128, 256]

def _pixelify_all_sizes(image_path, color_palette):
    for size in PIXELS_PER_EDGE:
        pixel_artify(image_path, color_palette, size)

is_this_it_path = f"{INPUT_IMAGE_PATH}/is_this_it.png"
is_this_it_palette = {
    "black":      (0, 0, 0),
    "white":      (255, 255, 255),
    "grey":       (128, 128, 128),
    "light grey": (192, 192, 192),
    "light pink": (255, 182, 193),
}

_pixelify_all_sizes(is_this_it_path, is_this_it_palette)