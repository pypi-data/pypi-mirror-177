# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_sentence_classify',
 'fast_sentence_classify.core',
 'fast_sentence_classify.core.bp',
 'fast_sentence_classify.core.dmo',
 'fast_sentence_classify.core.svc',
 'fast_sentence_classify.datablock',
 'fast_sentence_classify.datablock.dmo',
 'fast_sentence_classify.datablock.dto',
 'fast_sentence_classify.datablock.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'spacy==3.3']

setup_kwargs = {
    'name': 'fast-sentence-classify',
    'version': '0.1.6',
    'description': 'Generic Sentence Classification Service',
    'long_description': '# Fast Sentence Classification (fast-sentence-classify)\n\n## Sample Usage\n```python\nfrom fast_sentence_classify import classify\n\nd_result = classify("I\'d like it if you could give me some directions to the library")\n```\nResult:\n```json\n{\n   "data":{\n      "input_text":"I\'d like it if you could give me some directions to the library",\n      "output_text":"WHERE_LOCATION"\n   },\n   "event":"fast-sentence-classify",\n   "service":"classify",\n   "stopwatch":"117.30μs",\n   "ts":"1666897985.085184"\n}\n```\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/fast-sentence-classify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
