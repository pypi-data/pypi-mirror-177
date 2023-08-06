# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transfers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'transfers',
    'version': '0.0.1',
    'description': 'Transfers for Humans',
    'long_description': '# transfers\n\n[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]\n\nShare your data in seconds.\n\n\n\n\n## Installation\n\n```bash\npip install transfers\n```\n\n\n\n## Quickstart\n\n```python\nimport transfers\n```\n\n\n\n## License\n\ntransfers has a BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/transfers/blob/main/LICENSE) file.\n\n\n\n## Contributing\n\n\n\n## Changelog\n\n\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/transfers\n\n\n\n[pypi_badge]: https://badgen.net/pypi/v/transfers?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/transfers',
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/transfers',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
