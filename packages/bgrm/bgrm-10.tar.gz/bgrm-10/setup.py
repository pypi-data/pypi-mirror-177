# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bgrm']

package_data = \
{'': ['*']}

install_requires = \
['cvzone==1.5.3',
 'mediapipe==0.8.11',
 'opencv-python==4.6.0.66',
 'protobuf==3.19.0',
 'v4l2-python3==0.3.1']

setup_kwargs = {
    'name': 'bgrm',
    'version': '10',
    'description': 'Remove backgrounds from video feeds in your web cam applications.',
    'long_description': '# Background Remover\n\n## The Need\n\nIt\'s been good long while since Microsoft first released a Teams version for Linux and yet, one of Teams\' coolest features doesn\'t exist in said Linux version: removable backgrounds. As someone who uses Linux for their daily driver, this annoys me.\n\nWell, I\'m an engineer, so of course, I found a solution.\n\nUsing OpenCV and a v4l2loopback device (basically a virtual webcam you can write data to), I threw together a Python application that takes your normal webcam input, removes and replaces the background, and outputs that to the created video device. Problem solved :)\n\nNote, this will work anywhere WebCams are used, not just Teams\n\nNow, the program can also be used to remove backgrounds from video files and save them as video files as well!\n\n## How to Use\n\n### WebCam Replacement\n\nDependencies:\n    - python >= 3.8 (3.10 is what\'s supported officially)\n    - pip\n    - v4l2loopback\n\nSetup:\n1. Configure v4l2loopback (may not be necessary):\n    - Recommended something like this:\n    ```\n    export DEVICE_ARR=(`ls /sys/devices/virtual/video4linux | tr -d \'video\'`); \\\n    sudo modprobe v4l2loopback \\\n        devices=1 exclusive_caps=1 video_nr=${DEVICE_ARR[1]} max_buffers=2 \\\n        card_label=v4l2lo\n    ```\n2. Install with `pip install bgrm`\n\nThen, you can run: \n- Run with `python -m bgrm <options>` (use `--help` to see all options)\n- Example: `python -m bgrm -b ~/Pictures/Wallpapers/ni-skyline-wallpaper.png -w 320 -H 240 -s 2.0`\n\n### File Replacement\n\nYou can also remove the background from video files. It works just like the WebCam, but instead of setting the `--camera` cli arg, you call the program like this:\n\n`python -m bgrm --file_mode -i <input file> -o <output file> <other options>`\n\n## Build from Repo\n\nYou can also build the package yourself from source (or grab the latest version from the releases tab)\n\nTo do that you need the "poetry" build system.\n\nRun `poetry build` and install the whl from the dist/ folder\n',
    'author': 'Dylan Turner',
    'author_email': 'dylantdmt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blueOkiris/bgrm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
