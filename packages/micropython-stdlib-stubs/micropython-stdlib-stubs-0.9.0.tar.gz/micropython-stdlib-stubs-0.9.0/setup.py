# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['builtins']
setup_kwargs = {
    'name': 'micropython-stdlib-stubs',
    'version': '0.9.0',
    'description': "Reduced copy of typeshed's stdlib for use by MicroPython stub packages",
    'long_description': '\nA limited size copy of typesheds stdlib directory. \nhttps://github.com/python/typeshed/tree/main/stdlib\n\nThis is used as a dependency in the micropython-*-stub packages to allow overriding of some of the stdlib modules with micropython specific implementations.\n\nIf you have suggestions or find any issues with the stubs, please report them in the [MicroPython-stubs Discussions](https://github.com/Josverl/micropython-stubs/discussions)\n\nFor an overview of  Micropython Stubs please see: https://micropython-stubs.readthedocs.io/en/main/ \n * List of all stubs : https://micropython-stubs.readthedocs.io/en/main/firmware_grp.html\n\n',
    'author': 'josverl',
    'author_email': 'josverl@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/josverl/micropython-stubs#micropython-stubs',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
