# PSXify

PSXify is a very simple Python script that converts an image into a PS1 Texture.

## Usage

usage: `psxify.py [-h] [-r {detailed,standard,low}] [-p {true,false}] input_image output_image`

Convert a texture to a PS1-style.

**Positional Arguments:**

*   `input_image`:  Path to the input texture file.  It is recommended this file is a 1:1 aspect ratio.
*   `output_image`: Path to save the processed image.

**Options:**

*   `-h, --help`:  Show this help message and exit.
*   `-r, --resolution {detailed,standard,low}`:  Conversion resolution.
    *   `detailed`: Recommended for important objects (e.g., characters).
    *   `standard`:  A good default for most textures.
    *   `low`: Recommended for small or unimportant background props.
*   `-p, --posterization {true,false}`:  Enable posterization (restricts the color palette).
    *   `true`:  Posterization is enabled.
    *   `false`: Posterization is disabled.  Recommended for non-albedo textures.
