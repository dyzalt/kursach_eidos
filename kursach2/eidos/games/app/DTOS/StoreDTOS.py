from games.app.Parser.HtmlParsers.GenericParser import GenericParser
from games.app.Parser.HtmlParsers.STEAMPAYparser import SteamPayParser
from games.app.Parser.HtmlParsers.GOGparser import GOGparser
from games.app.Parser.HtmlParsers.ZAKAparser import ZakaParser
class _StoreDTO:
    def __init__(self, name:str, parser:GenericParser):
        self.__name = name
        self.__parcer = parser

    def get_name(self) -> str:
        return self.__name

    def get_parcer(self) -> GenericParser:
        return self.__parcer

    def __str__(self):
        return self.__name

class _ZakaStore(_StoreDTO):
    def __init__(self):
        super().__init__("zaka-zaka", ZakaParser)

class _GogStore(_StoreDTO):
    def __init__(self):
        super().__init__("gog", GOGparser)

class _SteamPayStore(_StoreDTO):
    def __init__(self):
        super().__init__("steampay", SteamPayParser)

Store, ZakaStore, GogStore, SteamPayStore = _StoreDTO, _ZakaStore(), _GogStore(), _SteamPayStore()
