# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rtui', 'rtui.commands']

package_data = \
{'': ['*']}

install_requires = \
['astoria>=0.11.1,<0.12.0', 'prompt-toolkit>=3.0.31,<4.0.0']

entry_points = \
{'console_scripts': ['rtui = rtui.app:app']}

setup_kwargs = {
    'name': 'rtui',
    'version': '0.1.1',
    'description': 'Robot Terminal User Interface for Student Robotics Kit',
    'long_description': '# RTUI - Robot Terminal User Interface\n\nA TUI for [Astoria](https://github.com/srobo/astoria)-driven robots.\n\n[![asciicast](https://asciinema.org/a/NJoUTaZ0G7VcotlNVgL7iXufR.svg)](https://asciinema.org/a/NJoUTaZ0G7VcotlNVgL7iXufR)\n\n## Usage\n\nThe `rtui` command can be used standalone by running `rtui`.\n\nIt can also be used as an SSH forced command by adding the following to the `authorized_keys` file:\n\n```\ncommand="/usr/bin/rtui" ssh-ed25519 AAAA....\n```\n\n### Available Commands\n\n- `arena`: Get or set the current arena\n- `exit`: Leave the terminal session.\n- `help`: Show available commands\n- `kill`: Kill running code\n- `metadata`: Show all robot metadata\n- `mode`: Get or set the current robot mode (COMP or DEV)\n- `quit`: Leave the terminal session.\n- `restart`: Restart running code\n- `start`: Trigger the virtual start button\n- `trigger`: Trigger the virtual start button\n- `zone`: Get or set the current zone\n\n\n## Development\n\nThis application is written in Python 3.8+ and is managed using poetry.\n\n```shell\npoetry install\npoetry run rtui\n```\n\nYou will need to have an instance of Astoria running for some functionality, the docker setup is recommended for this.',
    'author': 'Dan Trickey',
    'author_email': 'srobo-rtui@trickey.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/srobo/robot-tui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
