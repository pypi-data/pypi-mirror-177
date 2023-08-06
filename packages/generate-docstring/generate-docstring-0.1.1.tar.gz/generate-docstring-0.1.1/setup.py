# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['generate_docstring']

package_data = \
{'': ['*'], 'generate_docstring': ['templates/*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0', 'libcst>=0.4.1,<0.5.0']

setup_kwargs = {
    'name': 'generate-docstring',
    'version': '0.1.1',
    'description': '',
    'long_description': "# Docstring generator\n\n## Install instruction\n\n```bash\n# Install docstring package\npip install .\n\n# Copy vim plugin to vim pack\nmkdir -p ~/.vim/packs/plugins/start\nln -s $PWD/plugins ~/.vim/packs/plugins/start/generate-docstring\n```\n\n## TODO:\n\n* add tox support                       [ ]\n* parse existing docstring              [ ]\n* don't fail if no typing (annotation)  [X]\n* recusrive subscipt (ex: typing.Dict)  [X]\n* add raise on function                 [X]\n* module attribute                      [ ]\n* module name, extract filename         [X]\n\n## Dev tools:\n\n```\npoetry run pylint --rcfile=.pylintrc ./src/\n```\n",
    'author': 'manslaughter03',
    'author_email': 'manslaughter03@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
