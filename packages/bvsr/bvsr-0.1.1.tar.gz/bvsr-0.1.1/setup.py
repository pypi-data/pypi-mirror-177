# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bvsr']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0', 'gevent==22.10.2', 'tqdm==4.64.1']

entry_points = \
{'console_scripts': ['bvsr = src.bvsr.bvsr:main']}

setup_kwargs = {
    'name': 'bvsr',
    'version': '0.1.1',
    'description': 'Batch Video Size Reduction (BVSR) using ffmpeg.',
    'long_description': "# BVSR\n[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n\nBatch Video Size Reduction (BVSR) using [ffmpeg](https://ffmpeg.org).\n\nA python script to reduce the size of all videos in a folder while keeping its exact structure.\n\n## Requirements\n+ Python 3\n+ [ffmpeg](https://ffmpeg.org/download.html) \n\n## Installation\n```bash\npip install bvsr\n```\nor clone from source\n```bash\ngit clone https://github.com/abdeladim-s/bvsr && cd bvsr\npip install -r requirements.txt\n```\n##\n\n## Usage\n```bash\nusage: bvsr.py [-h] [--version] [--destination-folder DESTINATION_FOLDER]\n               [--crf CRF | --video-quality VIDEO_QUALITY | --target-size TARGET_SIZE] [--audio-quality AUDIO_QUALITY]\n               [--ffmpeg-exec FFMPEG_EXEC] [--encoder ENCODER] [-i]\n               source_folder\n\npositional arguments:\n  source_folder         The Source folder of the videos\n\noptions:\n  -h, --help            show this help message and exit\n  --version             show program's version number and exit\n  --destination-folder DESTINATION_FOLDER\n                        The directory where the output videos will be stored, default to the same folder name with `bvsr` suffix in the\n                        parent directory\n  --crf CRF             Target Constant Rate Factor (CRF) value (RECOMMENDED)[More info at: https://trac.ffmpeg.org/wiki/Encode/H.264]\n  --video-quality VIDEO_QUALITY\n                        Target video quality. Available qualities: ['videophone', 'videoconferencing', '240p', '360p', '480p', 'VCD', '720p',\n                        '720p60', '1080p', '1080p60']\n  --target-size TARGET_SIZE\n                        Target upper bound video size (in MB)\n  --audio-quality AUDIO_QUALITY\n                        Target audio quality. Default to the audio quality of the source video. Available qualities: ['low', 'mid-range',\n                        'medium', 'high', 'highest']\n  --ffmpeg-exec FFMPEG_EXEC\n                        The ffmpeg executable file, default to `ffmpeg`\n  --encoder ENCODER     The video encoder name\n  -i, --ignore-other-files\n                        Ignore the other non-video files, the default operation is to copy the other files to the target folder to keep the\n                        same source folder structure\n\n\n```\n\n## Examples\n\n+ The **recommended** way to reduce the size of a video file is to use the [Constant Rate Factor (CRF)](https://trac.ffmpeg.org/wiki/Encode/H.264):\n> The range of the CRF scale is 0–51, where 0 is lossless, 23 is the default, and 51 is worst quality possible. A lower value generally leads to higher quality, and a subjectively sane range is 17–28. Consider 17 or 18 to be visually lossless or nearly so; it should look the same or nearly the same as the input but it isn't technically lossless.\nThe range is exponential, so increasing the CRF value +6 results in roughly half the bitrate / file size, while -6 leads to roughly twice the bitrate.\n\n>Choose the highest CRF value that still provides an acceptable quality. If the output looks good, then try a higher value. If it looks bad, choose a lower value.\n\nRun the following command to use a CRF value of 34 for example:\n```bash\npython bvsr --crf 34 /path/to/the/source_folder\n```\n\nThis will output the results in a folder in the parent directory with the same name of your `source_folder` suffixed with `_bvsr`. \nThe output folder will have the same structure as the `source_folder` (i.e. processing the video files and just copying any other file. Use `--ignore-other-files` to ignore them instead).\n\n## \n\n+ If you want to specify a video quality rather than using the CRF:\n```bash\npython bvsr --video-quality 480p /path/to/the/source_folder\n```\n[Available qualities](https://en.wikipedia.org/wiki/Bit_rate): `['videophone', 'videoconferencing', '240p', '360p', '480p', 'VCD', '720p',\n                        '720p60', '1080p', '1080p60']`\n\n+ If you just care about the size and not the quality, you can specify a  target size in `MB` directly:\n```bash\npython bvsr --target-size 100 --destination-folder /path/to/destination_folder\n```\n_Although it is not guaranteed._ \n\n## License\n\nGPLv3 © [Batch Video Size Reduction (BVSR)](https://github.com/abdeladim-s/bvsr)\n",
    'author': 'abdeladim-s',
    'author_email': 'sadiki.abdeladim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
