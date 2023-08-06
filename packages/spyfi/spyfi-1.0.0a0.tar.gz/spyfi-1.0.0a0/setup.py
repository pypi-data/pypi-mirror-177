# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['spyfi']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1']

setup_kwargs = {
    'name': 'spyfi',
    'version': '1.0.0a0',
    'description': 'Spyfi',
    'long_description': '# Spyfi\n\n[![PyPI](https://img.shields.io/pypi/v/spyfi.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/spyfi.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/spyfi)][python version]\n[![License](https://img.shields.io/pypi/l/spyfi)][license]\n\n[![Read the documentation at https://spyfi.readthedocs.io/](https://img.shields.io/readthedocs/spyfi/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/bobthemighty/spyfi/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/bobthemighty/spyfi/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/spyfi/\n[status]: https://pypi.org/project/spyfi/\n[python version]: https://pypi.org/project/spyfi\n[read the docs]: https://spyfi.readthedocs.io/\n[tests]: https://github.com/bobthemighty/spyfi/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/bobthemighty/spyfi\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nA quick and dirty way to turn your existing classes into spies.\n\n## Why though?\n\nI very often create spies for my tests by wrapping an interface around a list, eg.\n\n```python\nclass FakeEmailSender(list):\n\n    def send(self, address: str, message: str) -> None:\n        self.append((address, message))\n\n\ndef test_when_a_customer_signs_up():\n\n    sender = FakeEmailSender()\n    handler = SignupHandler(sender)\n\n    handler("user@domain.com", "password")\n\n    assert (("user@domain.com", "welcome to the website")) in sender\n```\n\nSometimes this is a little fiddly, particularly if you need to spy on a hierarchy of objects. Spyfi, pronounced "spiffy", is a quick way to instrument a python object graph and capture calls made to it.\n\n## Installation\n\nYou can install _Spyfi_ via [pip] from [PyPI]:\n\n```console\n$ pip install spyfi\n```\n\n## Usage\n\n```python\nfrom spyfi import Spy\n\n\nclass Thing:\n\n    def __init__(self, colour):\n        self.colour = colour\n\n    def say_hello(self, message):\n        print(f"Hello, I am a {self.colour} thing: {message})\n\n\nclass ThingFactory:\n\n    def make_thing(self, colour:str) -> Thing:\n        return Thing(colour)\n\n\ndef test_thing_messages():\n\n    # Spiffy takes any old object and wraps its methods\n    # so that an arbitrary callback receives args and kwargs.\n    # In this case, we\'re appending all calls to a list.\n    spy = Spy(ThingFactory())\n\n    # The returned object is otherwise unchanged. `factory` is a real\n    # ThingFactory and behaves as normal.\n    factory = spy.target\n    factory.make_thing("blue").say_hello("I like python")\n\n    # Since we have access to the calls list, we can assert that\n    # particular methods were called with the right data.\n    assert len(spy.calls) == 2\n    assert calls[0].method == "make_thing"\n    assert calls[0].args == ("blue",)\n\n    # Spyfi includes a helper method to make assertions easier\n    assert spy.has("say_hello")\n    assert spy.has("say_hello", "I like python")\n```\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Spyfi_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/bobthemighty/spyfi/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/bobthemighty/spyfi/blob/main/LICENSE\n[contributor guide]: https://github.com/bobthemighty/spyfi/blob/main/CONTRIBUTING.md\n[command-line reference]: https://spyfi.readthedocs.io/en/latest/usage.html\n',
    'author': 'Bob Gregory',
    'author_email': 'bob@codefiend.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bobthemighty/spyfi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
