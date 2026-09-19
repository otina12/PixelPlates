import os
from collections import Counter

from PIL import Image


def pixel_artify(image_path: str, color_palette: dict[str, tuple[int, int, int]], pixels_per_edge: int):
    if pixels_per_edge <= 0:
        raise ValueError("pixels_per_edge must be a positive integer")

    image = Image.open(image_path)
    width, height = image.size

    if width != height:
        raise ValueError("Image must be square (width must equal height)")

    image = _upscale_to_multiple(image, pixels_per_edge)

    width, height = image.size
    coordinate_cnt = pixels_per_edge ** 2
    pixelated_image = Image.new("RGB", (width, height))
    color_counts = Counter()

    for coordinate_i in range(coordinate_cnt):
        x, y = _oned_to_twod(coordinate_i, pixels_per_edge)
        pixel_data = _coordinate_pixels(image, x, y, pixels_per_edge)
        avg_color = _avg_color(pixel_data)
        color_name, closest = _closest_color(avg_color, color_palette)
        color_counts[color_name] += 1

        start_x = x * width // pixels_per_edge
        start_y = y * height // pixels_per_edge
        end_x = (x + 1) * width // pixels_per_edge
        end_y = (y + 1) * height // pixels_per_edge

        pixelated_image.paste(closest, (start_x, start_y, end_x, end_y))

    pixelated_image = _gridify_image(pixelated_image, pixels_per_edge)

    image_name = image_path.split("/")[-1].split(".")[0]
    image_dir = f"output/{image_name}"
    output_path = f"{image_dir}/{image_name}_{pixels_per_edge}x{pixels_per_edge}.png"

    os.makedirs(image_dir, exist_ok = True)
    pixelated_image.save(output_path)

    _print_color_usage(image_name, pixels_per_edge, color_palette, color_counts)


def _upscale_to_multiple(image: Image.Image, pixels_per_edge: int) -> Image.Image:
    width, height = image.size

    new_width = max(((width + pixels_per_edge - 1) // pixels_per_edge) * pixels_per_edge, pixels_per_edge * 2)
    new_height = max(((height + pixels_per_edge - 1) // pixels_per_edge) * pixels_per_edge, pixels_per_edge * 2)

    return image.resize((new_width, new_height), Image.Resampling.NEAREST)


def _oned_to_twod(index: int, width: int) -> tuple[int, int]:
    x = index % width
    y = index // width

    return (x, y)


def _coordinate_pixels(image: Image.Image, x: int, y: int, pixels_per_edge: int) -> list[tuple[int, int, int]]:
    width, height = image.size

    start_x = x * width // pixels_per_edge
    end_x = (x + 1) * width // pixels_per_edge
    start_y = y * height // pixels_per_edge
    end_y = (y + 1) * height // pixels_per_edge

    return image.crop((start_x, start_y, end_x, end_y)).getdata()


def _avg_color(pixels: list[tuple[int, int, int]]) -> tuple[int, int, int]:
    r = sum(pixel[0] for pixel in pixels) // len(pixels)
    g = sum(pixel[1] for pixel in pixels) // len(pixels)
    b = sum(pixel[2] for pixel in pixels) // len(pixels)

    return (r, g, b)


def _closest_color(pixel: tuple[int, int, int], color_palette: dict[str, tuple[int, int, int]]) -> tuple[str, tuple[int, int, int]]:
    r, g, b = pixel
    color_name, closest = min(color_palette.items(), key = lambda item: (item[1][0] - r) ** 2 + (item[1][1] - g) ** 2 + (item[1][2] - b) ** 2)

    return (color_name, closest)


def _gridify_image(image: Image.Image, pixels_per_edge: int) -> Image.Image:
    width, height = image.size
    grid_image = image.copy()

    for grid_x in range(pixels_per_edge):
        x = grid_x * width // pixels_per_edge
        for y in range(height):
            grid_image.putpixel((x, y), (0, 0, 0))

    for grid_y in range(pixels_per_edge):
        y = grid_y * height // pixels_per_edge
        for x in range(width):
            grid_image.putpixel((x, y), (0, 0, 0))

    return grid_image

def _print_color_usage(image_name, pixels_per_edge, color_palette, color_counts):
    total = pixels_per_edge ** 2
    print(f"\n{image_name} — {pixels_per_edge}x{pixels_per_edge} ({total:,} pixels)")

    for color_name in sorted(color_palette, key = lambda name: color_counts[name], reverse = True):
        count = color_counts[color_name]
        print(f"  {color_name:<17} {count:>7,}")