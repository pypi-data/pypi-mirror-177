# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['farmworld', 'farmworld.env', 'farmworld.geojson']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.10.0,<23.0.0',
 'gym==0.21.0',
 'polygenerator>=0.2.0,<0.3.0',
 'pygame>=2.1.2,<3.0.0',
 'stable-baselines3[extra]>=1.6.2,<2.0.0',
 'torch>=1.13.0,<2.0.0']

setup_kwargs = {
    'name': 'farmworld',
    'version': '0.0.2',
    'description': 'Reinforcement Learning for Agriculture',
    'long_description': '# FarmWorld\n\nA reinforcement learning library for agriculture.',
    'author': 'Tom Grek',
    'author_email': 'tom.grek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tomgrek/farmworld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
