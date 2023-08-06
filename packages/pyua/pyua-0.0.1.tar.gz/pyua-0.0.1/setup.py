# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyua']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyua',
    'version': '0.0.1',
    'description': 'User Agents for Humans',
    'long_description': '# PyUA\n\n[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]\n\nGenerate your user agents in seconds.\n\n\n\n\n## Installation\n\n```bash\npip install pyua\n```\n\n\n\n## Quickstart\n\n```python\nimport pyua\n```\n\n\n\n## License\n\nPyUA has a BSD license, as found in the [LICENSE](https://github.com/imyizhang/pyua/blob/main/LICENSE) file.\n\n\n\n## Contributing\n\n\n\n## Changelog\n\n\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/pyua\n\n\n\n[pypi_badge]: https://badgen.net/pypi/v/pyua?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/pyua',
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/pyua',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
