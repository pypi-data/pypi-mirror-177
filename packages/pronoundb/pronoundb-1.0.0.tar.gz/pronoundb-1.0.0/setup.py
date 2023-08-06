# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pronoundb']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0']

setup_kwargs = {
    'name': 'pronoundb',
    'version': '1.0.0',
    'description': 'API wrapper for pronoundb.org',
    'long_description': '# PronounDB Python API\n\nPython API for the PronounDB API.\n\n## Installation\n\n```bash\npip install pronoundb\n```\n\n## Examples\n\nlookup someones pronouns by their discord id:\n\n```py\nfrom pronoundb import lookup, Platform\n\nlookup(Platform.DISCORD, 123456789012345678)\n# -> {123456789012345678: ["he", "him"]}\n```\n\nlookup someones pronouns by their minecraft (java) uuid:\n\n```py\nfrom pronoundb import lookup, Platform\n\nlookup(Platform.MINECRAFT, "12345678-1234-1234-1234-123456789012")\n# -> {"12345678-1234-1234-1234-123456789012": ["they", "them"]}\n```\n\nlookup multiple users pronouns by their discord id:\n\n```py\nfrom pronoundb import lookup, Platform\n\nlookup(Platform.DISCORD, [123456789012345678, 987654321098765432])\n# -> {123456789012345678: ["he", "him"], 987654321098765432: ["she", "her"]}\n```\n\n## Supported Platforms\n\n- Discord\n- Facebook\n- GitHub\n- Minecraft (Java)\n- Twitch\n- Twitter\n\n## Contributing\n\nContributions to this library are always welcome and highly encouraged.\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.\n',
    'author': 'SteffoSpieler',
    'author_email': 'steffo@steffospieler.de',
    'maintainer': 'SteffoSpieler',
    'maintainer_email': 'steffo@steffospieler.de',
    'url': 'https://gitlab.com/SteffoSpieler/pronoundb-library',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
