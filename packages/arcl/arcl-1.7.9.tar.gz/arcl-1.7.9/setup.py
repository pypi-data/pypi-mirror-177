# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcl']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'msal-extensions>=1.0.0,<2.0.0',
 'msal>=1.10.0,<2.0.0',
 'requests']

entry_points = \
{'console_scripts': ['arcl = arcl.cli:cli']}

setup_kwargs = {
    'name': 'arcl',
    'version': '1.7.9',
    'description': 'The CLI for Archimedes',
    'long_description': "# Archimedes CLI\n\nThe Archimedes CLI tool is used to bootstrap archimedes projects. The projects are based on a template available \n[here](https://github.com/OptimeeringAS/archimedes-cookiecutter/).\n\nThe CLI tool also helps you authenticate using your organization credentials and get credentials to access the \n[Archimedes API](https://github.com/OptimeeringAS/archimedes-api/) and the database.\n\n## Installation\n\nArchimedes-cli can be installed on Linux, macOS and Windows. Follow the instructions for your operating system:\n* [Install arcl on Linux](install-arcl-on-linux.md)\n* [Install arcl on macOS](install-arcl-on-macos.md)\n* [Install arcl on Windows](install-arcl-on-windows.md)\n\n\n## Post-installation setup\n\nAfter installation of arcl tool, you will need to install and configure some other tools to be able to use arcl on your\noperating system. Please follow the instructions below:\n* [Post-install setup on Linux](post-install-linux.md)\n* [Post-install setup on macOS](post-install-macos.md)\n* [Post-install setup on Windows](post-install-windows.md)\n\n## Usage\n\n```shell\narcl --help\n```\n\n#### Login\n\nTo login to Archimedes, which is required for using it, run the following command and follow the on-screen instructions:\n\n```shell\narcl auth login optimeering\n```\n\nTo login to the DEV environment:\n```shell\narcl auth logout\nENVIRONMENT=dev arcl auth login optimeering\n```\n\n## Dev setup\n\n```shell\npyenv shell 3.10.8\npip install --upgrade pip wheel\npyenv rehash\npoetry install\npoetry shell\narcl --help\n```\n\n## Publishing releases\n\nA new release can be made by \n[creating a release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) \nusing the GitHub web interface.\n\nWhen the release it created, as long as the tag naming convention is followed, it is automatically built and published \nto pypi by GitHub Actions, which is configured in the [.github/workflows](.github/workflows) in this repo. Please refer \nto the following instructions when making releases:\n\n* Make sure that [pyproject.toml](pyproject.toml) is updated with a new version. We use \n[semantic versioning](https://semver.org/). Make sure the version hasn't already been published to \n[pypi](https://pypi.org/project/arcl/#history). \n* Go to the [Releases page](/releases) of the project\n* Click the `Create a new release` button\n* Click on `Choose a tag` and in the input field, enter `release/cli/v{VERSION_NUMBER_FROM_pyproject.toml}`, for e.g. \n`release/v1.2.3`. This tag name should NOT already exist, so it will NOT appear in the dropdown menu which appears as \nyou enter text. You need to click on `Create new tag release/cli/v{VERSION_NUMBER_FROM_pyproject.toml} on publish` to create \nthe tag.\n* In the release title, write `v{VERSION_NUMBER_FROM_pyproject.toml}`, for e.g. `v1.2.3`.\n* In Release Notes, ideally, we should write the titles of all the Shortcut stories and link to them.\n* Click on the `Publish Release` button.\n* Then, check that the [release pipeline](/actions) is running and wait for it to complete successfully.\n* Verify the release is [published to pypi](https://pypi.org/project/arcl/#history).\n* New arcl version has now been released.\n* Then, you are ready to build and publish the Windows distribution of arcl, which we currently perform manually. See\n[here](arcl-win/README.md) for instructions on how to do that.\n",
    'author': 'Optimeering AS',
    'author_email': 'dev@optimeering.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
