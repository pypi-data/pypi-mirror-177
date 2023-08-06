# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_flash']

package_data = \
{'': ['*'], 'starlette_flash': ['templates/starlette_flash/*']}

install_requires = \
['starlette']

setup_kwargs = {
    'name': 'starlette-flash',
    'version': '0.2.0',
    'description': 'Flash messages for Starlette framework.',
    'long_description': "# Starlette-Flash\n\nFlash messages for Starlette framework.\n\n![PyPI](https://img.shields.io/pypi/v/starlette_flash)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/starlette_flash/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/starlette_flash)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/starlette_flash)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/starlette_flash)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/starlette_flash)\n\n## Installation\n\nInstall `starlette_flash` using PIP or poetry:\n\n```bash\npip install starlette_flash\n# or\npoetry add starlette_flash\n```\n\n## Quick start\n\nSee example application in [examples/](examples/) directory of this repository.\n\n## Setup\n\nYou must install SessionMiddleware to use flash messages.\n\n## Flashing messages\n\nTo flash a message use `flash` helper.\n\n```python\nfrom starlette_flash import flash\n\n\ndef index_view(request):\n    flash(request).add('This is a message.', 'success')\n\n```\n\n### Using helpers\n\nThere are several predefined helpers exists which automatically set the category:\n\n- success\n- error\n- info\n- debug\n\n```python\nfrom starlette_flash import flash\n\n\ndef index_view(request):\n    flash(request).success('This is a message.')\n    flash(request).error('This is a message.')\n    flash(request).info('This is a message.')\n    flash(request).debug('This is a message.')\n\n```\n\n## Reading messages\n\nTo get current flash messages without removing them from session, use `all` method:\n\n```python\nfrom starlette_flash import flash\n\n\ndef index_view(request):\n    flash(request).success('This is a message.')\n\n    messages = flash(request).all()\n    print(messages)  # {'category': 'success', 'message': 'This is a message.'}\n\n```\n\n## Consuming messages\n\nYou can read messages one by one and then clear the storage by using `consume` method.\n\n```python\nfrom starlette_flash import flash\n\n\ndef index_view(request):\n    flash(request).success('This is a message.')\n\n    messages = []\n    for message in flash(request).consume():\n        messages.append(message)\n    print(messages)  # {'category': 'success', 'message': 'This is a message.'}\n    print(flash(request).all())  # empty, messages has been consumed\n\n```\n\nYou can iterate the flash bag to consume messages as well:\n\n```python\nfrom starlette_flash import flash\n\n\ndef index_view(request):\n    flash(request).success('This is a message.')\n\n    messages = []\n    for message in flash(request):\n        messages.append(message)\n    print(messages)  # {'category': 'success', 'message': 'This is a message.'}\n    print(flash(request).all())  # empty, messages has been consumed\n\n```\n",
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alex-oleshkevich/starlette_flash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<4.0.0',
}


setup(**setup_kwargs)
