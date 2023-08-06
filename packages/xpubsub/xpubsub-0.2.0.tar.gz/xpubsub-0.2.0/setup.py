# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xpubsub']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xpubsub',
    'version': '0.2.0',
    'description': 'Basic PubSub for python app.',
    'long_description': '# [xpubsub](https://pypi.org/project/xpubsub)\nA basic pubsub module for communications within an app.\n\nThis project is an excercise to help me develop skills relating to:\n\n+ writing a Python module\n+ publishing modules on pypi\n+ using:\n\t+ [git](https://pypi.org/project/git)\n\t+ [pytest](https://pypi.org/project/pytest)\n\t+ [pyenv](https://pypi.org/project/pyenv)\n\t+ [poetry](https://pypi.org/project/poetry)\n\t+ [mypy](https://pypi.org/project/mypy)\n\t+ [tox](https://pypi.org/project/tox)\n\nYou would probably be better off using [PyPubSub](https://pypi.org/project/PyPubSub/)\n\n## Interface\n```python\nfrom xpubsub import PubSub\npub = PubSub()\n\nHashOrList = Union[Hashable, list[Hashable]]\n\npub.add(topic_list: HashOrList, callback: Callable):\npub.remove(topic_list: HashOrList, callback: Callable):\npub.send(topic_list: HashOrList, message: Any):\n```\n\n## Example: example.py\n```python\nfrom xpubsub import PubSub\n\npub = PubSub()\n\n\ndef hello(topic, message):\n    print(topic, message)\n\n\ndef goodbye(topic, msg):\n    print("😭", topic, msg)\n\n\npub.add("hi", hello)\npub.add(["SHTF!", "go away"], goodbye)\n\npub.send("hi", "👋😍")\npub.send("SHTF!", "Head For The Hills!")\npub.send("go away", "its over")\n\npub.remove("go away", goodbye)\npub.send("go away", "nothing happens")  # this does nothing!\n\n```\nOutput\n```\nhi 👋😍\n😭 SHTF! Head For The Hills!\n😭 go away its over\n\n```\n\n\n',
    'author': 'treborg',
    'author_email': 'treborg@atomix.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/treborg/xpubsub',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
