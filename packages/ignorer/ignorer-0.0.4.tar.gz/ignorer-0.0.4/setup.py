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
    'version': '0.0.4',
    'description': 'Generate .gitignore files from your command line',
    'long_description': "# ignorer\n\nignorer generates .gitignore files from your command line using\nGitHub's [vast repository](https://github.com/github/gitignore) of .gitignore templates.\n\n## Installation\n\n### pipx (recommended)\n\nThe recommended, cross-platform, way of installing ignorer is via [pipx](https://pypa.github.io/pipx/).\n\n```bash\npipx install ignorer\n```\n\n### Homebrew\n\nmacOS users who would rather install via [Homebrew](https://brew.sh) can do that instead:\n\n```bash\nbrew tap celsiusnarhwal/formulae\nbrew install ignorer\n```\n\n### pip (not recommended)\n\nignorer can be installed via pip like any other Python package, but unless you're going to make a virtual environment\nfor it yourself, you're strongly encouraged to use pipx or Homebrew.\n\n```bash\npip install ignorer\n```\n\n## Usage\n\nSimply invoke ignorer from the command line:\n\n```bash\nignorer\n```\n\nThat's it. ignorer will interactively guide you through the rest.\n\nSee it in action below.\n\n![A GIF demonstrating the usage of ignorer.](media/demonstration.gif)]\n\n# Acknowledgements\n\nignorer's functionality is largely based on JetBrains' [.ignore plugin](https://github.com/JetBrains/idea-gitignore)\nfor their IDEs.\n\n## License\n\nignorer is licensed under the [MIT License](LICENSE.md).\n",
    'author': 'celsius narhwal',
    'author_email': 'hello@celsiusnarhwal.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/celsiusnarhwal/ignorer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
