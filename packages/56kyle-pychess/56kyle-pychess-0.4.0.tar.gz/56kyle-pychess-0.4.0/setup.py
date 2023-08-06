# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chess']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': '56kyle-pychess',
    'version': '0.4.0',
    'description': 'A python chess engine',
    'long_description': '\n# Pychess\n\n[![Status][status badge]][status badge]\n[![Tests][github actions badge]][github actions page]\n[![Codecov][codecov badge]][codecov page]\n[![Python Version][python version badge]][github page]\n[![License][license badge]][license]\n\n[code of conduct]: https://github.com/56kyle/pychess/blob/master/CODE_OF_CONDUCT.md\n[codecov badge]: https://codecov.io/gh/56kyle/pychess/branch/master/graph/badge.svg?token=0QDENTNTN7\n[codecov page]: https://app.codecov.io/gh/56kyle/pychess/branch/master\n[contributor covenant badge]: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg\n[github actions badge]: https://github.com/56kyle/pychess/workflows/Tests/badge.svg\n[github actions page]: https://github.com/56kyle/pychess/actions?workflow=Tests\n[github page]: https://github.com/56kyle/pychess\n[license badge]: https://img.shields.io/github/license/56kyle/pychess\n[license]: https://opensource.org/licenses/MIT\n[python version badge]: https://img.shields.io/pypi/pyversions/56kyle-pychess\n[status badge]: https://img.shields.io/pypi/status/56kyle-pychess\n\nA chess library written in Python.\n\n\n[Pychess](#Pychess)\n    - [Description](#Description)\n    - [Installation](#Installation)\n    - [Usage](#Usage)\n        - [Game](#Game)\n        - [Board](#Board)\n        - [Move](#Move)\n        - [Piece](#Piece)\n        - [Player](#Player)\n        - [Square](#Square)\n    - [Contributing](#Contributing)\n    - [License](#License)\n\n\n## Installation\n    \n    ```bash\n    # Install from PyPI\n    pip install 56kyle-pychess\n\n    # Install from poetry\n    poetry add 56kyle-pychess\n    ```\n\n## Description\nThe main purpose of this library is to try and practice constantly improving the quality of a codebase instead of allowing complexity to grow with time.\n\nI was mainly inspired by the books "Clean Code" and "Clean Coder" both written by Robert C. Martin. Most of the code in this library is written with the principles of clean code in mind.\n\n### General Design Decisions\n- The Board class is immutable. This means that every time a move is made, a new board is created. This is to prevent the board from being in an invalid state.\n- Moves and most geometry related classes are described in terms of Points and Lines\n- Almost all iterables are sets to allow for hash comparisons of various frozen dataclass based objects\n\n### Simplifications\n- The board may not be infinite\n- The board must be a rectangle\n\n\n## Features\n- [ ] API\n    - [ ] Game\n    - [x] Board\n    - [ ] Move\n    - [x] Piece\n    - [x] Player\n    - [x] Square\n- [ ] Engine\n- [ ] UCI\n- [ ] GUI\n- [ ] Documentation\n\n## Usage\n### Game\n    TODO\n### Board\n    TODO\n### Move\n    TODO\n### Piece\n    TODO\n### Player\n    TODO\n### Square\n    TODO\n    \n\n\n    \n\n\n\n',
    'author': 'kyle',
    'author_email': '56kyleoliver@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/56kyle/pychess',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
