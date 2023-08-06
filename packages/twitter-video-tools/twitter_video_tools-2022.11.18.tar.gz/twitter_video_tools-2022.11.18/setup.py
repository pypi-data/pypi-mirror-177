# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twitter_video_tools',
 'twitter_video_tools.tests',
 'twitter_video_tools.utils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'playwright>=1.27.1,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'youtube_dl>=2021.12.17,<2022.0.0']

setup_kwargs = {
    'name': 'twitter-video-tools',
    'version': '2022.11.18',
    'description': 'Twitter Video Tools is a multi-processing supported video downloader, supports videos from twitter (or specific user from twitter) && monsnode.',
    'long_description': '# Twitter Video Tools\n[![PyPI version](https://badge.fury.io/py/twitter-video-tools.svg)](https://badge.fury.io/py/twitter-video-tools)\n[![Test](https://github.com/code-yeongyu/twitter_video_tools/actions/workflows/test.yaml/badge.svg?branch=master)](https://github.com/code-yeongyu/twitter_video_tools/actions/workflows/test.yaml)\n[![codecov](https://codecov.io/gh/code-yeongyu/twitter_video_tools/branch/master/graph/badge.svg?token=97K8BBWOH7)](https://codecov.io/gh/code-yeongyu/twitter_video_tools)\n\n- A multi-processing supported video downloader\n- supports downloading videos from twitter (or specific user from twitter) && monsnode.\n\n## Install\n\n### with PIP\n\n```sh\npip install twitter-video-tools\n```\n\n### with Poetry (Recommended)\n\n```sh\npoetry add twitter-video-tools\n```\n\n## Contribution\n\n### Prerequisites\n\n- Python 3.9\n- poetry\n- code editor (vscode recommended)\n\n### Quick Info of setups\n\n- strict type checking using mypy\n- amazing linters & formatters (`yapf`, `pylint`, `isort`)\n  - `unify` for forcing single-quote\n- unit test using `pytest`\n- vscode launch & formatting setups\n\n### All-in-one\n\n```sh\ngh repo clone code-yeongyu/twitter_video_tools\npython3 -m pip install poetry\npoetry install # install dependencies\ncode --install-extension emeraldwalk.RunOnSave # to force single quote\n```\n\nDone!\n\n### Test\n\n```sh\npoetry shell\ninv test\n```\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/code-yeongyu/twitter_video_tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
