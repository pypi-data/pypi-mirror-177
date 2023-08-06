# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['godoo_rpc', 'godoo_rpc.importers']

package_data = \
{'': ['*']}

install_requires = \
['OdooRPC>=0.8.0,<0.9.0',
 'j-pandas-datalib>=0.0.6,<0.0.7',
 'openpyxl>=3.0.10,<4.0.0',
 'pylint-gitlab>=1.1.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'godoo-rpc',
    'version': '0.0.1',
    'description': 'Helper Functions around OdooRPC',
    'long_description': '# gOdoo-RPC\n\nSeveral Abstraction layers around [OdooRPC](https://odoorpc.readthedocs.io/en/latest/).\n\nMade Possible by: [WEMPE Elektronic GmbH](https://wetech.de)\n\n## Features\n\n- Login to Odoo helper functions\n- Importing Images from the Filesystem\n- Import CSV/Json/Excel Data to Odoo via RPC\n- Import res.config.settings\n- import Translations\n- Extend Base.Import feature with Language cols (fieldname:lang:en_US, fieldname:lang:de_DE)\n- Copy Records from Odoo to Odoo via RPC and remap relational Atributes\n\n## Development\n\n### VS Code Devcontainer\n\nThis workspace contains a [Vscode devcontainer](https://code.visualstudio.com/docs/remote/containers).\n\n### Bump / Release Version\n\n- Trigger [Version Bump](https://github.com/OpenJKSoftware/gOdoo-rpc/actions/workflows/version-bump.yml) pipeline with appropriate target.\n- Merge the created PullRequest. Name: `:shipit: Bump to Version: <versionnumber>`\n- This will create a Tag on `main`\n- Create a release from this Tag. A Pipeline will automatically push to [Pypi](https://pypi.org/project/gOdoo-rpc/)\n',
    'author': 'Joshua Kreuder',
    'author_email': 'joshua_kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenJKSoftware/gOdoo-rpc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
