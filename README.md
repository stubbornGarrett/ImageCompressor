## Image Compressor
A script to compress all images inside of a folder

# How to use
Put the script inside the folder with the to compressing images and execute it.
This will create compressed copies of the images, inside a subfolder (./compressed), with default values.

# default values
    -p --path                 : ./
    -e --extension / --format : keeps original format (.jpg and .png supported)
    -q --quality              : 90%

## Note
If the images are already compressed it can be, that the processed images are bigger than the original ones, if the compression quality is better than before.

Converting images from .png to .jpg can obviously result in higher quality loss.
