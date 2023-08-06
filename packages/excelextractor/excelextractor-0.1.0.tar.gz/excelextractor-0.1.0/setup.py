# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['excelextractor']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0']

setup_kwargs = {
    'name': 'excelextractor',
    'version': '0.1.0',
    'description': 'ExcelExtractor is an module to handle Excel documents in a normal table format for python',
    'long_description': '# ExcelExtractor\n\nExcelExtractor handles maschine readable data for excel documents\n\nExcelExtrator handles excel worksheet with an headline and data under it.\nIt can read/write from those data and presents them in an maschine readable format in python\nNeeded file Structure in Excel:\n\n```\n|    A    |    B    |    C    | ....\n+---------+---------+---------+-------\n| ... \n+---------+---------+---------+-------\n| Header1 | Header2 | Header3 | ...\n+---------+---------+---------+-------\n| Content | Content | Content | ...\n+---------+---------+---------+-------\n| ...\n```\n\n## Requirements\n\n- Python >= 3.6\n- openpyxl\n\n## Installation\n\nInstall with pip\n\n````\npip install excelextractor\n````\n\n## Documentation\n\nhttps://dcfsec.github.io/excelextractor/\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/dcfSec/SecurityRatConnector/tags). \n\n## Authors\n\n* [dcfSec](https://github.com/dcfSec) - *Initial work*\n\nSee also the list of [contributors](https://github.com/dcfSec/SecurityRatConnector/contributors) who participated in this project.\n\n## License\n\nThis project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details\n\n## ToDo\n\n* Tests\n* Documentation\n',
    'author': 'dcfSec',
    'author_email': 'contributor@dcfsec.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dcfSec/SecurityRatConnector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
