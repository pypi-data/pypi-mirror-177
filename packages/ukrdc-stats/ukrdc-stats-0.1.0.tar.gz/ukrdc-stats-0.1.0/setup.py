# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ukrdc_stats', 'ukrdc_stats.models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.40,<2.0.0',
 'pandas>=1.4.3,<2.0.0',
 'psycopg2-binary>=2.9.3,<3.0.0',
 'pydantic>=1.10.1,<2.0.0',
 'ukrdc-sqla>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'ukrdc-stats',
    'version': '0.1.0',
    'description': 'A package to produce stats from the ukrdc database to be displayed on the dashboard',
    'long_description': '# Dashboard Statistics Library\n\nLibrary for generating statistics for the ukrdc dashboard\n\n[![Test](https://github.com/renalreg/dashboard-stats/actions/workflows/main.yml/badge.svg)](https://github.com/renalreg/dashboard-stats/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/renalreg/dashboard-stats/branch/master/graph/badge.svg?token=Ay8mk0zrKj)](https://codecov.io/gh/renalreg/dashboard-stats)\n\n## Developer notes\n\n### Installation\n\n```bash\npoetry install\n```\n\n### Iterating version numbers\n\nThe library should follow [semantic versioning](https://semver.org/).\n\n[Use Poetry to set the application version.](https://python-poetry.org/docs/cli/#version)\n\nE.g. `poetry version patch` for fix releases, `poetry version minor` for new functionality releases, or `poetry version major` for breaking-change releases.\n\n### Running the demo notebooks\n\nInstall additional demo notebook dependencies with\n\n```bash\npoetry install --with demo\n```\n',
    'author': 'Philip Main',
    'author_email': 'Philip.Main@renalregistry.nhs.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/renalreg/dashboard-stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
