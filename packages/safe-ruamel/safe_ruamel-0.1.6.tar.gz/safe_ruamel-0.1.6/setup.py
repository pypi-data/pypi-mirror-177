# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['safe_ruamel']
install_requires = \
['ruamel-yaml>=0,<1']

extras_require = \
{'testing': ['pytest>=7.1.2,<8.0.0', 'tox>=3.25.0,<4.0.0']}

setup_kwargs = {
    'name': 'safe-ruamel',
    'version': '0.1.6',
    'description': 'A proxy class for ruamel.yaml.YAML that bypass the thread safety issue.',
    'long_description': '# Safe ruamel.yaml\n\nA proxy class for ruamel.yaml.YAML that bypass the thread-safe issue.\n\n---\n\n## Usage\n\n```python\nfrom safe_ruamel import YAML\n\nyaml = YAML()\n\nobj = yaml.load("a: 1")\nprint(yaml.dump(obj).read())\n```\n',
    'author': 'Wonder',
    'author_email': 'wonderbeyond@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wonderbeyond/safe-ruamel',
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
