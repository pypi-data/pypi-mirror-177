# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['extended_tortoise_models']

package_data = \
{'': ['*']}

install_requires = \
['tortoise-orm']

setup_kwargs = {
    'name': 'extended-tortoise-models',
    'version': '0.1.2',
    'description': 'Extended models for tortoise; less boilerplate for everybody! ⛰',
    'long_description': '# Extended tortoise models\n\nThis package is simply an extension of the `tortoise.Model` to avoid duplicated boilerplate across projects using `tortoise`.\n\n## Installation\n\n```shell\npip install extended-tortoise-models\n```\n\n## Contribution\n\nAdditional models are more than welcome! Please submit a pull request (PR).\n',
    'author': 'Can H. Tartanoglu',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
