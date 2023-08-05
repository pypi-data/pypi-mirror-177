# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_fixture_ref']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytest-fixture-ref',
    'version': '0.0.2',
    'description': 'Lets users reference fixtures without name matching magic.',
    'long_description': '# pytest fixture ref\n\n[![PyPI](https://img.shields.io/pypi/v/pytest-fixture-ref?style=flat-square)](https://pypi.python.org/pypi/pytest-fixture-ref/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-fixture-ref?style=flat-square)](https://pypi.python.org/pypi/pytest-fixture-ref/)\n[![PyPI - License](https://img.shields.io/pypi/l/pytest-fixture-ref?style=flat-square)](https://pypi.python.org/pypi/pytest-fixture-ref/)\n[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)\n\n\n---\n\n**Documentation**: [https://rtaycher.github.io/pytest-fixture-ref](https://rtaycher.github.io/pytest-fixture-ref)\n\n**Source Code**: [https://github.com/rtaycher/pytest-fixture-ref](https://github.com/rtaycher/pytest-fixture-ref)\n\n**PyPI**: [https://pypi.org/project/pytest-fixture-ref/](https://pypi.org/project/pytest-fixture-ref/)\n\n---\n\n## Let developers reference pytest fixtures without name matching magic.\n\nPass fixtures via default value or decorator args instead of magic strings.\n\nLet me admit this is a bit of a hack.\nIt might be important to note that this still uses pytests usual magic string matching under the covers\nby grabbing the function name and re-writing the function.\nThat means you do have to make sure pytest imports it by installing it/specifying it in pytest_plugins/etc\nas well as importing it for reference.\nIt also means this technically works with fake/dummy functions with the same name\n(in case you can\'t easily import some fixtures)\n\n\n\nexample:\n\n    from pytest_fixture_ref import using_fixtures_from_defaults, using_fixtures_from_kwargs\n\n    @using_fixtures_from_defaults\n    def test_bar1(_=fix_w_yield1, __=fix_w_yield2, tmp=tmp_path):\n        assert tmp.exists()\n\n\n    @using_fixtures_from_kwargs(_=fix_w_yield1, __=fix_w_yield2, tmp=tmp_path)\n    def test_bar2(_, __, tmp):\n        assert tmp.exists()\n\n\nYou can also use it to reference fixtures from other fixtures\n\n    @pytest.fixture\n    def first_entry():\n        return "a"\n\n\n    @pytest.fixture\n    @using_fixtures_from_defaults\n    def order(fe=first_entry):\n        return [fe]\n\n## Installation\n\n```sh\npip install git+https://github.com/rtaycher/pytest-fixture-ref.git\n\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Testing\n\n```sh\npytest\n```\n\n### Documentation\n\nThe documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings\n of the public signatures of the source code. The documentation is updated and published as a [Github project page\n ](https://pages.github.com/) automatically as part each release.\n\n### Releasing\n\nTrigger the [Draft release workflow](https://github.com/rtaycher/pytest-fixture-ref/actions/workflows/draft_release.yml)\n(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.\n\nFind the draft release from the\n[GitHub releases](https://github.com/rtaycher/pytest-fixture-ref/releases) and publish it. When\n a release is published, it\'ll trigger [release](https://github.com/rtaycher/pytest-fixture-ref/blob/master/.github/workflows/release.yml) workflow which creates PyPI\n release and deploys updated documentation.\n\n### Pre-commit\n\nPre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality\n checks to make sure the changeset is in good shape before a commit/push happens.\n\nYou can install the hooks with (runs for each commit):\n\n```sh\npre-commit install\n```\n\nOr if you want them to run only for each push:\n\n```sh\npre-commit install -t pre-push\n```\n\nOr if you want e.g. want to run all checks manually for all files:\n\n```sh\npre-commit run --all-files\n```\n\n---\n\nThis project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.\n',
    'author': 'Roman A. Taycher',
    'author_email': 'rtaycher.devmail@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://rtaycher.github.io/pytest-fixture-ref',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
