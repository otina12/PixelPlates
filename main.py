from pixelify import pixel_artify

INPUT_IMAGE_PATH = "input"
PIXELS_PER_EDGE = [8, 16, 32, 64, 128, 256]

def _pixelify_all_sizes(image_path, color_palette):
    for size in PIXELS_PER_EDGE:
        pixel_artify(image_path, color_palette, size)