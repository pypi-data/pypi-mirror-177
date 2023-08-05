# pylint: disable=W0212
"""
Decorators to protect API routes.
"""
from .errors import TokenRequiredError


def token_required(func):
    """
    Enforces that an access token is required in order to make
    a request to the specified endpoint. Endpoints the require
    a token can be found at: https://the-one-api.dev/documentation
    under the heading: Which routes are available?
    """

    def wrap(self, *args, **kwargs):
        if self._access_token is None:
            raise TokenRequiredError(
                'An access token is required to access this endpoint.'
            )
        return func(self, *args, **kwargs)

    return wrap
