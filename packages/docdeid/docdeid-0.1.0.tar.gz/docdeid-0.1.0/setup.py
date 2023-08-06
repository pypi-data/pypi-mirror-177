# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docdeid', 'docdeid.ds', 'docdeid.process', 'docdeid.str']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.1,<2.0.0']

setup_kwargs = {
    'name': 'docdeid',
    'version': '0.1.0',
    'description': 'Create your own document de-identifier using docdeid, a simple framework independent of language or domain.',
    'long_description': '# docdeid\n\n[![tests](https://github.com/vmenger/docdeid/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/vmenger/docdeid/actions/workflows/test.yml)\n[![coverage](https://coveralls.io/repos/github/vmenger/docdeid/badge.svg?branch=main)](https://coveralls.io/github/vmenger/docdeid?branch=main)\n[![build](https://github.com/vmenger/docdeid/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/vmenger/docdeid/actions/workflows/build.yml)\n[![Documentation Status](https://readthedocs.org/projects/docdeid/badge/?version=latest)](https://docdeid.readthedocs.io/en/latest/?badge=latest)\n![pypy version](https://img.shields.io/pypi/v/docdeid)\n![python versions](https://img.shields.io/pypi/pyversions/docdeid)\n![license](https://img.shields.io/github/license/vmenger/docdeid)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[Installation](#installation) - [Getting started](#getting-started) - [Features](#features) - [Documentation](#documentation) - [Development and contributiong](#development-and-contributing) - [Authors](#authors)  \n\n<!-- start include in docs -->\n\nCreate your own document de-identifier using `docdeid`, a simple framework independent of language or domain.\n\n> Note that `docdeid` is still on version 0.x.x, and breaking changes might occur. If you plan to do extensive work involving `docdeid`, feel free to get in touch to coordinate. \n\n## Installation\n\nGrab the latest version from PyPi:\n\n```bash\npip install docdeid\n```\n\n## Getting started\n\n```python\nfrom docdeid import DocDeid\nfrom docdeid.tokenize import WordBoundaryTokenizer\nfrom docdeid.process SingleTokenLookupAnnotator, RegexpAnnotator, SimpleRedactor\n\ndeidentifier = DocDeid()\n\ndeidentifier.tokenizers["default"] = WordBoundaryTokenizer()\n\ndeidentifier.processors.add_processor(\n    "name_lookup",\n    SingleTokenLookupAnnotator(lookup_values=["John", "Mary"], tag="name"),\n)\n\ndeidentifier.processors.add_processor(\n    "name_regexp",\n    RegexpAnnotator(regexp_pattern=re.compile(r"[A-Z]\\w+"), tag="name"),\n)\n\ndeidentifier.processors.add_processor(\n    "redactor", \n    SimpleRedactor()\n)\n\ntext = "John loves Mary, but Mary loves William."\ndoc = deidentifier.deidentify(text)\n```\n\nFind the relevant info in the `Document` object:\n\n```python\nprint(doc.annotations)\n\nAnnotationSet({\n    Annotation(text=\'John\', start_char=0, end_char=4, tag=\'name\', length=4),\n    Annotation(text=\'Mary\', start_char=11, end_char=15, tag=\'name\', length=4),\n    Annotation(text=\'Mary\', start_char=21, end_char=25, tag=\'name\', length=4), \n    Annotation(text=\'William\', start_char=32, end_char=39, tag=\'name\', length=7)\n})\n```\n\n```python\nprint(doc.deidentified_text)\n\n\'[NAME-1] loves [NAME-2], but [NAME-2] loves [NAME-3].\'\n```\n\n## Features\n\nAdditionally, `docdeid` features: \n\n- Ability to create your own `Annotator`, `AnnotationProcessor`, `Redactor` and `Tokenizer` components\n- Some basic re-usable components included (e.g. regexp, token lookup, token patterns)\n- Callable from one interface (`DocDeid.deidenitfy()`)\n- String processing and filtering\n- Fast lookup based on sets or tries\n- Anything you add! PRs welcome.\n\nFor a more in-depth tutorial, see: [docs/tutorial](https://docdeid.readthedocs.io/en/latest/tutorial.html)\n\n<!-- end include in docs -->\n\n## Documentation\n\nFor full documentation and API, see: [https://docdeid.readthedocs.io/en/latest/](https://docdeid.readthedocs.io/en/latest/)\n\n## Development and contributing\n\nFor setting up dev environment, see: [docs/environment](https://docdeid.readthedocs.io/en/latest/environment.html)\n\nFor contributing, see: [docs/contributing](https://docdeid.readthedocs.io/en/latest/contributing.html).\n\n## Authors\nVincent Menger - *Author, maintainer*\n',
    'author': 'Vincent Menger',
    'author_email': 'vmenger@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
