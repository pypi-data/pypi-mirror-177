# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ignorer']

package_data = \
{'': ['*'],
 'ignorer': ['gitignore/*',
             'gitignore/.github/*',
             'gitignore/Global/*',
             'gitignore/community/*',
             'gitignore/community/AWS/*',
             'gitignore/community/DotNet/*',
             'gitignore/community/Elixir/*',
             'gitignore/community/GNOME/*',
             'gitignore/community/Golang/*',
             'gitignore/community/Java/*',
             'gitignore/community/JavaScript/*',
             'gitignore/community/Linux/*',
             'gitignore/community/PHP/*',
             'gitignore/community/Python/*',
             'gitignore/community/embedded/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'inflect>=6.0.2,<7.0.0',
 'inquirerpy>=0.3.4,<0.4.0',
 'pyperclip>=1.8.2,<2.0.0']

entry_points = \
{'console_scripts': ['ignorer = ignorer.ignorer:cli']}

setup_kwargs = {
    'name': 'ignorer',
    'version': '0.0.3',
    'description': '',
    'long_description': '',
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
