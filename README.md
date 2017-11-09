# Images resizer

Resize image to desired height and width. 
User can specify either scale or width and/or height
Also desired location of a resized image can be specified.
If desired location (--output_dir) is not specified 
will be put to initial image location


# System requirements
required python 3.5 installed
pip install -r requirements.txt

# How to install and run

to run it: 
on windows:
```
    python image_resize.py --image_dir "<original image dir>" --width <int> --height <int>
    python image_resize.py --directory "C:\Users\TestFolder\pic.png" --width 100 --height 200
```
on linux might require 
```
  python image_resize.py --image_dir "<original image dir>" --width <int> --height <int>
  ```
--image_dir, --output-dir shall be in the format of your system

Supported Systems: Windows, Unix

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
