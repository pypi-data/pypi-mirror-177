# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xsentinels']

package_data = \
{'': ['*']}

install_requires = \
['typing-inspect>=0,<1']

setup_kwargs = {
    'name': 'xsentinels',
    'version': '1.2.0',
    'description': 'Sentinels for Defaults, Null and for creating sentinels/singletons.',
    'long_description': "![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10&color=blue?style=flat-square&logo=python)\n![PyPI version](https://badge.fury.io/py/xsentinels.svg?)\n\n\n\n# Overview\n\nVarious objects that allow for sentinel-like singletons for various purposes, including:\n\n- Ones pre-defined in this library:\n  - Default\n  - Null\n- Also, Easily create your own custom singletons/sentinels types.\n\n**[📄 Detailed Documentation](https://xyngular.github.io/py-xsentinels/latest/)** | **[🐍 PyPi](https://pypi.org/project/xsentinels/)**\n\n# Install\n\n```bash\n# via pip\npip install xsentinels\n\n# via poetry\npoetry add xsentinels\n```\n\n# Quick Start\n\n```python\nfrom xsentinels import Default\nimport os\n\ndef my_func(my_param = Default):\n    if my_param is Default:\n        # Resolve default value for parameter, otherwise None.\n        my_param = os.environ.get('MY_PARAM', None)\n    ...\n```\n\n# Licensing\n\nThis library is licensed under the MIT-0 License. See the LICENSE file.\n",
    'author': 'Josh Orr',
    'author_email': 'josh@orr.blue',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyngular/py-xsentinels',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
