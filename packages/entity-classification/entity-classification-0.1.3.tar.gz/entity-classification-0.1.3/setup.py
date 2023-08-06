# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entity_classification',
 'entity_classification.bp',
 'entity_classification.dmo',
 'entity_classification.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'entity-classification',
    'version': '0.1.3',
    'description': 'Perform Intent Classification using a list of Entities',
    'long_description': "# entity-classification\n\nPerform Entity Classification via two inputs: `entity_names: list` and `input_tokens: list`\n\nAssume you wish to classify `network_topology` and you have these tokens extracted from your text:\n```python\n[\n    'edge',\n    'network',\n    'moderate',\n    'cat5',\n    'topology',\n    'locate'\n]\n```\n\nUse this code\n```python\nfrom entity_classification import classify\n\nclassify(entity_names=['network_topology'], input_tokens=input_tokens)\n```\n\nThe result will be\n```python\n{\n    'result': ['network_topology'],\n    'tokens': ['network', 'topology']\n}\n```\n",
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/entity-classification',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
