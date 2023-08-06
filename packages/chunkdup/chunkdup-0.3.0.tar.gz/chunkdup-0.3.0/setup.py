# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunkdup']

package_data = \
{'': ['*']}

install_requires = \
['chunksum']

entry_points = \
{'console_scripts': ['chunkdiff = chunkdup.chunkdiff:main',
                     'chunkdup = chunkdup.chunkdup:main']}

setup_kwargs = {
    'name': 'chunkdup',
    'version': '0.3.0',
    'description': 'Find (partial content) duplicate files.',
    'long_description': '# chunkdup\n\nFind (partial content) duplicate files using [chunksum](https://github.com/xyb/chunksum) outputs.\n\n[![test](https://github.com/xyb/chunkdup/actions/workflows/test.yml/badge.svg)](https://github.com/xyb/chunkdup/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/xyb/chunkdup/branch/main/graph/badge.svg?token=TVFUKMLFMX)](https://codecov.io/gh/xyb/chunkdup)\n[![Maintainability](https://api.codeclimate.com/v1/badges/0935f557916da1fdcddb/maintainability)](https://codeclimate.com/github/xyb/chunkdup/maintainability)\n[![Latest version](https://img.shields.io/pypi/v/chunkdup.svg)](https://pypi.org/project/chunkdup/)\n[![Support python versions](https://img.shields.io/pypi/pyversions/chunkdup)](https://pypi.org/project/chunkdup/)\n\n```\nFind (partial content) duplicate files.\n\nUsage: chunkdup <chunksums_file1> <chunksums_file2>\n\nExamples:\n\n  $ chunksum dir1/ -f chunksums.dir1\n  $ chunksum dir2/ -f chunksums.dir2\n  $ chunkdup chunksums.dir1 chunksums.dir2\n',
    'author': 'Xie Yanbo',
    'author_email': 'xieyanbo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/xyb/chunkdup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
