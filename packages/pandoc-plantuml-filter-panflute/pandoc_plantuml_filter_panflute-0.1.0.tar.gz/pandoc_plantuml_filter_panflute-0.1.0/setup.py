# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandoc_plantuml_filter_panflute']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'panflute>=2.2.3,<3.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['pandoc-plantuml = pandoc_plantuml_filter_panflute:main']}

setup_kwargs = {
    'name': 'pandoc-plantuml-filter-panflute',
    'version': '0.1.0',
    'description': '',
    'long_description': "# pandoc-plantuml-filter\n\nPandoc filter which converts PlantUML code blocks to PlantUML images.\n\n````\n```plantuml\nAlice -> Bob: Authentication Request\nBob --> Alice: Authentication Response\n\nAlice -> Bob: Another authentication Request\nAlice <-- Bob: another authentication Response\n```\n````\n\n## Usage\n\nInstall it with pip:\n\n```\npip install pandoc-plantuml-filter\n```\n\nAnd use it like any other pandoc filter:\n\n```\npandoc tests/sample.md -o sample.pdf --filter pandoc-plantuml\n```\n\nThe PlantUML binary must be in your `$PATH` or can be set with the\n`PLANTUML_BIN` environment variable.\n\n### Additional parameters\n\nYou could pass additional parameters into `plantuml` filter which will be processed as picture's options:\n\n````\n```{ .plantuml height=50% plantuml-filename=test.png }\nAlice -> Bob: Authentication Request\nBob --> Alice: Authentication Response\n```\n````\n\nThe `plantuml-filename` parameter create a symlink for the destination picture, which could be used in the same file as an image directly.\n\n## But there is ...\n\nThere are a few other filters trying to convert PlantUML code blocks however\nthey all failed for me.\n",
    'author': 'Augusto Zanellato',
    'author_email': 'augusto.zanellato@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
