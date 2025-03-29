#!/usr/bin/env python

from PIL import Image, ImageOps
import argparse
import os


class bcolors:
    OK = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def ps1_texture_conversion(
    input_image_path: str,
    output_image_path: str,
    resolution: tuple[int, int],
    posterization: str,
    bits: int,
) -> None:
    """
    Converts an image to a PS1-style texture with different options.

    Args:
        input_image_path: Path to the input image file.
        output_image_path: Path to save the processed image.
        resolution:  'detailed', 'standard', or 'low'.
        posterization:  'true', or 'false'.
    """
    try:
        img = Image.open(input_image_path)
    except FileNotFoundError:
        print(bcolors.FAIL, end="")
        print(f"Error: Input image file not found at {input_image_path}")
        print(bcolors.ENDC, end="")
        exit(1)
    except Exception as e:
        print(bcolors.FAIL, end="")
        print(f"Error opening image: {e}")
        print(bcolors.ENDC, end="")
        exit(1)

    width, height = img.size
    if (width / height) != 1:
        print(bcolors.WARNING, end="")
        print(
            f"WARNING: provided image resolution of ({width}x/{height}y) "
            "is not a 1:1 aspect ratio. Visual distortion will occur."
        )
        print(bcolors.ENDC, end="")

    print(f"Shrinking image to {resolution}...")
    imgResized = img.resize(resolution, Image.NEAREST)

    if posterization == "true":
        print(f"Posterizing image to {bits} bits...")
        try:
            imgResized = ImageOps.posterize(imgResized, bits)
        except OSError as e:
            print(bcolors.FAIL, end="")
            print(f"Invalid input image format: {e}")
            print(bcolors.ENDC, end="")
            exit(1)

    try:
        img.save(output_image_path)
        print(bcolors.OK, end="")
        print(f"Processed image saved to {output_image_path}")
        print(bcolors.ENDC, end="")
    except Exception as e:
        print(bcolors.FAIL, end="")
        print(f"Error saving image: {e}")
        print(bcolors.ENDC, end="")
        exit(1)


def split_filepath(filepath: str) -> tuple[str, str]:
    """
    Splits a filepath into the path and the extension.

    Args:
      filepath: The full path to a file.

    Returns:
      A tuple containing:
        - The base name of the file (without extension).
        - The extension (including the leading dot).
    """
    try:
        base_name, extension = os.path.splitext(filepath)
        return base_name, extension
    except Exception as e:
        print(bcolors.FAIL, end="")
        print(f"Error determining default output filename: {e}")
        print(bcolors.ENDC, end="")
        return "", ""

def main():
    parser = argparse.ArgumentParser(
        description="Convert a texture to a PS1-style."
    )
    parser.add_argument(
        "input_image",
        help="Path to the input texture file. It is recommended "
        "this file is a 1:1 aspect ratio.",
    )
    parser.add_argument(
        "output_image", nargs="?", help="Path to save the processed image."
    )
    parser.add_argument(
        "-r",
        "--resolution",
        default="standard",
        choices=["detailed", "standard", "low"],
        help="Conversion resolution: detailed, standard, or low. "
        "Recommended to use detailed for important objects "
        "(e.g. characters), low to unimportant background props, "
        "and standard for everything else.",
    )
    parser.add_argument(
        "-p",
        "--posterization",
        default="true",
        choices=["true", "false"],
        help="Whether to enable posterization, which will restrict "
        "the color palette. Recommended to turn off for "
        "non-albedo textures, if you are using those.",
    )

    args = parser.parse_args()

    if args.resolution == "detailed":
        resolution = (256, 256)
        bits = 8
    elif args.resolution == "standard":
        resolution = (128, 128)
        bits = 4
    elif args.resolution == "low":
        resolution = (64, 64)
        bits = 4

    if not os.path.exists(args.input_image):
        print(f"{args.input_image} does not exist.")
        exit(1)

    if not args.output_image:
        args.output_image = (
            f"{split_filepath(args.input_image)[0]}"
            "_psx_{args.resolution}{split_filepath"
            "(args.input_image)[1]}"
        )

    ps1_texture_conversion(
        args.input_image,
        args.output_image,
        resolution,
        args.posterization,
        bits,
    )

    exit(0)

if __name__ == "__main__":
    main()
