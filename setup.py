from pathlib import Path
from setuptools import setup

version = "0.5.0"
description = "A minimalistic python documentation tool."

source_root = Path(".")

with (source_root / "README.md").open(encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mindoc",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Min Chul Kim",
    author_email="minchulkim87@gmail.com",
    url="https://minchulkim87.github.io/mindoc/",
    py_modules=["mindoc"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["mindoc = mindoc:main"]},
    python_requires=">=3.6",
    install_requires=[
        "appdirs==1.4.4",
        "attrs==19.3.0",
        "beautifulsoup4==4.9.1",
        "black==19.10b0; python_version >= '3.6'",
        "cached-property==1.5.1",
        "cerberus==1.3.2",
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "click==7.1.2",
        "colorama==0.4.3",
        "distlib==0.3.0",
        "idna==2.9",
        "mistune==0.8.4",
        "orderedmultidict==1.0.1",
        "packaging==19.2",
        "pathspec==0.8.0",
        "pep517==0.8.2",
        "pip-shims==0.5.2",
        "pipenv-setup==3.0.1",
        "pipfile==0.0.2",
        "plette[validation]==0.2.3",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.1",
        "regex==2020.5.14",
        "requests==2.23.0",
        "requirementslib==1.5.9",
        "six==1.15.0",
        "soupsieve==2.0.1",
        "toml==0.10.1",
        "tomlkit==0.6.0",
        "typed-ast==1.4.1",
        "typing==3.7.4.1",
        "urllib3==1.25.9",
        "vistir==0.5.2",
        "wheel==0.34.2",
    ],
)
