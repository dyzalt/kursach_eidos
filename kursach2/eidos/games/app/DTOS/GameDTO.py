from typing import Dict, Optional
from games.app.DTOS.StoreDTOS import Store, GogStore, ZakaStore, SteamPayStore
from games.app.DTOS.PriceDTO import Price

class Game:
    def __init__(self, name:str, urls: Dict[Store, str], prices: Dict[Store, Price]=None):
        self.__name = name
        self.__urls: Dict[Store, str] = urls
        self.__prices: Dict[Store, Price] = prices

    def __str__(self):
        urls = ""
        for d in self.__urls.keys():
            urls += f"{d} : {self.__urls[d]}\n"
        prices = ""
        for p in self.__prices.keys():
            prices += f"{p} : {self.__prices[p]}\n"
        str = f"name : {self.__name}\n" \
              f"URLS:\n" \
              f"{urls}" \
              f"PRICES:\n" \
              f"{prices}"
        return str


    def getName(self) -> str:
        return self.__name

    def getUrls(self) -> Dict[Store, str]:
        return self.__urls

    def __get_url(self, store:Store) -> Optional[str]:
        return self.__urls.get(store, None)

    def get_url(self, store:Store) -> Optional[Price]:
        return self.__get_url(store)

    def __get_price(self, store:Store) -> Optional[Price]:
        return self.__prices.get(store, None)

    def get_price(self, store:Store)  -> Optional[Price] :
        return self.__get_price(store)

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

    def get_gog_price(self) -> Optional[Price]:
        return self.__get_price(GogStore)

    def get_zaka_price(self) -> Optional[Price]:
        return self.__get_price(ZakaStore)

    def get_steam_pay_price(self) -> Optional[Price]:
        return self.__get_price(SteamPayStore)

def test():
    game:Game = Game("cyberpunk", {GogStore:"abcd"}, {GogStore:Price(1, "a")})
    print(game.get_gog_url())

if __name__ == '__main__':
    test()