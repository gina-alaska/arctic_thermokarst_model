"""
setup script
"""
from setuptools import setup,find_packages
import atm

config = {
    'description': 'Arctic thermokarst model ',
    'author': 'Rawser Spicer',
    'url': atm.__codeurl__,
    'author_email': atm.__email__ ,
    'version': atm.__version__,
    'install_requires': ['numpy','pyyaml', 'gdal', 'matplotlib', 'pandas', 'scipy', 'numba' ],
    'packages': find_packages(),
    'scripts': [],
    'package_data': {},
    'name': 'Arctic thermokarst model'
}

setup(**config)
