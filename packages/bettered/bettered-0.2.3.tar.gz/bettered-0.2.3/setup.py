# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bettered']
install_requires = \
['moe-transcode>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['bettered = bettered:main']}

setup_kwargs = {
    'name': 'bettered',
    'version': '0.2.3',
    'description': 'Automatic helper for redacted better.php.',
    'long_description': '# BetteRED\n\n## Introduction\nbettered automatically transcodes a given path of flac files to mp3 files\nbased on desired quality (MP3 V0 or MP3 320). It will then create a\ncorresponding torrent file to be uploaded to redacted.\n\nbettered uses [Moe](https://github.com/MoeMusic/Moe) to initialize and read the configuration, and the plugin [moe_transcode](https://github.com/MoeMusic/moe_transcode) to handle the transcoding logic.\n\n## Installation:\n\n### 1. Install `bettered` from PyPI\n`$ pip install bettered`\n\n### 2. Install `mktorrent`\n`mktorrent` must be built from source unless your package manager includes >=v1.1\n\n~~~\n$ git clone https://github.com/Rudde/mktorrent.git\n$ cd mktorrent\n$ sudo make install\n~~~\n\n### 3. Install `ffmpeg`\nhttps://ffmpeg.org/download.html\n\nRun `ffmpeg -h` to ensure it\'s in your path.\n\n### 4. Configure\n\nYour configuration file should exist in "~/.config/bettered/config.toml" and should look like the following:\n\n``` toml\nenable_plugins = ["transcode"]\n\n[transcode]\ntranscode_path = "~/transcode"\n\n[bettered]\ntorrent_file_path = "~/torrents"\nredacted_announce_id = "1234abcd"\n```\n\n`transcode_path` is where the transcoded albums will be placed.\n`torrent_file_path` is where the `.torrent` files will be places\n`redacted_announce_id` can be found at https://redacted.ch/upload.php and is the 32 alphanumeric id in your "announce URL"\n\n### 5. Run\n`bettered -h`\n\n## Contributing:\n\n#### 1. Fork the repository and create a feature/bug fix branch\n\n#### 2. Install development requirements\n`$ poetry install`\n\n#### 3. Hack away\n\n#### 4. Lint your code\n`$ pre-commit run -a`\n\n#### 5. Submit a pull request\n',
    'author': 'Jacob Pavlock',
    'author_email': 'jtpavlock@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jtpavlock/bettered',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
