# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dagon',
 'dagon.ar',
 'dagon.cache',
 'dagon.core',
 'dagon.db',
 'dagon.event',
 'dagon.ext',
 'dagon.fs',
 'dagon.http',
 'dagon.inspect',
 'dagon.option',
 'dagon.persist',
 'dagon.pool',
 'dagon.proc',
 'dagon.script_mode',
 'dagon.storage',
 'dagon.task',
 'dagon.tool',
 'dagon.ui',
 'dagon.util']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.4.0,<5.0.0']

extras_require = \
{':python_version < "3.10"': ['importlib-metadata'],
 'http': ['aiohttp>=3.8.3,<4.0.0']}

entry_points = \
{'console_scripts': ['dagon = dagon.tool.main:start',
                     'dagon-inspect = dagon.inspect.main:start'],
 'dagon.extensions': ['dagon.cache = dagon.cache:_Ext',
                      'dagon.db = dagon.db:_DatabaseExt',
                      'dagon.events = dagon.event:_EventsExt',
                      'dagon.http = dagon.http:_Ext',
                      'dagon.options = dagon.option:_OptionsExt',
                      'dagon.persist = dagon.persist:_PersistExt',
                      'dagon.pools = dagon.pool:_PoolsExt',
                      'dagon.storage = dagon.storage:_Ext',
                      'dagon.ui = dagon.ui:_Ext'],
 'dagon.uis': ['dagon.ui.fancy = dagon.ui.fancy:FancyUI',
               'dagon.ui.simple = dagon.ui.simple:SimpleUI']}

setup_kwargs = {
    'name': 'dagon',
    'version': '0.10.1',
    'description': 'An asynchronous task graph execution system',
    'long_description': '# Dagon - An Asynchronous Task Graph Execution Engine\n\n*Dagon* is a job execution system designed for speed, flexibility,\nexpressiveness, and correctness with two overarching goals in mind:\n\n1. It should be *easy* to use *correctly*.\n2. It should be *hard* to use *incorrectly*.\n\nDagon itself can be used as a development tool, a CI tool, an application\nframework, or a library for creating declarative task-graph programs and\npipelines.\n\nFor more information, refer to the `docs/` subdirectory.\n',
    'author': 'vector-of-bool',
    'author_email': 'vectorofbool@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vector-of-bool/dagon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
