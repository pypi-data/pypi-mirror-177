# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.myst_reader']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'docutils>=0.17.0,<=0.18',
 'markdown-word-count>=0.0.1,<0.0.2',
 'myst-parser>=0.18.0,<0.19.0',
 'pelican>=4.5,<5.0',
 'pyyaml>=6.0,<7.0',
 'sphinxcontrib-bibtex>=2.5.0,<2.6.0']

extras_require = \
{'markdown': ['markdown>=3.2.2,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-myst-reader',
    'version': '1.2.0b1',
    'description': "Pelican plugin for converting MyST's Markdown variant to HTML.",
    'long_description': '# MyST Reader: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/ashwinvis/myst-reader/build)](https://github.com/ashwinvis/myst-reader/actions)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ashwinvis/myst-reader/main.svg)](https://results.pre-commit.ci/latest/github/ashwinvis/myst-reader/main)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-myst-reader)](https://pypi.org/project/pelican-myst-reader/)\n![License](https://img.shields.io/pypi/l/pelican-myst-reader?color=blue)\n\nMyST Reader is a [Pelican][] plugin that converts documents written in [MyST’s variant of Markdown][] into HTML.\n\n## Requirements\n\nThis plugin requires:\n\n- Python 3.9 or higher\n\n## Installation\n\nThis plugin can be installed via:\n\n```bash\npython -m pip install pelican-myst-reader\n```\n\n## Configuration\n\nThis plugin converts [MyST’s variant of Markdown][] into HTML. MyST being a\nsuperset of [CommonMark][CommonMark] should cover most Markdown variants, but\nstrictly speaking, conversion from other Markdown variants is unsupported.\nConverting to output formats other than HTML is also unsupported.\n\n### Specifying File Metadata\n\nThe plugin expects all Markdown files to start with a YAML-formatted content header, as shown below.\n\n```yaml\n---\ntitle: "<post-title>"\nauthor: "<author-name>"\ndate: "<date>"\nsummary: |\n  The summary (can be on more than one line)...\n---\n```\n\nIf the values of the metadata can include MyST syntax, in which case, the field\nname should be added to the `FORMATTED_FIELDS` list variable in\n`pelicanconf.py`.\n\n> ⚠️ **Note:** The YAML-formatted header shown above is syntax specific to MyST\n> for specifying content metadata. This maybe different from Pelican’s\n> front-matter format. If you ever decide to stop using this plugin and switch\n> to Pelican’s default Markdown handling, you may need to switch your\n> front-matter metadata to [Python-Markdown’s Meta-Data\n> format](https://python-markdown.github.io/extensions/meta_data/).\n\nAs a compromise and in order to support both metadata formats (although this\nmeans deviating away from MyST standard), title case headers are acceptable.\nThe advantage is that files are compatible with both MyST reader and Pelican\'s\nMarkdown reader.\n\n```yaml\n---\nTitle: "<post-title>"\nAuthor: "<author-name>"\nDate: "<date>"\n---\n```\n\nFor more information on Pelican\'s default metadata format please visit the link below:\n\n- [Pelican’s default metadata format](https://docs.getpelican.com/en/stable/content.html#file-metadata)\n\n### Specifying MyST Options\n\nThe plugin supports passing options to MyST. This is done by\nconfiguring your Pelican settings file (e.g.,\n`pelicanconf.py`):\n\n- `MYST_EXTENSIONS`\n\nIn the `MYST_EXTENSIONS` setting, you may enable/disable any number of the supported [MyST extensions](https://myst-parser.readthedocs.io/en/latest/using/syntax-optional.html):\n\n```python\nMYST_EXTENSIONS = [\n    "amsmath",\n    "dollarmath",\n]\n```\n\n- `MYST_FORCE_SPHINX`\n\nThe Sphinx renderer is automatically used if any math extension is enabled or\nBibTeX files are found. This setting would force Sphinx rendering for all cases\nwhich is slightly slower but has more features.\n\n```py\nMYST_FORCE_SPHINX = True\n```\n\n### Calculating and Displaying Reading Time\n\nThis plugin may be used to calculate the estimated reading time of articles and pages by setting `CALCULATE_READING_TIME` to `True` in your Pelican settings file:\n\n```python\nCALCULATE_READING_TIME = True\n```\n\nYou may display the estimated reading time using the `{{ article.reading_time }}` or `{{ page.reading_time }}` template variables. The unit of time will be displayed as “minute” for reading times less than or equal to one minute, or “minutes” for those greater than one minute.\n\nThe reading time is calculated by dividing the number of words by the reading speed, which is the average number words read in a minute.\n\nThe default value for reading speed is set to 200 words per minute, but may be customized by setting `READING_SPEED` to the desired words per minute value in your Pelican settings file:\n\n```python\nREADING_SPEED = <words-per-minute>\n```\n\nThe number of words in a document is calculated using the [Markdown Word Count](https://github.com/gandreadis/markdown-word-count) package.\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\nSpecial thanks to [Justin Mayer](https://justinmayer.com), [Erwin Janssen](https://github.com/ErwinJanssen), [Joseph Reagle](https://github.com/reagle) and [Deniz Turgut](https://github.com/avaris) for their improvements and feedback on this plugin.\n\n[existing issues]: https://github.com/ashwinvis/myst-reader/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\n## License\n\nThis project is licensed under the AGPL-3.0 license.\n\n[Pelican]: https://getpelican.com\n[MyST’s variant of Markdown]: https://myst-parser.readthedocs.io/en/latest/using/syntax.html\n[CommonMark]: https://commonmark.org/\n',
    'author': 'Ashwin Vishnu',
    'author_email': 'dev@fluid.quest',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ashwinvis/myst-reader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
