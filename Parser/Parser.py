from Kursach.Parser.HtmlParsers.GenericParser import GenericParser
from Kursach.Parser.HtmlScraper import Scraper
from aiohttp import ClientSession
from Kursach.CustomExceptions.UnsucsessfulCurrencySetException import UnsucsessfulCurrencySetException
from Kursach.CustomExceptions.WrongHtmlException import WrongHtmlException
from Kursach.Parser.HtmlParsers.GOGparser import GOGparser
from Kursach.Parser.HtmlParsers.ZAKAparser import ZakaParser
from Kursach.Parser.HtmlParsers.STEAMPAYparser import SteamPayParser
from Kursach.DTOS.GameDTO import Game
from Kursach.DTOS.StoreDTOS import Store, ZakaStore, GogStore, SteamPayStore
from Kursach.DTOS.PriceDTO import Price
from typing import Dict, Union, List, Coroutine
import asyncio


def _wrapper(store: Store):
    def outer(func: Coroutine):
        async def inner(*args, **kwargs) -> Dict[Store, Union[Price, Exception]]:
            try:
                res: Price = await func(*args, **kwargs)
            except Exception as e:
                return {store: e}
            else:
                return {store: res}
        return inner
    return outer

def _gog_wrapper(store: Store):
    def outer(func: Coroutine):
        async def inner(*args, **kwargs) -> Dict[Store, Union[Price, Exception]]:
            try:
                res = await func(*args, **kwargs)
            except Exception as e:
                return {store: e}
            else:
                return res
        return inner
    return outer

class _Parser():
    def __init__(self):
        pass

    async def __parse_single(self, url:str, session:ClientSession, parser:GenericParser) -> Price:
        html:str = await Scraper.get_html(url, session)
        try:
            price:Price = parser.parse_price(html)
        except WrongHtmlException:
            raise WrongHtmlException(url)
        return price

    async def __set_session_for_gog(self, currency_url:str) -> ClientSession:
        session: ClientSession = Scraper.get_session()
        async with session.get(currency_url) as r:
            st_code = r.status
        if st_code != 200:
            await session.close()
            raise UnsucsessfulCurrencySetException(st_code, currency_url)
        else:
            return session

    @_wrapper(GogStore)
    async def __parse_single_gog(self, url:str, session:ClientSession, currency:str) -> Price:
        price:Price = await self.__parse_single(url, session, GOGparser)
        price.set_currency(currency)
        return price

    @_wrapper(ZakaStore)
    async def __parse_single_zaka(self, url:str, session:ClientSession) -> Price:
        price:Price = await self.__parse_single(url, session, ZakaParser)
        return price

    @_wrapper(SteamPayStore)
    async def __parse_single_steam_pay(self, url:str, session:ClientSession) -> Price:
        price:Price = await self.__parse_single(url, session, SteamPayParser)
        return price

    async def parse_single_zaka(self, url:str) -> Price:
        session:ClientSession = Scraper.get_session()
        async with session:
            return await self.__parse_single_zaka(url, session)

    async def parse_single_steam_pay(self, url:str) -> Price:
        session:ClientSession = Scraper.get_session()
        async with session:
            return await self.__parse_single_steam_pay(url, session)

    @_gog_wrapper(GogStore)
    async def parse_single_gog(self, url:str, currency_url:str) -> Price:
        session:ClientSession = await self.__set_session_for_gog(currency_url)
        currency: str = currency_url.split("/")[-1]
        async with session:
            return await self.__parse_single_gog(url, session, currency)

    async def __parse_single_game(self, game:Game, gog_currency_url:str, gog_session:ClientSession, zaka_session:ClientSession, steam_session:ClientSession) -> Dict[Store, Union[Price, Exception]]:
        gog_url, zaka_url, steam_url = game.get_gog_url(), game.get_zaka_url(), game.get_steam_pay_url()
        tasks: List[asyncio.Task] = self.__create_tasks(gog_url, zaka_url, steam_url, gog_session, gog_currency_url, zaka_session, steam_session)
        res:Dict[Store, Union[Price, Exception]] = await asyncio.gather(*tasks)
        return res

    def __create_tasks(self, gog_u:str, zaka_u:str, steam_pay_u:str, gog_s:ClientSession, gog_cur:str ,zaka_s:ClientSession, steam_pay_s:ClientSession) -> List[asyncio.Task]:
        tasks:List[asyncio.Task] = []
        if gog_u != None:
            tasks.append(asyncio.create_task(self.__parse_single_gog(gog_u, gog_s, gog_cur)))
        if zaka_u != None:
            tasks.append(asyncio.create_task(self.__parse_single_zaka(zaka_u, zaka_s)))
        if steam_pay_u != None:
            tasks.append(asyncio.create_task(self.__parse_single_steam_pay(steam_pay_u, steam_pay_s)))
        return tasks


    async def parse_single_game(self, game:Game, gog_currency_url:str) -> Dict[Store, Union[Price, Exception]]:
        gog_url, zaka_url, steam_url = game.get_gog_url(), game.get_zaka_url(), game.get_steam_pay_url()
        res:Dict[Store, Union[Price, Exception]] = {}
        if gog_url != None:
            gog_res = await self.parse_single_gog(gog_url, gog_currency_url)
            res.update(gog_res)
        if zaka_url != None:
            zaka_res = await self.parse_single_zaka(zaka_url)
            res.update(zaka_res)
        if steam_url != None:
            steam_res = await self.parse_single_steam_pay(steam_url)
            res.update(steam_res)
        return res

    async def parse_many_games(self, games:List[Game], gog_currency_url:str) -> List[Dict[Store, Union[Price, Exception]]]:
        gog_s = self.__set_session_for_gog(gog_currency_url)
        zaka_s = Scraper.get_session()
        steam_s = Scraper.get_session()
        tasks:List[asyncio.Task] = [asyncio.create_task(self.__parse_single_game(game, gog_currency_url, gog_s, zaka_s, steam_s)) for game in games]
        res:List[Dict[Store, Union[Price, Exception]]] = await asyncio.gather(*tasks)
        return res

Parser = _Parser()



