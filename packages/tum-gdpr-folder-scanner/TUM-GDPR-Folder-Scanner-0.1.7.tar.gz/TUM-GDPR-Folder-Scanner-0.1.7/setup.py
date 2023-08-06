# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tum_gdpr_folder_scanner']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0',
 'tika>=1.24,<2.0',
 'tqdm>=4.64.1,<5.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tum-gdpr-folder-scanner = '
                     'tum_gdpr_folder_scanner.main:app']}

setup_kwargs = {
    'name': 'tum-gdpr-folder-scanner',
    'version': '0.1.7',
    'description': 'Script to check local folders for GDPR-relevant information in the TUM context.',
    'long_description': '# TUM-GDPR-Folder-Scanner\n\nStudents at the [Technical University of Munich (TUM)](https://www.tum.de/en/) have the right to request to information on personal data after Art. 17 GDPR.\nI wrote this script to check local folders for such information.\n\n## Usage\n\n\n```shell\n$ tum-gdpr-folder-scanner --help\nUsage: tum-gdpr-folder-scanner [OPTIONS] [DIRECTORY]\n\n  Scans all relevant files (CSV, PDF, TXT, XLSX, XML) for the given name, TUM\n  name, and matriculation number.\n\nArguments:\n  [DIRECTORY]  The directory we want to analyze.  [default: .]\n\nOptions:\n  -n, --name-to-search TEXT       The name we are looking for. Please write\n                                  the name in the form `Lastname Firstname` or\n                                  `Firstname Lastname`.\n  -m, --matriculation-no TEXT     The matriculation number we are looking for.\n  -t, --tum-id TEXT               The TUM ID, e.g., ga12acb.\n  -S, --skip-pdfs                 The PDF extraction takes some time. You can\n                                  skip it for a first run.\n  -X, --skip-xlsx                 The XLSX extraction takes some time. You can\n                                  skip it for a first run.\n  -v, --version                   Shows the version and exits.\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n  --help                          Show this message and exit.\n```\n\n## Contact\n\nIf you have any question, please contact [Patrick Stöckle](mailto:patrick.stoeckle@posteo.de).\n',
    'author': 'Patrick Stöckle',
    'author_email': 'patrick.stoeckle@posteo.de',
    'maintainer': 'Patrick Stöckle',
    'maintainer_email': 'patrick.stoeckle@posteo.de',
    'url': 'https://github.com/pstoeckle/TUM-GDPR-Folder-Scanner.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
