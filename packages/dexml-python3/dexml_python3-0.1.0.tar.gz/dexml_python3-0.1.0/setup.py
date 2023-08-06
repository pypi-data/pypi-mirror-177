# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dexml', 'dexml.fields']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dexml-python3',
    'version': '0.1.0',
    'description': 'A dead-simple xml object mapper for Python',
    'long_description': '# dexml: An Object-XML Mapper for Python\n\nThis is a maintained version of the original `dexml` Python package, intended for Python 3 use only.\n\nOther than providing a maintained version that supports modern Python 3, other future goals include:\n - support with Python dataclasses and `pydantic` models\n - support for auto-generating models based on example XML payloads\n - keep backwards compatibility with original `dexml` package where possible\n\nBefore refactoring, the original code was sourced from both:\n - https://github.com/realrunner/dexml\n - https://github.com/rfk/dexml\n\n## Documentation\n\nLet\'s face it: xml is a fact of modern life. I\'d even go so far as to say\nthat it\'s *good* at what it does. But that doesn\'t mean it\'s easy to work\nwith and it doesn\'t mean that we have to like it. Most of the time, XML\njust needs to get out of the way and let you do some actual work instead\nof writing code to traverse and manipulate yet another DOM.\n\nThe dexml module takes the obvious mapping between XML tags and Python objects\nand lets you capture that as cleanly as possible. Loosely inspired by Django\'s\nORM, you write simple class definitions to define the expected structure of\nyour XML document. Like so::\n\n```\n  >>> import dexml\n  >>> from dexml import fields\n  >>> class Person(dexml.Model):\n  ...   name = fields.String()\n  ...   age = fields.Integer(tagname=\'age\')\n```\n\nThen you can parse an XML document into an object like this::\n\n```\n  >>> p = Person.parse("<Person name=\'Foo McBar\'><age>42</age></Person>")\n  >>> p.name\n  u\'Foo McBar\'\n  >>> p.age\n  42\n```\n\nAnd you can render an object into an XML document like this::\n\n```\n  >>> p = Person(name="Handsome B. Wonderful",age=36)\n  >>> p.render()\n  \'<?xml version="1.0" ?><Person name="Handsome B. Wonderful"><age>36</age></Person>\'\n```\n\nMalformed documents will raise a ParseError::\n\n```\n  >>> p = Person.parse("<Person><age>92</age></Person>")\n  Traceback (most recent call last):\n      ...\n  ParseError: required field not found: \'name\'\n```\n\nOf course, it gets more interesting when you nest Model definitions, like this::\n\n```\n  >>> class Group(dexml.Model):\n  ...   name = fields.String(attrname="name")\n  ...   members = fields.List(Person)\n  ...\n  >>> g = Group(name="Monty Python")\n  >>> g.members.append(Person(name="John Cleese",age=69))\n  >>> g.members.append(Person(name="Terry Jones",age=67))\n  >>> g.render(fragment=True)\n  \'<Group name="Monty Python"><Person name="John Cleese"><age>69</age></Person><Person name="Terry Jones"><age>67</age></Person></Group>\'\n```\n\nThere\'s support for XML namespaces, default field values, case-insensitive\nparsing, and more fun stuff. Check out the documentation on the following\nclasses for more details:\n\n```\n  :Model:  the base class for objects that map into XML\n  :Field:  the base class for individual model fields\n  :Meta:   meta-information about how to parse/render a model\n```\n\n## Development\n\nThe project uses [poetry](https://python-poetry.org/) to manage dependencies, virtual environments, and publishing.\n\nIt also uses `pre-commit` to provide some standard git hook checks.\n\nThe `Makefile` has some shortcuts for common operations. After cloning, the following steps can be taken:\n1. Run `make restore`\n2. Optionally enter virtual environment with `poetry shell`\n3. Run `make test`\n4. Run `make build` to create a distribution\n\n## Contributing\n\nThis is an early stage project but pull requests are welcome.\n',
    'author': 'Patrick Withams',
    'author_email': 'pwithams@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pwithams/dexml-python3',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
