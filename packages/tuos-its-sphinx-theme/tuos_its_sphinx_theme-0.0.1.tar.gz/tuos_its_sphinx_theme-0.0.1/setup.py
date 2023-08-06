# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tuos_its_sphinx_theme']

package_data = \
{'': ['*'],
 'tuos_its_sphinx_theme': ['static/*',
                                'static/img/*']}

install_requires = \
['Sphinx>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'tuos_its_sphinx_theme',
    'version': '1.0.0',
    'description': 'A Sphinx theme for the Sheffield University IT Services Research IT documentation pages.',
    'long_description': 'A Sphinx theme for the Sheffield University IT Services Research IT documentation pages.',
    'author': 'rcgsheffield',
    'author_email': 'research-it@sheffield.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rcgsheffield/tuos_its_sphinx_theme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}

setup(**setup_kwargs)
