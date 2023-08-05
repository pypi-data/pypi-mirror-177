# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataurls']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dataurls',
    'version': '0.0.1',
    'description': 'Data URLs for Humans',
    'long_description': '# dataurls\n\n[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]\n\ndataurls is \n\n* a very simple but fully featured Data URL (also known as data URI) encoder for Python.\n* written in Python Standard Library\n\ndataurls supports to\n\n* encode data in Data URLs\n\n\n\n\n## Installation\n\n```bash\npip install dataurls\n```\n\n\n\n## Quickstart\n\n```python\nimport dataurls\n```\n\n\n\n## License\n\ndataurls has a BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/dataurls/blob/main/LICENSE) file.\n\n\n\n## Contributing\n\n\n\n## Changelog\n\n\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/dataurls\n\n\n\n[pypi_badge]: https://badgen.net/pypi/v/dataurls?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/dataurls',
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/dataurls',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
