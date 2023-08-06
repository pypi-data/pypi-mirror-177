# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['helm_yaml_tui']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'ruamel.yaml>=0.17.21,<0.18.0', 'textual==0.5.0']

entry_points = \
{'console_scripts': ['helm-yaml-tui = helm_yaml_tui.main:main']}

setup_kwargs = {
    'name': 'helm-yaml-tui',
    'version': '0.1.3',
    'description': 'TUI navigator for rendered Helm YAML output with tree navigation and syntax highlighting',
    'long_description': 'None',
    'author': 'Adrian Rumpold',
    'author_email': 'a.rumpold@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
