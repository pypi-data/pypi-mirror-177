# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpi_remote']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.12.0,<3.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['rpi-remote = rpi_remote.rpi_remote:main']}

setup_kwargs = {
    'name': 'rpi-remote',
    'version': '0.1.0',
    'description': 'Rpi remote client',
    'long_description': '# Install instructions\n\n## Run install script\n```\ncurl -sSL https://gist.githubusercontent.com/radaron/4f844cca0ba09c8521cf13c29fbddfe1/raw | bash\n```\n\n## Edit config\n```\ncp config.ini.sample config.ini\n```\nEdit the relevan fields.\n\n## Start service\n```\nsudo systemctl start rpi_remote\n```\n\n# Check logs\n```\njournalctl -f | grep rpi-remote\n```',
    'author': 'Radics Aron',
    'author_email': 'radics.aron.jozsef@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
