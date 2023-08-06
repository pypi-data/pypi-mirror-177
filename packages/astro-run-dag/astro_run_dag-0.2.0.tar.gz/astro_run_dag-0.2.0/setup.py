# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['run_dag', 'run_dag.utils']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>2.0',
 'astro-sdk-python>=1.2.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['flow = main:app']}

setup_kwargs = {
    'name': 'astro-run-dag',
    'version': '0.2.0',
    'description': 'Empower analysts to build workflows to transform data using SQL',
    'long_description': 'DAG Runner for the Astro CLI\n',
    'author': 'Astronomer',
    'author_email': 'humans@astronomer.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
