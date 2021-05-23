from games.models import Game
from .Parser.Parser import Parser
from .DTOS.GameDTO import Game as GameDTO
from .DTOS.StoreDTOS import Store, ZakaStore, GogStore, SteamPayStore
from .DTOS.PriceDTO import Price
from typing import List, Dict, Union
import asyncio

class _ParseAndStoreApp():
    def __init__(self):
        pass

    def __update_one(self, game:Game, currency_gog):
        game_dto:GameDTO = game.get_game_dto()
        res: Dict[Store, Union[Price, Exception]] = self.__run_async(Parser.parse_single_game, game_dto, currency_gog)
        self.__save_changes(res, game)

    def __save_changes(self, res:Dict[Store, Union[Price, Exception]], game:Game):
        sucsess, excep = self.__filter(res)
        game.update_prices(sucsess)

    def __update_many(self, games:List[Game], currency_gog):
        game_dtos:List[GameDTO] = [game.get_game_dto() for game in games]
        results = self.__run_async(Parser.parse_many_games, game_dtos, currency_gog)
        for game, res in zip(games, results):
            self.__save_changes(res, game)



    def __filter(self, res:Dict[Store, Union[Price, Exception]]):
        excep: Dict[Store, Exception] = {}
        sucsess: Dict[Store, Price] = {}
        for key in res.keys():
            val = res[key]
            if isinstance(val, Exception):
                excep[key] = val
            elif isinstance(val, Price):
                sucsess[key] = val
        return sucsess, excep

    def __run_async(self, func, *args, **kwargs):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        res = asyncio.run(func(*args,  **kwargs))
        return res

    def update_one_game_prices_by_game_name(self,  game_name:str, currency_gog="https://www.gog.com/user/changeCurrency/USD"):
        game:Game = Game.objects.get(game_name=game_name)
        self.__update_one(game, currency_gog)

    def update_one_game_prices_by_game_object(self, game:Game, currency_gog="https://www.gog.com/user/changeCurrency/USD"):
        self.__update_one(game, currency_gog)

    def update_many_games_prices_by_games_names(self, games_names:List[str], currency_gog="https://www.gog.com/user/changeCurrency/USD"):
        games:List[Game] = [Game.objects.get(game_name=game_name) for game_name  in games_names]
        self.__update_many(games, currency_gog)

    def update_many_games_prices_by_games_objects(self, games:List[Game], currency_gog="https://www.gog.com/user/changeCurrency/USD"):
        self.__update_many(games, currency_gog)

    def update_all_games_prices(self, currency_gog="https://www.gog.com/user/changeCurrency/USD"):
        games:List[Game] = Game.objects.all()
        self.__update_many(games, currency_gog)

ParseAndStoreApp = _ParseAndStoreApp()
