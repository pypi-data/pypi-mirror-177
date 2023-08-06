# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['will_not_work_on_windows_try_from_wsl_instead']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'will-not-work-on-windows-try-from-wsl-instead',
    'version': '0.1.0',
    'description': '',
    'long_description': '# will-not-work-on-windows-try-from-wsl-instead\n\nThis is a placeholder package used for preventing installation on Windows for\npackages that are known to not work on Windows.\n\nIf you have a Python package that only supports Unix-like systems, like Linux\n or MacOS, you can add this package as a dependency to prevent installation on\npure-Windows.\n\n```ini\n# setup.cfg\n\n[options]\ninstall_requires =\n  # Special order section for helping pip:\n  will-not-work-on-windows-try-from-wsl-instead; platform_system=="Windows"\n  ...\n```\n',
    'author': 'Sorin Sbarnea',
    'author_email': 'ssbarnea@redhat.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
