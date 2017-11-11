import argparse
import logging
import sys
from PIL import Image
from pathlib import Path


VERBOSITY_TO_LOGGING_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--scale', type=float,
        help='Scale the image, incompatible with --height or --width')
    parser.add_argument(
        '-he', '--height', type=int, help='Desired height of image')
    parser.add_argument(
        '-w', '--width', type=int, help='Desired width of image')
    parser.add_argument(
        '-imd', '--image_dir', required=True, help='Path to initial image')
    parser.add_argument(
        '-otd', '--output_dir', help='Path to resulted image')
    parser.add_argument(
        '-v', '--verbose', help='log level', action='count', default=0)
    return parser.parse_args()


def load_original_image(path_to_original_image):
    try:
        return Image.open(path_to_original_image)
    except (FileNotFoundError, IOError):
        return None


def write_resized_image(resized_image, output_dir, original_dir):
    img_name_template = '{name}__{width}X{height}{ext}'
    try:
        resized_image_name = img_name_template.format(
            name=original_dir.stem, width=resized_image.width,
            height=resized_image.height, ext=original_dir.suffix)
        location = output_dir if output_dir else original_dir.parent
        resized_image_path = Path(location).joinpath(Path(resized_image_name))
        resized_image.save(resized_image_path)
        return resized_image_path
    except (FileNotFoundError, IOError, AttributeError):
        return None


def resize_by_width_height(image, **kwargs):
    width, height = kwargs.get('width'), kwargs.get('height')
    if not width:
        hratio = height / float(image.height)
        width = int(float(image.width) * float(hratio))
    if not height:
        wratio = width / float(image.width)
        height = int(float(image.height) * float(wratio))
    current_aspect = round(float(image.height) / float(image.width), 1)
    expected_aspect = round(height / width, 1)
    if current_aspect != expected_aspect:
        logging.warning("Desired height width aspect ratio "
                        "does not match the current")
    return image.resize((width, height))


def get_resized_image(image, scale, height, width):
    if not image:
        return None
    logging.debug("Original image widthXheight: {}X{}".format(image.width,
                                                              image.height))
    if scale:
        img = image.resize((int(image.width*scale), int(image.height*scale)))
    elif width or height:
        img = resize_by_width_height(image, height=height, width=width)
    else:
        return None
    return img


if __name__ == '__main__':
    cmd_args = parse_args()
    logging_level = VERBOSITY_TO_LOGGING_LEVELS[cmd_args.verbose]
    logging.basicConfig(level=logging_level)
    if cmd_args.scale and (cmd_args.width or cmd_args.height):
        sys.exit("Incompatible program arguments, "
                 "please use --help for more details")
    image_dir_path = Path(cmd_args.image_dir)
    origional_image = load_original_image(image_dir_path)
    resized_image = get_resized_image(origional_image,
                                      scale=cmd_args.scale,
                                      height=cmd_args.height,
                                      width=cmd_args.width)
    resized_image_path = write_resized_image(resized_image,
                                             cmd_args.output_dir,
                                             image_dir_path)
    if resized_image_path:
        print("Resized image location", resized_image_path)
    else:
        print("Bad original image or/and missing/incorrect program args")
