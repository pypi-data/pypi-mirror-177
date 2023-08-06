#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)

VERSION = "1.0.0-beta.1"
DESCRIPTION = 'Plugin to monkey patch web3.py to support cfx2eth-bridge'
with open('./README.md') as readme:
    long_description = readme.read()

extras_require = {
    'tester': [
        "pytest>=6.2.5,<7",
        "typing_extensions"
        # "py-geth>=3.8.0,<4",
    ],
    'linter': [
        "black>=22.1.0,<23.0",
        # "flake8==3.8.3",
        # "isort>=4.2.15,<4.3.5",
        # "mypy==0.910",
        # "types-setuptools>=57.4.4,<58",
        # "types-requests>=2.26.1,<3",
        # "types-protobuf==3.19.13",
    ],
    'docs': [
        # "mock",
        # "sphinx-better-theme>=0.1.4",
        # "click>=5.1",
        # "configparser==3.5.0",
        # "contextlib2>=0.5.4",
        # "py-geth>=3.8.0,<4",
        # "py-solc>=0.4.0",
        # "pytest>=6.2.5,<7",
        # "sphinx>=4.2.0,<5",
        # "jupyter-book",
        # "sphinx_rtd_theme>=0.1.9",
        # "toposort>=1.4",
        # "towncrier==18.5.0",
        # "urllib3",
        "wheel"
    ],
    'dev': [
        "bumpversion",
    ]
}

extras_require['dev'] = (
    extras_require['tester']
    + extras_require['linter']
    + extras_require['docs']
    + extras_require['dev']
)


# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="conflux-web3py-signer",
    version=VERSION,
    author="Conflux-Dev",
    author_email="wenda.zhang@confluxnetwork.org",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    package_data={"conflux_web3_bridge": ["py.typed"]},
    url='https://github.com/conflux-fans/conflux-web3py-signer',
    install_requires=[
        "cfx-account>=0.1.0b9",
        "web3>=6.0.0b1",
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    extras_require=extras_require,
    keywords=['python', 'conflux', 'blockchain'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
