"""
API Client module.
"""
import aiohttp
import asyncio
from functools import wraps
import logging
from pprint import pprint
from typing import Callable, Coroutine

from .log import get_logger
from .models import Student, StudentDetails
from .query import BuruakaQuery


def request(coro: Callable[["BuruakaClient", ...], Coroutine]):
    """Decorator to mark a certain method as http requestor.
    Used to create session before request.

    Args:
        coro (Callable[["BuruakaClient", ...], Coroutine]): actual requestor coroutine function.

    Returns:
        Callable[["BuruakaClient", ...], Coroutine]: wrapped coroutine function.
    """
    @wraps(coro)
    async def wrapper(self: "BuruakaClient", *args, **kwargs):
        if self._session is None:
            await self.setup()
        return await coro(self, *args, **kwargs)
    return wrapper


class BuruakaClient:
    """
    BlueArchive Unofficial API Buruaka's API client.
    """

    def __init__(self):
        self._session: aiohttp.ClientSession | None = None
        self.logger: logging.Logger = get_logger("bluearchive")

    async def setup(self):
        """Setup client."""
        self._session = aiohttp.ClientSession(base_url="https://api.ennead.cc")

    async def get_chara(self, *, query: BuruakaQuery = None, chara: str = None) -> list[StudentDetails]:
        """Wrapper function of character API. Calls corresponding requestor using args.

        Args:
            query (BuruakaQuery, optional): BuruakaQuery object for Query API. Defaults to None.
            chara (str, optional): Student name. Defaults to None.

        Returns:
            list[StudentDetails]: API response.
        """
        if query is not None:
            return await self.query_chara_details(query)
        if chara is not None:
            return [await self.single_chara(chara)]
        return await self.all_chara()

    @request    # i hate typing. damnit.
    async def query_chara(self, query: BuruakaQuery) -> list[str]:
        """Query student(character) using Query API.

        Args:
            query (BuruakaQuery, optional): BuruakaQuery object for Query API.

        Returns:
            list[str]: API response. List of students' name matching with given query.
        """
        async with self._session.get(url="/bluearchive/character" + query.build()) as resp:
            return await resp.json()

    @request
    async def query_chara_details(self, query: BuruakaQuery) -> list[StudentDetails]:
        """Get students' detailed object using Query API.

        Args:
            query (BuruakaQuery): Query API params.

        Returns:
            list[StudentDetails]: API response as list of StudentDetails object.
        """
        chara_list = await self.query_chara(query)
        resp = await asyncio.gather(*map(
            lambda c: self.single_chara(c),
            chara_list
        ))
        self.logger.debug(resp)
        return resp

    @request
    async def single_chara(self, chara: str) -> StudentDetails:
        """Get single student's detailed object using character API.

        Args:
            chara (str): student name.

        Returns:
            StudentDetails: API response as StudentDetails object.
        """
        async with self._session.get(url=f"/buruaka/character/{chara}") as resp:
            json = await resp.json()
            self.logger.debug(json)
            return StudentDetails.from_json(json)

    @request
    async def all_chara(self) -> list[Student]:
        """Get all student's object using character API.
        Will lack some fields as API does not provide them, though it can be retrieved by additional requests.

        Returns:
            list[Student]: API response as list of Student object.
        """
        async with self._session.get(url="/buruaka/character") as resp:
            json = await resp.json()
            self.logger.debug(json)
            return list(map(Student.from_json, json["data"]))

    async def get_raid(self, query):
        """Wrapper function of raid API. WIP.
        Args:
            query (_type_): _description_
        """
        pass

    async def close(self):
        """Close session."""
        await self._session.close()
        self._session = None

    async def __aenter__(self):
        """Supports Async Conetext (`async with ~`) syntax."""
        await self.setup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Supports Async Conetext (`async with ~`) syntax."""
        await self.close()
        if exc_val is not None:
            raise exc_val   # toss exception to outer scope, for now.
