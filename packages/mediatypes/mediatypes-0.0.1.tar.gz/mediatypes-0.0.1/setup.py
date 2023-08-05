# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediatypes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mediatypes',
    'version': '0.0.1',
    'description': 'Media Types for Humans',
    'long_description': '# mediatypes\n\n[![GitHub][github_badge]][github_link] [![PyPI][pypi_badge]][pypi_link]\n\nmediatypes is \n\n* a very simple but fully featured media type (also known as MIME type) mapper for Python.\n* written in Python Standard Library\n\nmediatypes supports to\n\n* map filenames to media types\n\n\n\n\n## Installation\n\n```bash\npip install mediatypes\n```\n\n\n\n## Quickstart\n\n```python\nimport mediatypes\n```\n\n\n\n## License\n\nmediatypes has a BSD-3-Clause license, as found in the [LICENSE](https://github.com/imyizhang/mediatypes/blob/main/LICENSE) file.\n\n\n\n## Contributing\n\n\n\n## Changelog\n\n\n\n[github_badge]: https://badgen.net/badge/icon/GitHub?icon=github&color=black&label\n[github_link]: https://github.com/imyizhang/mediatypes\n\n\n\n[pypi_badge]: https://badgen.net/pypi/v/mediatypes?icon=pypi&color=black&label\n[pypi_link]: https://www.pypi.org/project/mediatypes',
    'author': 'Yi Zhang',
    'author_email': 'yizhang.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/mediatypes',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
