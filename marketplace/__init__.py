"""Marketplace Client Library

https://wiki.mozilla.org/Marketplace

Mozilla is building a Marketplace to bring personalized discovery,
worldwide distribution, and easy payments to the largest platform
for app development: the Web.

This library helps to create Python based sites or apps to communicate
with Marketplace.
"""

__version__ = '0.1'
__all__ = [
        'Client',
]
__author__ = 'Piotr Zalewa <zalun@mozilla.com>'

from .client import Client
