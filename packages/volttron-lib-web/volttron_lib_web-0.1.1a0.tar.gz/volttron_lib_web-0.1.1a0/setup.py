# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['volttron', 'volttron.services.web']

package_data = \
{'': ['*'],
 'volttron.services.web': ['static/*',
                           'static/js/*',
                           'static/specs/*',
                           'templates/*']}

install_requires = \
['PyJWT==1.7.1',
 'argon2-cffi>=21.3.0,<22.0.0',
 'passlib>=1.7.4,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'treelib>=1.6.1',
 'volttron>=10.0.a42,<11.0',
 'werkzeug>=2.1.2',
 'ws4py>=0.5.1']

setup_kwargs = {
    'name': 'volttron-lib-web',
    'version': '0.1.1a0',
    'description': '',
    'long_description': "VOLTTRON™ is an open source platform for distributed sensing and control. The platform provides services for collecting and storing data from buildings and devices and provides an environment for developing applications which interact with that data.\n\n[![Run Pytests](https://github.com/eclipse-volttron/volttron-lib-web/actions/workflows/run-test.yml/badge.svg)](https://github.com/eclipse-volttron/volttron-lib-web/actions/workflows/run-test.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron.svg)](https://pypi.org/project/volttron-core/)\n\n## Installation with Web\n\n```bash\n> pip install volttron-lib-web\n```\n\n### Quick Start\n\n 1. Start the platform\n    ```bash\n    > volttron -vv -l volttron.log &>/dev/null &\n    ```\n\n 2. Install listener agent\n    ```bash\n    > vctl install volttron-listener\n    ```\n\n 3. View status of platform\n    ```bash\n    > vctl status\n    ```\n\n 4. Shutdown the platform\n    ```bash\n    > vctl shutdown --platform\n    ```\n\nFull VOLTTRON documentation available at [VOLTTRON Readthedocs](https://volttron.readthedocs.io)\n\n## Contributing to VOLTTRON\n\nPlease see the [contributing.md](CONTRIBUTING.md) document before contributing to this repository.\n\n## Development of VOLTTRON\n\n### Environment\n\nVOLTTRON uses [Poetry](https://python-poetry.org/), a dependency management and packaging tool for Python. If you don't have Poetry installed on your machine, follow [these steps](https://python-poetry.org/docs/#installation) to install it on your machine.\n\nTo check if Poetry is installed, run `poetry --version`. If you receive the error 'command not found: poetry', add the following line to your '~/.bashrc' script: ```export PATH=$PATH:$HOME/.poetry/bin```.\n\n#### Recommended configuration for poetry\n\nBy default, poetry creates a virtual environment in {cache-dir}/virtualenvs. To configure 'poetry' to create the virtualenv inside this project's root directory, run the following command:\n\n[```poetry config virtualenvs.in-project true```](https://python-poetry.org/docs/configuration)\n\n### Setup\n\n 1. Clone the repository\n    ```bash\n    git clone https://github.com/VOLTTRON/volttron-core -b develop\n    ```\n\n 1. cd into volttron-core directory\n    ```bash\n    cd volttron-core\n    ```\n\n 1. Install volttron into the current directory\n    ```bash\n    poetry install\n    ```\n\n 1. Run tests\n    ```bash\n    poetry run pytest\n    ```\n\n 1. Activate environment (removes the need for add poetry run to all commands)\n    ```bash\n    poetry shell\n    ```\n\n 1. Run volttron\n    ```bash\n    volttron -vv -l volttron.log &>/dev/null &\n    ```\n\n### Using modules to run VOLTTRON\n\nIn order to run VOLTTRON from within an ide the recommended way is to run the platform using the modules\n\n ```bash\n > poetry shell\n > python -m volttron.server -vv -l volttron.log &\n > python -m volttron.commands.control -vv status\n```\n\nPlease see the [contributing.md](CONTRIBUTING.md) document before contributing to this repository.\n\nHappy Editing!\n",
    'author': 'Craig Allwardt',
    'author_email': 'craig.allwardt@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://volttron.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
