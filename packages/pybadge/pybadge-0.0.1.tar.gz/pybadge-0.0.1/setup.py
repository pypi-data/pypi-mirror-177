# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybadge']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybadge',
    'version': '0.0.1',
    'description': 'Badges for Humans',
    'long_description': '# PyBadge\n\n[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]\n\nGenerate your badges in seconds.\n\n\n\n\n## Installation\n\n```bash\npip install pybadge\n```\n\n\n\n## Quickstart\n\n```python\nimport pybadge\n```\n\n\n\n## License\n\nPyBadge has a BSD license, as found in the [LICENSE](https://github.com/imyizhang/pybadge/blob/main/LICENSE) file.\n\n\n\n## Contributing\n\n\n\n## Changelog\n\n\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/pybadge\n\n\n\n[pypi_badge]: https://badgen.net/pypi/v/pybadge?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/pybadge',
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pybadge',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
