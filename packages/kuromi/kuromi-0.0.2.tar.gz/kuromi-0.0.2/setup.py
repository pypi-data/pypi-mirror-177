import os
from codecs import open
from setuptools import find_packages, setup
from kuromi import VERSION

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r', 'utf-8') as handle:
    readme = handle.read()


setup(
    name='kuromi',
    version=VERSION,
    description='system tool',
    long_description=readme,
    author='ponponon',
    url='http://github.com/ponponon/kuromi',
    packages=find_packages(exclude=['testing']),
    install_requires=[
        "click",
        "psutil",
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'kuromi=kuromi.cli.main:main',
        ]
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
