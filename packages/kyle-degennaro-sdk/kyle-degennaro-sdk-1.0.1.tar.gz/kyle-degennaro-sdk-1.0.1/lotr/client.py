"""
Client module to handle logic for making an API request.
"""
import re
import os
from typing import Any, Dict, Optional

import requests

from .endpoints import Endpoints
from .errors import InvalidFilterOperator, UnauthorizedError

_API_URL = 'https://the-one-api.dev/v2'
_FILTER_OPERATOR_PATTERN = r'[=!?><]+'
_TIMEOUT = 5


class Client(Endpoints):
    """
    Class client handles logic for making an API request.
    """

    def __init__(self, access_token: Optional[str] = None):
        self._access_token = access_token
        if not self._access_token:
            self._access_token = os.getenv('ACCESS_TOKEN')

    def _make_api_request(  # pylint: disable=R0913,R0914
        self,
        endpoint: str,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Optional[str] = None,
        filter: Optional[str] = None,
        data: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Makes an API request to the specified endpoint.
        """
        url = f'{_API_URL}{endpoint}'

        params = {}
        if limit:
            params['limit'] = limit

        if page:
            params['page'] = page

        if offset:
            params['offset'] = offset

        if sort:
            params['sort'] = sort

        if filter:
            matches = re.findall(_FILTER_OPERATOR_PATTERN, filter)
            if len(matches) == 0:
                raise InvalidFilterOperator(
                    'The supplied operator for the filter is invalid'
                )

            operator = matches[0]
            field, val = filter.split(operator)

            if operator != '=':
                operator = operator.replace('=', '')
                params[f'{field}{operator}'] = val
            else:
                params[field] = val

        req = requests.get if not data else requests.post
        headers = {'Authorization': f'Bearer {self._access_token}'}
        try:
            resp = req(
                url,
                params=params,
                data=data,
                headers=headers,
                timeout=_TIMEOUT,
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as error:
            raise UnauthorizedError(
                'The provided access token is not authorized to access this API'
            ) from error

        return resp.json()
