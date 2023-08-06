# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mielib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mielib',
    'version': '0.1.1',
    'description': '',
    'long_description': '# MieLib\n\nLibrary which contains many Mie-ralated functions in optics and acoustics. In particular:\n- Scattering Mie coefficients for isotropic spheres:\n    -  Acoustic Mie coefficients based on Phys. Rev. Lett. 123, 183901 (2019) (see SM)\n    - Optics Mie coefficients based on Bohren Huffmann book.\n- Scalar spherical harmonics\n- Vector spherical harmonics (complex and real)\n\n\n## Credits\nIvan Toftul \n\n`toftul.ivan@gmail.com`\n',
    'author': 'Ivan Toftul',
    'author_email': 'toftul.ivan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
