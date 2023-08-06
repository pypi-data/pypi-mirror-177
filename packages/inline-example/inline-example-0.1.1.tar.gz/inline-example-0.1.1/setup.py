# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inline_example', 'inline_example.examples']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'inline-example',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Inline Example\n\nGenerates an inline example for your end users.  \n\n**Example Usage**  \nTo see an example of how to use Inline Example, run the following in a python script:  \n\n```\nfrom inline_example.examples import example_usage\nexample_usage()\n```',
    'author': 'MBeebe',
    'author_email': 'pyn-sol@beebe.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
