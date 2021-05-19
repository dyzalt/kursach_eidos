import abc
from games.app.DTOS.PriceDTO import Price

class GenericParser(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def parse_price(self, html:str) -> Price:
        pass







