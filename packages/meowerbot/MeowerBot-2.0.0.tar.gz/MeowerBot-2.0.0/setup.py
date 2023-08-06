# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['MeowerBot']

package_data = \
{'': ['*']}

install_requires = \
['cloudlink==0.1.7.3', 'requests>=2.28.0,<3.0.0']

setup_kwargs = {
    'name': 'meowerbot',
    'version': '2.0.0',
    'description': 'A meower bot lib for py',
    'long_description': '# MeowerBot.py\n\nA bot lib for Meower\n\n\n## License\n\nsee [LICENSE](./LICENSE)\n\n\n## docs\n\nThe Docs are located [here](./docs/callbacks.md)\n\n\n## Quick Example\n\n```py\n\nfrom MeowerBot import Bot\n\n\nbot = Bot(debug=False)\n\n\ndef handle_db_msg(message: Dict, bot:Bot=bot) -> None:\n\tif message[\'u\'] == "Discord" and ": " in message[\'p\']:\n\t\tmessage[\'u\'] = message[\'p\'].split(": ")[0]\n\t\tmessage[\'p\'] = message[\'p\'].split(": ")[1]\n\n\tif message[\'u\'] == "Webhooks" and ": " in message[\'p\']: # Webhooks should not be supported other then spliting the username off the post (so a webhooks user can still run things)\n\t\tmessage[\'p\'] = message[\'p\'].split(": ")  \n\t\t\nbot.callback("post", handle_db_msg)\n\nbot.start("username", "password")\n\n```\n',
    'author': 'showierdata9978',
    'author_email': '68120127+showierdata9978@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/showierdata9978/MeowerBot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
