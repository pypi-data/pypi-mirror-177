# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pivuq']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.3,<0.57.0',
 'numpy>=1.23.4,<2.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'pivuq',
    'version': '0.4.1',
    'description': 'A library for PIV Uncertainty Quantification',
    'long_description': '# PIVUQ: PIV Uncertainty Quantification\n\n[![Docs](https://img.shields.io/readthedocs/pivuq?style=flat-square&labelColor=000000)](https://pivuq.readthedocs.io/)\n[![PyPi Version](https://img.shields.io/pypi/v/pivuq.svg?style=flat-square&labelColor=000000)](https://pypi.org/project/pivuq/)\n[![PyPi Python versions](https://img.shields.io/pypi/pyversions/pivuq.svg?style=flat-square&labelColor=000000)](https://pypi.org/project/pivuq/)\n[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square&labelColor=000000)](#license)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.6458153-blue?style=flat-square&labelColor=000000)](https://doi.org/10.5281/zenodo.6458153)\n\n## Description\n\nThis package contains python implementations of uncertainty quantification (UQ) for Particle Image Velocimetry (PIV). Primary aim is to implement UQ algorithms for PIV techniques. Future goals include possible extensions to other domains including but not limited to optical flow and BOS.\n\nList of approachs:\n\n- [`pivuq.diparity.ilk`](https://pivuq.readthedocs.io/en/latest/api/disparity.html#pivuq.disparity.ilk): Iterative Lucas-Kanade based disparity estimation. [[scikit-image](https://scikit-image.org/docs/dev/api/skimage.registration.html#skimage.registration.optical_flow_ilk)]\n- [`pivuq.disparity.sws`](https://pivuq.readthedocs.io/en/latest/api/disparity.html#pivuq.disparity.ilk): Python implementation of Sciacchitano, A., Wieneke, B., & Scarano, F. (2013). PIV uncertainty quantification by image matching. *Measurement Science and Technology, 24* (4). [https://doi.org/10.1088/0957-0233/24/4/045302](https://doi.org/10.1088/0957-0233/24/4/045302). [[piv.de](http://piv.de/uncertainty/)]\n\n\n## Installation\n\nInstall using pip\n\n```bash\npip install pivuq\n```\n\n### Development mode\n\nInitialize [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html) environment\n\n```bash\nconda env create -f environment.yml\n```\n\nInstall packages using [`poetry`](https://python-poetry.org/docs/):\n\n```bash\npoetry install\n```\n\n## How to cite\n\n*Work in progress* version: https://doi.org/10.5281/zenodo.6458153\n\nIn future, please cite the following paper:\n\n> Manickathan et al. (2022). PIVUQ: Uncertainty Quantification Toolkit for Quantitative Flow Visualization. *in prep*.\n',
    'author': 'MrLento234',
    'author_email': 'lento.manickathan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lento234/pivuq',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
