# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyprojects']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyprojects',
    'version': '0.0.1',
    'description': 'Python Projects for Humans',
    'long_description': '# pyprojects\n\n[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]\n\nCreate your Python Projects in seconds.\n\n\n\n\n## Installation\n\n```bash\npip install pyprojects\n```\n\n\n\n## Quickstart\n\n```python\nimport pyprojects\n```\n\n\n\n## License\n\npyprojects has a BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/pyprojects/blob/main/LICENSE) file.\n\n\n\n## Contributing\n\n\n\n## Changelog\n\n\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/pyprojects\n\n\n\n[pypi_badge]: https://badgen.net/pypi/v/pyprojects?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/pyprojects',
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pyprojects',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
