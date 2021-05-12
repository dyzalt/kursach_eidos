from aiohttp import ClientSession
from asyncio import Task, create_task, gather, run, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from Kursach.CustomExceptions.WrongStatusException import WrongStatusException
from typing import List, Tuple


class _Scraper:
    def __init__(self):
        pass

    def get_session(self) -> ClientSession:
        return ClientSession()

    async def get_html(self, url:str, session:ClientSession) -> str:
        async with session.get(url) as r:
            if r.status != 200:
                raise WrongStatusException(r.status, url)
            else:
                html:str = await r.text()
        return html

    async def scrape_site(self, urls:List[str], session:ClientSession) -> Tuple[List[str], List[Exception]]:
        exceptions:List[Exception] = []
        htmls:List[str] = []
        tasks:List[Task] = [create_task(self.get_html(url, session)) for url in urls]
        results = await gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, Exception):
                exceptions.append(r)
            else:
                htmls.append(r)
        return (htmls, exceptions)

Scraper = _Scraper()


