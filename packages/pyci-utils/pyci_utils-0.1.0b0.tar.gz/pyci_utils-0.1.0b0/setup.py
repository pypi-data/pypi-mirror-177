"""
Module to create the setup of the PyCI tools
"""
from pathlib import Path
from setuptools import setup, find_packages
from pyci import __version__

__desc__ = "Python CI Tools to improve the coding experience and the coding quality at a better way."
__long_desc__ = (Path(__file__).parent / "README.md").read_text()

setup(
    name='pyci_utils',
    version=__version__,
    packages=find_packages(exclude=['server', 'webpage']),
    author='Ricardo Leal',
    author_email='rick.leal420@gmail.com',
    description=__desc__,
    long_description=__long_desc__,
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'click>=8.1', 'attrs>=22.1.0',
        'rich>=2.6', 'pylint>=2.15'
    ],
    include_package_data=True,
    entry_points="""
    [console_scripts]
    pyci=pyci
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development'
    ]
)
