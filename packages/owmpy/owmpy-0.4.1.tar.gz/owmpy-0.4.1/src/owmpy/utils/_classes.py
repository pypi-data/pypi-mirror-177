from typing import NamedTuple
import aiohttp as _aiohttp


Number = int | float


class ShortLong(NamedTuple):
    """Represents shorthand and longhand of a unit."""

    short: str
    """Shorthand form, eg '°C'"""
    long: str
    """Longhandform, eg 'Celsius'"""


class _AutomaticClient:
    client: _aiohttp.ClientSession
    appid: str

    def __init__(self, appid: str, client: _aiohttp.ClientSession | None = None) -> None:
        self.appid = appid
        self.client = client or _aiohttp.ClientSession()

    async def close(self):
        await self.client.close()

    async def __aenter__(self, *args):
        return self

    async def __aexit__(self, *args):
        await self.close()
        return self
