# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icb',
 'icb.helper',
 'icb.helper.db',
 'icb.helper.ml',
 'icb.helper.ts',
 'icb.main',
 'icb.task']

package_data = \
{'': ['*'], 'icb': ['data/*']}

install_requires = \
['click==8.1.3',
 'commonmark==0.9.1',
 'joblib==1.2.0',
 'kallisto==1.0.9',
 'pandas==1.5.1',
 'pillow==9.3.0',
 'pygments==2.13.0',
 'python-dateutil==2.8.2',
 'pytz==2022.6',
 'rdkit==2022.9.1',
 'rich==12.6.0',
 'scikit-learn==1.1.1',
 'scipy==1.9.2',
 'six==1.16.0',
 'threadpoolctl==3.1.0']

entry_points = \
{'console_scripts': ['sobo = icb.main.main:main']}

setup_kwargs = {
    'name': 'sobo',
    'version': '0.2.0',
    'description': 'Regioselectivity of the iridium-catalyzed borylation.',
    'long_description': '# Environment setup\nStart with setting up a new `conda` virtual environment (venv)\n\n```bash\n> conda create --name sobo python=3.9\n```\n\nand activate the created venv\n\n```bash\n> conda activate sobo\n```\n\n# Install dependencies\nGet `openbabel` and `xtb` dependencies\n\n```bash\n> conda install -c conda-forge openbabel\n...\n> conda install -c conda-forge xtb\n...\n```\n\nThen install the SoBo method\n\n```bash\n> pip install sobo\n```\n',
    'author': 'Caldeweyher, Eike',
    'author_email': 'e.caldeweyher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
