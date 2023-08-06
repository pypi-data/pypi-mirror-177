# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyvarium', 'pyvarium.cli', 'pyvarium.installers', 'pyvarium.util']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'dynaconf>=3.1.4,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pyaml>=21.8.3,<22.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'rich>=10.7.0,<11.0.0',
 'rtoml>=0.8.0,<0.9.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['pyvarium = pyvarium.cli:app']}

setup_kwargs = {
    'name': 'pyvarium',
    'version': '0.1.0',
    'description': 'Tool for managing mixed Spack and pip packages',
    'long_description': 'None',
    'author': 'Robert Rosca',
    'author_email': '32569096+RobertRosca@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
