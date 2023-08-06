# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icortex', 'icortex.kernel', 'icortex.services']

package_data = \
{'': ['*'], 'icortex.kernel': ['icortex/*']}

install_requires = \
['Pygments>=2.13.0,<3.0.0',
 'black>=22.10.0,<23.0.0',
 'entrypoints>=0.4,<0.5',
 'importlib-metadata>=4.0.0',
 'ipykernel>=6.16.0,<7.0.0',
 'ipython>=7.0.0',
 'ipywidgets>=8.0.2,<9.0.0',
 'jupyter-client>=7.4.2,<8.0.0',
 'jupyter-console>=6.4.4,<7.0.0',
 'jupyter-core>=4.11.1,<5.0.0',
 'jupyterlab-widgets>=3.0.3,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'urllib3>=1.26.12,<2.0.0']

extras_require = \
{'huggingface': ['onnxruntime>=1.12.1,<2.0.0',
                 'onnx>=1.12.0,<2.0.0',
                 'optimum>=1.4.0,<2.0.0',
                 'transformers>=4.23.1,<5.0.0',
                 'torch>=1.12.1,<2.0.0'],
 'openai': ['openai>=0.23.1,<0.24.0']}

entry_points = \
{'console_scripts': ['icortex = icortex.cli:main']}

setup_kwargs = {
    'name': 'icortex',
    'version': '0.1.3',
    'description': 'Jupyter kernel that can generate Python code from natural language prompts',
    'long_description': '<p align="center">\n    <a href="https://icortex.ai/"><img src="https://raw.githubusercontent.com/textcortex/icortex/main/assets/logo/banner.svg"></a>\n    <br />\n    <br />\n    <a href="https://github.com/textcortex/icortex/workflows/Build/badge.svg"><img src="https://github.com/textcortex/icortex/workflows/Build/badge.svg" alt="Github Actions Status"></a>\n    <a href="https://pypi.org/project/icortex/"><img src="https://img.shields.io/pypi/v/icortex.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="https://pepy.tech/project/icortex"><img src="https://pepy.tech/badge/icortex/month?" alt="Downloads"> </a>\n    <a href="https://icortex.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/icortex/badge/?version=latest" alt="Documentation Status"></a>\n    <a href="https://github.com/textcortex/icortex/blob/main/LICENSE"><img src="https://img.shields.io/github/license/textcortex/icortex.svg?color=blue" alt="License"></a>\n    <a href="https://discord.textcortex.com/"><img src="https://dcbadge.vercel.app/api/server/QtfGgKneHX?style=flat" alt="Discord"></a>\n    <a href="https://twitter.com/TextCortex/"><img src="https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40TextCortex" alt="Twitter"></a>\n    <br />\n    <br />\n    <i>A no-code development framework — Let AI do the coding for you 🦾</i>\n</p>\n<hr />\n\ntl;dr in goes English, out comes Python:\n\nhttps://user-images.githubusercontent.com/2453968/199964302-0dbe1d7d-81c9-4244-a9f2-9d959775e471.mp4\n\nICortex is a no-code development framework that lets you to develop Python programs using plain English. Simply create a recipe that breaks down step-by-step what you want to do in plain English. Our code generating AI will follow your instructions and develop a Python program that suits your needs.\n\n[Create a TextCortex account](https://app.textcortex.com/user/signup?registration_source=icortex) to receive free starter credits and start using ICortex.\n\n## Try it out\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/textcortex/icortex-binder/HEAD?filepath=basic_example.ipynb)\n\nYou can try out ICortex directly in your browser. Launch a Binder instance by clicking [here](https://mybinder.org/v2/gh/textcortex/icortex-binder/HEAD?filepath=basic_example.ipynb), and follow the [instructions in our docs](https://docs.icortex.ai/en/latest/quickstart.html#using-icortex) to get started.\n\nAlternatively, you can use ICortex in Google Colab if you have an account. See [below](#on-google-colab).\n\n[Check out the documentation](https://docs.icortex.ai/) to learn more. [Join our Discord](https://discord.textcortex.com/) to get help.\n\n## Installation\n\n### Locally\n\nInstall directly from PyPI:\n\n```sh\npip install icortex\n# This line is needed to install the kernel spec to Jupyter:\npython -m icortex.kernel.install\n```\n\n### On Google Colab\n\n[Google Colab](https://colab.research.google.com/) is a restricted computing environment that does not allow installing new Jupyter kernels. However, you can still use ICortex by running the following code in a Colab notebook:\n\n```\n!pip install icortex\nimport icortex.init\n```\n\nNote that the package needs to be installed to every new Google Colab runtime—you may need to reinstall if it ever gets disconnected.\n\n## Quickstart\n\n[Click here to get started using ICortex](https://icortex.readthedocs.io/en/latest/quickstart.html).\n\n## Getting help\n\nFeel free to ask questions in our [Discord](https://discord.textcortex.com/).\n\n## Uninstalling\n\nTo uninstall, run\n\n```bash\npip uninstall icortex\n```\n\nThis removes the package, however, it may still leave the kernel spec in Jupyter\'s kernel directories, causing it to continue showing up in JupyterLab. If that is the case, run\n\n```\njupyter kernelspec uninstall icortex -y\n```\n',
    'author': 'TextCortex Team',
    'author_email': 'onur@textcortex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://icortex.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4',
}


setup(**setup_kwargs)
