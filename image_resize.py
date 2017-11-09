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
        '--image_dir', required=True, help='Path to initial image')
    parser.add_argument(
        '--output_dir', help='Path to resulted image')
    parser.add_argument(
        '-v', '--verbose', action='count', default=0)
    return parser.parse_args()


def load_original_image(path_to_original_image):
        try:
            return Image.open(path_to_original_image)
        except FileNotFoundError:
            return None


def write_resized_image(resized_image, output_dir, original_dir):
    img_name_template = '{name}__{width}X{height}{ext}'
    resized_image_name = img_name_template.format(name=original_dir.stem,
                                                  width=resized_image.width,
                                                  height=resized_image.height,
                                                  ext=original_dir.suffix)
    location = output_dir if output_dir else original_dir.parent
    resized_image_path = Path(location).joinpath(Path(resized_image_name))
    try:
        resized_image.save(resized_image_path)
        return resized_image_path
    except FileNotFoundError:
        return None


def get_resized_image(image, scale, height, width):
    logging.debug("Original image widthXsize", image.width, image.height)
    if scale:
        img = image.resize((int(image.width*scale), int(image.height*scale)))
    elif width and height:
        img = image.resize((width, height))
    elif width:
        wratio = width/float(image.width)
        hsize = int(float(image.height)*float(wratio))
        img = image.resize((width, hsize))
    elif height:
        hratio = height / float(image.height)
        wsize = int(float(image.width) * float(hratio))
        img = image.resize((wsize, height))
    return img


if __name__ == '__main__':
    cmd_args = parse_args()
    logging_level = VERBOSITY_TO_LOGGING_LEVELS[cmd_args.verbose]
    logging.basicConfig(level=logging_level)
    if cmd_args.scale and (cmd_args.width or cmd_args.height):
        sys.exit("Incompatible program arguments, "
                 "please use --help for more details")
    if not cmd_args.scale and not (cmd_args.width or cmd_args.height):
        sys.exit("missing program arguments, "
                 "please use --help for more details")
    image_dir_path = Path(cmd_args.image_dir)
    origional_image = load_original_image(image_dir_path)
    if origional_image:
        resized_image = get_resized_image(origional_image,
                                          scale=cmd_args.scale,
                                          height=cmd_args.height,
                                          width=cmd_args.width)
        resized_image_path = write_resized_image(resized_image,
                                                 cmd_args.output_dir,
                                                 image_dir_path)
        if resized_image_path:
            print("Resized image location ", str(resized_image_path))
        else:
            print("Original image is damaged or output dir is wrong",
                  image_dir_path, cmd_args.output_dir)
