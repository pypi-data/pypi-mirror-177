# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['willspeak', 'willspeak.tts', 'willspeak.tts.sapi5']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'pyaudio>=0.2.12,<0.3.0',
 'pydantic>=1.10.2,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

extras_require = \
{':sys_platform == "win32"': ['comtypes>=1.1.14,<2.0.0']}

entry_points = \
{'console_scripts': ['willspeak = willspeak.cli:entrypoint']}

setup_kwargs = {
    'name': 'willspeak',
    'version': '0.3.0',
    'description': 'Python Text to Speach using Microsoft Sapi5 with a server/client model',
    'long_description': '# WillSpeak - Work in Progress\nPython Text to Speach using Microsoft Sapi5 with a server/client model.\n\n# Progress update\nThe core functionality is now working, and is ready for testing.\nSome cleanup is still required, but it works.\nOnly supports SAPI5 for now. More to come in the future.\n\n# Info\nI created this project as a way to have good TTS on linux, because TTS on linux at the moment is dreadful.\nFor a long time I wanted to switch to linux, but I needed a good linux TTS software but could not find one.\nSo I decided to create this project to interface with the windows SAPI5 TTS engine.\n\nHow it works is by running this software in server mode on a Windows machine. \nThen configure the linux client to communicate with that Windows TTS server.\nThe client will monitor for text that was copied to the clipboard and converts the text into speech.\n\n# Usage\nThis software has 2 different operational modes, "Local" & "Server/Client". If the TTS engine that you have selected \nworks natively on your operating system, Then you can use Local mode. e.g. SAPI5 is native to windows, so you can use\nLocal mode on Windows when using SAPI5. You should use Server/Client if you want to use SAPI5 on linux.\n\nRun locally on Windows\n```shell\nwillspeak local\n```\n\nTo run in server mode do.\n```shell\nwillspeak server\n```\n\nAnd on the client machine run. "--addr" is the address of the server running the server component.\n```shell\n# 192.168.1.60 is just an example\nwillspeak client --addr=192.168.1.60\n```\n\nThere is one last command that is used to stop any current speech.\n```shell\nwillspeak stop\n```\n\n# TODO\n* Use a string library to analyze and filter the text before converting.\n* Setup prometheus metrics to track usage. This is useful if you wish to use a paid for TTS Service.\n* Add support for other text to speech engines like eSpeak.\n* Add support for running the server component as a Windows service.\n\n# Links\nhttps://winaero.com/unlock-extra-voices-windows-10/\n\n## Version\n0.3.0\n',
    'author': 'willforde',
    'author_email': 'willforde@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/willforde/willspeek.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
