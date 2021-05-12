from Kursach.Parser.HtmlParsers.GenericParser import GenericParser
from Kursach.DTOS.PriceDTO import Price
from bs4 import BeautifulSoup
from Kursach.CustomExceptions.WrongHtmlException import WrongHtmlException

class _ZakaParser(GenericParser):
    def __init__(self):
        super().__init__()

    def __getSoup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")

    def __getPrice(self, soup: BeautifulSoup) -> float:
        raw_price = soup.find("div", attrs={"class":"buy-zone"}).find("meta", attrs={"itemprop":"price"}).get("content")
        price = str(raw_price).strip()
        return float(price)

    def __getCurrency(self, soup: BeautifulSoup) -> str:
        currency = soup.find("div", attrs={"class":"buy-zone"}).find("meta", attrs={"itemprop":"priceCurrency"}).get("content")
        return str(currency).strip()

    def __check_html(self, soup:BeautifulSoup) -> bool:
        if soup.find("div", attrs={"class":"buy-zone"}) == None:
            return False
        return True

    def parse_price(self, html:str) -> Price:
        soup = self.__getSoup(html)
        if not self.__check_html(soup):
            raise WrongHtmlException
        else:
            amount: float = self.__getPrice(soup)
            currency: str = self.__getCurrency(soup)
            return Price(amount, currency)



ZakaParser = _ZakaParser()
