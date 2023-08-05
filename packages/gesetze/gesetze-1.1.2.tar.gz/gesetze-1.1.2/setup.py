# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gesetze', 'gesetze.drivers', 'gesetze.scrapers']

package_data = \
{'': ['*'], 'gesetze': ['data/*']}

extras_require = \
{'cli': ['click>=8,<9', 'lxml>=4,<5', 'requests>=2,<3']}

entry_points = \
{'console_scripts': ['gesetze = gesetze.cli:cli']}

setup_kwargs = {
    'name': 'gesetze',
    'version': '1.1.2',
    'description': 'Linking german legal norms, dependency-free & GDPR-friendly',
    'long_description': '# py-gesetze\n[![License](https://badgen.net/badge/license/GPL/blue)](https://codeberg.org/S1SYPHOS/py-gesetze/src/branch/main/LICENSE) [![PyPI](https://badgen.net/pypi/v/gesetze)](https://pypi.org/project/gesetze) [![Build](https://ci.codeberg.org/api/badges/S1SYPHOS/py-gesetze/status.svg)](https://codeberg.org/S1SYPHOS/py-gesetze/issues)\n\nLinking german legal norms, dependency-free & GDPR-friendly. `py-gesetze` automatically transforms legal references into `a` tags - batteries included.\n\nThis project is a Python port of the PHP library [`php-gesetze`](https://github.com/S1SYPHOS/php-gesetze).\n\n\n## Installation\n\nIt\'s available from [PyPi](https://pypi.org/project/gesetze) using `pip`:\n\n```text\npip install gesetze\n```\n\n\n## Getting started\n\nUsing this library is straightforward.\n\n\n### Commandline\n\nPretty much self-explanatory - otherwise, `--help` is your friend:\n\n```text\n$ gesetze --help\nUsage: gesetze [OPTIONS] COMMAND [ARGS]...\n\n  Utilities for indexing & analyzing german legal norms\n\nOptions:\n  -v, --verbose  Enable verbose mode.\n  --version      Show the version and exit.\n  --help         Show this message and exit.\n\nCommands:\n  analyze  Analyzes legal norm\n  build    Builds index\n  clear    Clears download cache\n```\n\n\n### Package\n\nThe underlying module may also be used directly:\n\n```python\nfrom gesetze import Gesetz, analyze\n\n# Initialize it\nobj = Gesetz()\n\n# Configure it\nobj.title = \'normal\'\n\n# Convert legal references\nprint(obj.gesetzify(\'This text references Art. 1 GG.\'))\n\n# "This text references <a class="hover:underline" href="https://www.gesetze-im-internet.de/gg/art_1.html" title="Grundgesetz für die Bundesrepublik Deutschland">Art. 1 GG</a>."\n\nprint(analyze(\'§ 433 Abs. 2 BGB\'))\n\n# {\'norm\': \'433\', \'absatz\': \'2\', \'gesetz\': \'BGB\'}\n```\n\n\n## Usage\n\n### Class `Gesetz`\n\n#### `__init__(drivers: typing.Union[str, list])`\n\n`drivers` controls the providers (and their respective order) to be used, either `str` or `list`.\n\n**Note:** This defaults to all available drivers, which is a good overall choice, simply because of the vast array of supported laws. However, possible values are `gesetze`, `\'dejure\'`, `\'buzer\'` and `\'lexparency\'`.\n\n\n#### `gesetzify(string: str, callback: typing.Callable) -> str`\n\nTransforms legal references into HTML link tags\n\n**Note:** For more flexibility, you may use your own `callback` method as second parameter of `gesetzify`. Callbacks are being passed the [`re.Match`](https://docs.python.org/3/library/re.html#match-objects) object representing matched legal norms. This way, you could highlight them using `<strong>` tags instead of converting them into `a` tags. Default: `obj.linkify`\n\nExample: Inside the callback function, the `match` for \'§ 433 Abs. 2 BGB\' (`match.group(0)`) would give a dictionary like `{\'norm\': \'433\', \'absatz\': \'2\', \'satz\': None, \'nr\': None, \'lit\': None, \'gesetz\': \'BGB\'}` (eg using `match.groupdict()`).\n\n**Note:** For convenience, a [Markdown](https://en.wikipedia.org/wiki/Markdown) callback is included and may be used like this: `obj.gesetzify(\'your-text\', obj.markdownify)`\n\n\n### Helpers\n\n#### `analyze(string: str) -> dict`\n\nAnalyzes a single legal norm\n\n\n#### `extract(string: str) -> list`\n\nExtracts legal norms as list of strings\n\n\n#### `roman2arabic(string: str)`\n\nConverts roman numerals to arabic numerals (static method)\n\n\n## Configuration\n\nThe `gesetzify` command may be configured through the following options:\n\n\n### `obj.attributes (dict)`\n\nDefines HTML attribute defaults. Default: `{\'target\': \'_blank\'}`\n\n\n### `obj.title (False|str)`\n\nControls `title` attribute. Default: `False`\n\nPossible values:\n\n- `light`: abbreviated law (eg \'GG\')\n- `normal`: complete law (eg \'Grundgesetz\')\n- `full`: official heading (eg \'Art 45d Parlamentarisches Kontrollgremium\')\n\n\n## Contributing\n\nIf you want to get your hands dirty, this will download the repository and install `py-gesetze` along its dependencies inside a virtual environment, ready for action:\n\n```bash\n# Clone repository & change directory\ngit clone https://codeberg.org/S1SYPHOS/py-gesetze && cd py-gesetze\n\n# Set up & activate virtualenv\npoetry shell\n\n# Install dependencies\npoetry install\n```\n\n\n## Credits\n\nThis library is based on ..\n\n- .. an adapted (and somewhat improved) version of the [`jura_regex`](https://github.com/kiersch/jura_regex) regex package by Philipp Kiersch.\n- .. an adapted (and somewhat modified) version of the [`gesetze`](https://github.com/matejgrahovac/gesetze) crawler package by Matej Grahovac.\n\n\n## Special Thanks\n\nI\'d like to thank everybody that\'s making free & open source software - you people are awesome. Also I\'m always thankful for feedback and bug reports :)\n',
    'author': 'Digitalbüro',
    'author_email': 'post@digitalbuero.eu',
    'maintainer': 'Martin Folkers',
    'maintainer_email': 'hello@twobrain.io',
    'url': 'https://digitalbuero.eu',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
