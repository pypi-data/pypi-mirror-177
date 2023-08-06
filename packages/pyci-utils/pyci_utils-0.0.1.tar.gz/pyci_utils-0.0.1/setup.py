"""
Module to create the setup of the PyCI tools
"""
from setuptools import setup, find_packages

__version__ = '0.0.1'  # The version number
__desc__ = "Python CI Tools to improve the coding experience and the coding quality at a better way."
with open('README.md', 'r') as f:
    __long_desc__ = f.read()

setup(
    name='pyci_utils',
    version=__version__,
    packages=find_packages(include=['pyci']),
    author='Ricardo Leal',
    email='<rick.leal420@gmail.com>',
    description=__desc__,
    long_description=__long_desc__,
    long_description_content_type='text/markdown',
    install_requires=[
        'click>=8.1', 'attrs>=22.1.0',
        'rich>=2.6', 'pylint>=2.15'
    ],
    entry_points="""
    [console_scripts]
    pyci=pyci
    """
)
