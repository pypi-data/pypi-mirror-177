# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gev']

package_data = \
{'': ['*']}

extras_require = \
{'testing': ['pytest>=7.1.2,<8.0.0', 'tox>=3.25.0,<4.0.0']}

setup_kwargs = {
    'name': 'gev',
    'version': '0.0.1',
    'description': 'General Events Manager',
    'long_description': '# Gev (General Events Manager)\n\n```shell\n$ pip install gev\n```\n\n---\n\n## Usage\n\n```python\nfrom gev import Event, EventManager\n\nmanager = EventManager()\n\ndef handler_1(e):\n    print("handler_1 called with", e)\n\ndef handler_2(e):\n    print("handler_2 called with", e)\n\n# Register event handlers\nmanager.on(\'sys_1::event_a\').do(handler_1)\nmanager.on(\'sys_1::event_b\').do(handler_2)\n\nmanager.take(Event(\n    source=\'sys_1\',\n    type=\'event_a\',\n    payload={\'a\': 1}\n))  # handler_1 will be called\n\nmanager.take(Event(\n    source=\'sys_1\',\n    type=\'event_b\',\n    payload={\'b\': 1}\n))  # handler_1 will be called\n```\n\nIf you don\'t want to initialize an `EventManager` instance,\nyou can use the global `default_manager` and its `on` and `take` methods exposed at module level.\n\n```python\nfrom gev import on, take, Event\n\ndef handler_1(e):\n    print("handler_1 called with", e)\n\non(\'sys_1::event_a\').do(handler_1)\n\ntake(Event(\n    source=\'sys_1\',\n    type=\'event_a\',\n    payload={\'a\': 1}\n))  # handler_1 will be called\n```\n',
    'author': 'Wonder',
    'author_email': 'wonderbeyond@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wonderbeyond/gev',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
