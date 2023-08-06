# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cunnypy']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0', 'httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'cunnypy',
    'version': '1.0.0',
    'description': 'A python library for several image boards',
    'long_description': '<h1 align="center">🦀 Cunny.py 🦀</h1>\n\n<h3 align="center">A python library for several image boards</h3>\n\n<p align="center">\n    <a href="https://liberapay.com/GlitchyChan/donate">\n        <img src="https://img.shields.io/badge/Liberapay-F6C915?style=for-the-badge&logo=liberapay&logoColor=black" alt="liberapay" />\n    </a>\n    <a href="https://discord.gg/ZxbYHEh">\n        <img src="https://img.shields.io/badge/Discord-5865F2?logo=discord&logoColor=fff&style=for-the-badge" alt="Discord" />\n    </a>\n    <a href="https://twitter.com/glitchychan">\n        <img src="https://img.shields.io/badge/twitter-%2300acee?&style=for-the-badge&logo=twitter&logoColor=white" alt="twitter" />\n    </a>\n</p>\n\n---\n\n<p align="center">\n    <a href="#about">About</a> •\n    <a href="#features">Features</a> •\n    <a href="#usage">Development</a>\n</p>\n\n## **About**\nThis library is to make it much easier to interact with image boards with python.\n\n## **Features**\n- 🔁 Fully Async\n- 🔥 Blazingly Fast™️\n- 💯 Supports many sites with aliases (see [sites.json](./cunnypy/sites.json))\n- 🎱 Supports random search\n- ⚙️ 1 simple import to get going\n\n## **Usage**\nTo get started with cunny.py simply import the library and use the search function\n\nExample search with gelbooru\n```python\nimport cunnypy\n\nposts = await cunnypy.search("gel", tags=["megumin"])\nprint(posts)\n```\nThis will print out a list of [Post](./cunnypy/classes.py#L30-L80) classes which you can then manipulate\n\n\nOther examples can be found in the [Examples](./examples) folder\n',
    'author': 'Glitchy',
    'author_email': 'thepatheticweebgamer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/CunnyTech/Cunnypy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
