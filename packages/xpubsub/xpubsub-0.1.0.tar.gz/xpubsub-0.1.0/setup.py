# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpubsub']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xpubsub',
    'version': '0.1.0',
    'description': 'Basic PubSub for python app.',
    'long_description': '# xpubsub\nA basic pubsub module for communications within an app.\n',
    'author': 'treborg',
    'author_email': 'treborg@atomix.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/treborg/xpubsub',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.15',
}


setup(**setup_kwargs)
