from setuptools import setup, find_packages

description = (
    "A minimalistic python documentation tool."
)

setup(
    name="mindoc",
    version="0.1.3",
    description=description,
    author="Min Chul Kim",
    author_email="minchulkim87@gmail.com",
    url="https://minchulkim87.github.io/mindoc/",
    py_modules=['mindoc'],
    entry_points={
        'console_scripts': [
            'mindoc = mindoc:main'
        ]
    },
    install_requires=['mistune', 'beautifulsoup4']
)
