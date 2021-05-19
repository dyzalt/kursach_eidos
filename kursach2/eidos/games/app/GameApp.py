from games.models import Game
from games.app.Parser.Parser import Parser
from games.app.DTOS.GameDTO import Game as GameDTO
from games.app.DTOS.StoreDTOS import Store, ZakaStore, GogStore, SteamPayStore
from games.app.DTOS.PriceDTO import Price
from typing import List, Dict, Union
import asyncio

class _ParseAndStoreApp():
    def __init__(self):
        pass

    def update_one_game_prices(self, game_name:str, currecny_gog="https://www.gog.com/user/changeCurrency/USD"):
        game:Game = Game.objects.get(game_name = game_name)
        game_dto:GameDTO = game.get_game_dto()
        res:Dict[Store, Union[Price, Exception]] = self.parse_game_prices(game_dto, currecny_gog)
        excep:Dict[Store, Exception] = {}
        sucsess:Dict[Store, Price] = {}
        for key in res.keys():
            val = res[key]
            if isinstance(val, Exception):
                excep[key] = val
            elif isinstance(val, Price):
                sucsess[key] = val
        print(excep)
        print(sucsess)
        game.update_prices(sucsess)

    def update_many_games_prices(self, game_names:List[str], currecny_gog="https://www.gog.com/user/changeCurrency/USD"):
        for game_name in game_names:
            self.update_one_game_prices(game_name, currecny_gog)

    def test(self, game_name, currecny_gog="https://www.gog.com/user/changeCurrency/USD"):
        game:Game = Game.objects.get(game_name = game_name)
        game_dto:GameDTO = game.get_game_dto()
        res:Dict[Store, Union[Price, Exception]] = self.parse_game_prices(game_dto, currecny_gog)
        excep:Dict[Store, Exception] = {}
        sucsess:Dict[Store, Price] = {}
        for key in res.keys():
            val = res[key]
            if isinstance(val, Exception):
                excep[key] = val
            elif isinstance(val, Price):
                sucsess[key] = val
        print(excep)
        print(sucsess)
        return sucsess

    def parse_game_prices(self, game_dto:GameDTO, currency_gog)->Dict[Store, Union[Price, Exception]]:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        return asyncio.run(Parser.parse_single_game(game_dto, currency_gog))

ParseAndStoreApp = _ParseAndStoreApp()
