from typing import Dict, Union, Optional
from Kursach.DTOS.StoreDTOS import Store, GogStore, ZakaStore, SteamPayStore
from Kursach.DTOS.PriceDTO import Price

class Game:
    def __init__(self, name:str, urls: Dict[Store, str], prices: Dict[Store, Price]):
        self.__name = name
        self.__urls: Dict[Store, str] = urls
        self.__prices: Dict[Store, Price] = prices

    def getName(self) -> str:
        return self.__name

    def getUrls(self) -> Dict[Store, str]:
        return self.__urls

    def __get_url(self, store:Store) -> Optional[str]:
        return self.__urls.get(store, None)

    def get_gog_url(self) -> Optional[str]:
        return self.__get_url(GogStore)

    def get_zaka_url(self) -> Optional[str]:
        return self.__get_url(ZakaStore)

    def get_steam_pay_url(self)-> Optional[str]:
        return self.__get_url(SteamPayStore)

    def set_gog_url(self, url:str):
        self.__urls[GogStore] = url

    def set_zaka_url(self, url:str):
        self.__urls[ZakaStore] = url

    def set_steam_pay_url(self, url:str):
        self.__urls[SteamPayStore] = url

    def getPrices(self) -> Dict[Store, Price]:
        return self.__prices

    def setPrices(self, prices:Dict[Store, Price]):
        self.__prices = prices

def test():
    game:Game = Game("cyberpunk", {GogStore:"abcd"}, {GogStore:Price(1, "a")})
    print(game.get_gog_url())

if __name__ == '__main__':
    test()