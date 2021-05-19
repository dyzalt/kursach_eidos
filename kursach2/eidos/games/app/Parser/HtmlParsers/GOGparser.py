from games.app.Parser.HtmlParsers.GenericParser import GenericParser
from games.app.DTOS.PriceDTO import Price
from bs4 import BeautifulSoup
from games.app.CustomExceptions.WrongHtmlException import WrongHtmlException


class _GoGParser(GenericParser):
    def __init__(self):
        super().__init__()

    def __getSoup(self, html:str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")

    def __getPrice(self, soup:BeautifulSoup) -> float:
        raw_price = soup.find("div", class_="product-actions-price").find_all("span")[2].get_text()
        price = str(raw_price).strip()
        return float(price)

    def __check_html(self, soup:BeautifulSoup) -> bool:
        if soup.find("div", class_="product-actions-price") == None:
            return False
        return True

    def parse_price(self, html:str) -> Price:
        soup = self.__getSoup(html)
        if not self.__check_html(soup):
            raise WrongHtmlException
        else:
            amount: float = self.__getPrice(soup)
            currency: str = ''
            return Price(amount, currency)


GOGparser = _GoGParser()

