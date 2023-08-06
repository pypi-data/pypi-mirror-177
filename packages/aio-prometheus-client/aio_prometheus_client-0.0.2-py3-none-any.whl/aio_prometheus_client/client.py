from time import time as get_current_timestamp
from urllib.parse import urljoin

import httpx

from . import errors
from .model import parse_data, InstantVector, Scalar

DEFAULT_USER_AGENT = 'Python Aio Prometheus Client'
TIMEOUT = 10 * 60


class PrometheusClient:
    def __init__(self, base_url, user_agent=DEFAULT_USER_AGENT):
        self.base_url = base_url
        self.user_agent = user_agent

    async def _request(self, path, params=None):
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(
                    urljoin(self.base_url, path),
                    params=params,
                    headers={'User-Agent': self.user_agent},
                    timeout=TIMEOUT,
                )
            except Exception as e:
                raise errors.PrometheusConnectionError('request fail') from e

            if r.status_code == 400:
                data = r.json()
                raise errors.PrometheusMeticError(r.status_code, data)

            r.raise_for_status()
            data = r.json()

        if data['status'] != 'success':
            raise ValueError('invalid data: %s' % data)

        return data

    async def query(self, metric, time=0):
        if not time:
            time = get_current_timestamp()

        data = await self._request(
            path='api/v1/query',
            params={
                'query': metric,
                'time': str(time)
            }
        )

        return parse_data(data['data'])

    async def query_value(self, metric):
        data = await self.query(metric)
        if isinstance(data, InstantVector):
            series_count = len(data.series)
            if series_count != 1:
                raise ValueError('series count incorrect: %d' % series_count)

            return data.series[0].value.value
        elif isinstance(data, Scalar):
            return data.value
        else:
            raise TypeError('unknown data type: %s' % type(data))
