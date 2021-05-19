class UnsucsessfulCurrencySetException(Exception):
    def __init__(self, status_code:int, currency_url:str):
        self.__status_code:int = status_code
        self.__currency_url:str = currency_url

    def get_status_code(self)->int:
        return self.__status_code

    def get_currency_url(self)->str:
        return self.__currency_url

    def set_status_code(self, code:int):
        self.__status_code = code

    def set_currency_url(self, url:str):
        self.__currency_url = url
