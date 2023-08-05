"""
Exceptions raised by the client.
"""


class UnauthorizedError(Exception):
    """
    Thrown when an API method is invoked with an invalid access token.
    """


class TokenRequiredError(Exception):
    """
    Thrown when an API method is invoked that requires a valid access token.
    """


class InvalidFilterOperator(Exception):
    """
    Thrown when an invalid operator is supplied
    with the filter value for an API request.
    """
