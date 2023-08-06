"""
cibere.dev python wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper cibere.dev
"""

__description__ = "A basic wrapper cibere.dev"
__version__ = "0.3.0"

from .authorization import Authorization, FileUploaderAuthorization
from .client import Client
from .stream_client import StreamClient
