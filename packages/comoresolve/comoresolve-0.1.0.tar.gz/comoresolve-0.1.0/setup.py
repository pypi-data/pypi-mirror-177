# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comoresolve']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['comoresolve = comoresolve:main']}

setup_kwargs = {
    'name': 'comoresolve',
    'version': '0.1.0',
    'description': 'Utilitário para encontrar soluções para problemas no Python',
    'long_description': '# Como Resolve?\n\nUtilitário para encontrar soluções para problemas no Python.\n\n## Instalação\n\nInstale o pacote `comoresolve`. Exemplo:\n\n```sh\npip install comoresolve\n```\n\n## Uso\n\nUtilize o comando `comoresolve` como se fosse o interpretador do Python. Exemplo:\n\n```sh\n# Para:\npython meu_arquivo.py\n# Execute:\ncomoresolve meu_arquivo.py\n\n# Para:\npython -m meu_modulo\n# Execute:\ncomoresolve -m meu_modulo\n```\n',
    'author': 'Eduardo Klosowski',
    'author_email': 'eduardo_klosowski@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eduardoklosowski/comoresolve',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
