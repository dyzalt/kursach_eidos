import abc
from Kursach.DTOS.PriceDTO import Price

class GenericParser(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def parse_price(self, html:str) -> Price:
        pass







