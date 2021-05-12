class WrongStatusException(Exception):
    def __init__(self, status_code:int, url:str):
        self.__status_code = status_code
        self.__url = url

    def get_status_code(self)->int:
        return self.__status_code

    def get_url(self)->str:
        return self.__url