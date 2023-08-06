# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stage_left']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stage-left',
    'version': '0.1.1',
    'description': '',
    'long_description': '# stage-left\n\n[![Run tests](https://github.com/chris48s/stage-left/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/chris48s/stage-left/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/chris48s/stage-left/branch/master/graph/badge.svg?token=XS70M8EPCT)](https://codecov.io/gh/chris48s/stage-left)\n[![PyPI Version](https://img.shields.io/pypi/v/stage-left.svg)](https://pypi.org/project/stage-left/)\n![License](https://img.shields.io/pypi/l/stage-left.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fstage-left%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n[[x]it!](https://xit.jotaen.net/) is a plain-text file format for todos and check lists. Stage-left parses [x]it! documents into rich python objects.\n\n## Installation\n\n```\npip install stage-left\n```\n\n## Usage\n\n### Parse checklist from file\n\n```py\nfrom stage_left import parse_file, ParseError\n\nwith open("/path/to/checklist.xit") as fp:\n    try:\n        checklist = parse_file(fp)\n        print(checklist)\n    except ParseError:\n        raise\n```\n\n### Parse checklist from string\n\n```py\nfrom stage_left import parse_text, ParseError\n\ntext = """\n[ ] Open\n[x] Done\n"""\n\ntry:\n    checklist = parse_text(text)\n    print(checklist)\nexcept ParseError:\n    raise\n```\n\n## Implementation notes\n\nDue dates specified using the numbered week syntax e.g: `2022-W01` are parsed assuming Monday is the first day of the week. All days in a new year preceding the first Monday are considered to be in week 0 (`W00`).\n',
    'author': 'chris48s',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chris48s/stage-left',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
