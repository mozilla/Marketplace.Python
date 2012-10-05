from setuptools import setup

setup(
    name='Marketplace',
    version='0.1a',
    packages=['marketplace',],
    license='Mozilla Public License (MPL 2.0)',
    long_description=open('README.rst').read(),
    install_requires=['httplib2', 'oauth2', 'requests'])
