class WrongHtmlException(Exception):
    def __init__(self, url:str=""):
        self.__url = url

    def get_url(self) -> str:
        return self.__url

    def set_url(self, url:str):
        self.__url = url
