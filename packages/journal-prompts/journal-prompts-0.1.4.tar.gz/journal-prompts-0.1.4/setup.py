# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['journal_prompts', 'journal_prompts.dto', 'journal_prompts.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock']

setup_kwargs = {
    'name': 'journal-prompts',
    'version': '0.1.4',
    'description': 'Corpus of Random Journal Prompts',
    'long_description': "# Journal Prompts\nA corpus of journal prompts with a finder facade\n\n### Usage\n```python\nfrom journal_prompts import find_random_question\n\nfind_random_question()\n```\nEach function call returns a single random question.\n\n### Results\n```\nWhat's the funniest brand name you've ever seen?\nHave you ever broken a safety rule? What was it?\nWhat's the most ridiculous warning sign you've ever seen?\nHave you ever tried to lick your elbow?\n...\nDo you believe in UFOs, and have you seen one?\n```\n\n### Corpus Size\n```python\nfrom journal_prompts import corpus_size\nassert corpus_size() == 3642\n```\n",
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/journal-prompts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
