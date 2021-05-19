class Price:
    def __init__(self, amount:float, currency:str):
        self.__amount = amount
        self.__currency = currency

    def get_amount(self) -> float:
        return self.__amount

    def get_currency(self) -> str:
        return self.__currency

    def set_currency(self, currency:str):
        self.__currency = currency

    def __str__(self):
        return f"Amount: {self.__amount}, Currency: {self.__currency}"