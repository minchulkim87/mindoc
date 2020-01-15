from setuptools import setup, find_packages

description = (
    "A minimalistic python documentation module."
)

setup(
    name="mindoc",
    version="0.0.1",
    description=description,
    author="Min Chul Kim",
    author_email="minchulkim87@gmail.com",
    url="https://minchulkim87.github.io/mindoc/",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mindoc = mindoc:main'
        ]
    },
    install_requires=['mistune', 'beautifulsoup4']
)
