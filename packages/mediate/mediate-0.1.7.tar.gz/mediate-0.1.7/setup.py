# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediate']

package_data = \
{'': ['*']}

install_requires = \
['roster>=0.1.11,<0.2.0']

setup_kwargs = {
    'name': 'mediate',
    'version': '0.1.7',
    'description': 'Middleware for every occasion',
    'long_description': '# mediate\nMiddleware for every occasion\n\n## Installation\n`mediate` can be installed from [PyPI](https://pypi.org/project/mediate/)\n```console\npip install mediate\n```\n\n## Usage\n### `@middleware`\n```python\nfrom mediate import middleware\n\ndef shout(call_next, name):\n    return call_next(name.upper())\n\ndef exclaim(call_next, name):\n    return call_next(name + "!")\n\n@middleware(shout, exclaim)\ndef hello(name):\n    print(f"Hello, {name}")\n```\n\n```python\n>>> hello("sam")\nHello, SAM!\n```\n\n### `Middleware`\n#### `Middleware.bind`\n```python\nimport mediate\n\nmiddleware = mediate.Middleware()\n\n@middleware\ndef shout(call_next, name):\n    return call_next(name.upper())\n\n@middleware\ndef exclaim(call_next, name):\n    return call_next(name + "!")\n\n@middleware.bind\ndef hello(name):\n    print(f"Hello, {name}")\n```\n\n```python\n>>> hello("sam")\nHello, SAM!\n```\n\n#### `Middleware.compose`\n```python\nimport mediate\n\nmiddleware = mediate.Middleware()\n\n@middleware\ndef shout(call_next, name):\n    return call_next(name.upper())\n\n@middleware\ndef exclaim(call_next, name):\n    return call_next(name + "!")\n\ndef hello(name):\n    print(f"Hello, {name}")\n\ncomposed_hello = middleware.compose(hello)\n```\n\n```python\n>>> hello("sam")\nHello, sam\n>>> composed_hello("sam")\nHello, SAM!\n```',
    'author': 'Tom Bulled',
    'author_email': '26026015+tombulled@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tombulled/middleware',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
