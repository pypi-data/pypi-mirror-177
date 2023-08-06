# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['disinter', 'disinter.types']

package_data = \
{'': ['*']}

install_requires = \
['discord-interactions>=0.4.0,<0.5.0',
 'fastapi>=0.85.1,<0.86.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'disinter',
    'version': '0.0.1',
    'description': 'A discord interactions library',
    'long_description': '<div align=center>\n<h1>disinter.py</h1>\n\nA discord interactions library to receieve interactions via HTTP Posts with an API endpoint.\n\n</div>\n\n## Install\n\n```\npip3 install disinter\n```\n\n## [Usage](./docs/README.md)\n\nLibrary is still under heavy development and expect to have bugs and errors on the way.\n\n##\n\n**&copy; 2022 | TheBoringDude**\n',
    'author': 'TheBoringDude',
    'author_email': 'iamcoderx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
