# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyraingen', 'pyraingen.data', 'pyraingen.fortran_daily']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2', 'netCDF4>=1.6.2', 'numba>=0.56.4', 'numpy>=1.23.5']

setup_kwargs = {
    'name': 'pyraingen',
    'version': '0.1.0',
    'description': 'A package for stochastically generating daily and subdaily rainfall with ifd constaining.',
    'long_description': '# pyraingen\n\nA package for stochastically generating daily and subdaily rainfall with ifd constaining.\n\n## Installation\n\n```bash\n$ pip install pyraingen\n```\n\n## Usage\n\n`pyraingen` can be used to stochastically generate regionalised daily rainfall, disaggregate daily rainfall to subdaily fragments and constrain generated rainfall to observed or predicted Intensity Frequency Duration (IFD) relationships.\nThe three main functions are:\n\n```python\nfrom pyraingen.regionaliseddailysim import regionaliseddailysim\nfrom pyraingen.regionalisedsubdailysim import regionalisedsubdailysim\nfrom pyraingen.ifdcond import ifdcond\n```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`pyraingen` was created by Caleb Dykman. Caleb Dykman retains all rights to the source and it may not be reproduced, distributed, or used to create derivative works.\n\n## Credits\n\n`pyraingen` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Caleb Dykman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
