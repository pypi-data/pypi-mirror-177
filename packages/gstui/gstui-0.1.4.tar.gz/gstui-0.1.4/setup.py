# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gstui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'blessed>=1.19.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'diskcache>=5.4.0,<6.0.0',
 'google-cloud-storage>=2.5.0,<3.0.0',
 'pyfzf>=0.3.1,<0.4.0',
 'pytermgui>=7.2.0,<8.0.0',
 'tqdm>=4.64.1,<5.0.0']

entry_points = \
{'console_scripts': ['gstui = gstui.gstui:main', 'tests = scripts:test']}

setup_kwargs = {
    'name': 'gstui',
    'version': '0.1.4',
    'description': 'Text User interface for exploring, downloading and uploading files to Google Cloud Storage buckets',
    'long_description': "# Work in progress\n\n# GSTUI\n\nA Text User Interface for exploring Google Cloud Storage. Fast and cached.\n\n## Intallation\n\n```sh\npip install -U gstui\n```\n\nInstall [fzf](https://github.com/junegunn/fzf#installation)\n\n## Usage\n\nRun `gstui` or `gstui --help` to see more options.\n\nLoading buckets or the inital listing for the first time can take a long time to cache. You can create an initial cache of everything with: `gstui -a`.\n\nThe first picker is for selecting the bucket and the second is for selecting the blob to download.\n\n# Development\n\nBe free to submit a PR. Check the formatting with flake8 and for new features try to write tests.\n\n## Tests\n\n\n```sh\npoetry run tests\n```\n\nOr manually\n\n```sh\npoetry run pytest tests -n 4 -vvv\n```\n\n## TODO\n\n- [ ] Better thread management\n- [ ] Don't rely on `time.sleep` for cache tests\n- [ ] [urwid](https://github.com/urwid/urwid) UI\n\n# Related Projects\n\n* [gsutil](https://github.com/GoogleCloudPlatform/gsutil) A command line tool for interacting with cloud storage services. \n* [gcsfuse](https://github.com/GoogleCloudPlatform/gcsfuse) A user-space file system for interacting with Google Cloud Storage \n",
    'author': 'Matheus Fillipe',
    'author_email': 'matheusfillipeag@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
