# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itslive']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8',
 'matplotlib>=3.5',
 'multimethod>=1.8',
 'pyproj>=3.3',
 'python-benedict>=0.25',
 's3fs>=2022.3',
 'xarray>=2022.3',
 'zarr>=2.11']

setup_kwargs = {
    'name': 'itslive',
    'version': '0.1.2',
    'description': 'Python client for ITSLIVE gralcier velocity data',
    'long_description': 'None',
    'author': 'betolink',
    'author_email': 'luis.lopez@nsidc.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nasa-jpl/itslive-vortex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
