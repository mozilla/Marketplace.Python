from setuptools import setup

setup(
    name='Marketplace',
    version='0.1.2a',
    packages=['marketplace', ],
    license='Mozilla Public License (MPL 2.0)',
    author='Piotr Zalewa',
    author_email='zalun@mozilla.com',
    url='https://github.com/mozilla/Marketplace.Python',
    long_description="""
Marketplace Client Library

Mozilla is building a Marketplace to bring personalized discovery,
worldwide distribution, and easy payments to the largest platform
for app development: the Web.

This library helps to create Python based sites or apps to communicate
with Marketplace.

You may find the source code and collaborate your time and experience at
https://github.com/mozilla/Marketplace.Python
""",
    install_requires=['httplib2', 'oauth2', 'requests'])
