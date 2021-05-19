from django.db import models
from games.app.DTOS.StoreDTOS import Store, ZakaStore, GogStore, SteamPayStore
from games.app.DTOS.PriceDTO import Price
from games.app.DTOS.GameDTO import Game as GameDTO
from typing  import Dict, Union


class Zaka(models.Model):
    game_name = models.CharField(max_length=50, primary_key=True)
    game_url = models.URLField()
    price_amount = models.FloatField(null=True)
    price_currency = models.CharField(max_length=10, null=True)
    objects = models.Manager()

class Gog(models.Model):
    game_name = models.CharField(max_length=50, primary_key=True)
    game_url = models.URLField()
    price_amount = models.FloatField(null=True)
    price_currency = models.CharField(max_length=10, null=True)
    objects = models.Manager()

class SteamPay(models.Model):
    game_name = models.CharField(max_length=50, primary_key=True)
    game_url = models.URLField()
    price_amount = models.FloatField(null=True)
    price_currency = models.CharField(max_length=10,  null=True)
    objects = models.Manager()

class Articles(models.Model):
    title = models.CharField('Title', max_length=50)
    text = models.TextField('Text')
    date = models.DateTimeField('Date')
    objects = models.Manager()

class Game(models.Model):
    game_name = models.CharField(max_length=50, primary_key=True)
    Zaka = models.OneToOneField(Zaka, on_delete=models.CASCADE, null=True, db_index=False)
    Gog = models.OneToOneField(Gog, on_delete=models.CASCADE, null=True, db_index=False)
    SteamPay = models.OneToOneField(SteamPay, on_delete=models.CASCADE, null=True, db_index=False)
    objects = models.Manager()

    def get_stores_urls(self) -> Dict[Store, str]:
        stores_urls:Dict[Store:str] = {}
        try:
            gog_url = self.Gog.game_url
        except AttributeError:
            pass
        else:
            stores_urls[GogStore] = gog_url
        try:
            zaka_url = self.Zaka.game_url
        except AttributeError:
            pass
        else:
            stores_urls[ZakaStore] = zaka_url
        try:
            steam_url = self.SteamPay.game_url
        except AttributeError:
            pass
        else:
            stores_urls[SteamPayStore] = steam_url
        return stores_urls


    def get_stores_prices(self) -> Dict[Store, Price]:
        stores_urls:Dict[Store:str] = {}
        try:
            gog_amount:float = self.Gog.price_amount
            gog_currency:str = self.Gog.price_currency
            gog_price:Price = Price(gog_amount, gog_currency)
        except AttributeError:
            pass
        else:
            stores_urls[GogStore] = gog_price

        try:
            zaka_amount:float = self.Zaka.price_amount
            zaka_currency:str = self.Zaka.price_currency
            zaka_price:Price = Price(zaka_amount, zaka_currency)
        except AttributeError:
            pass
        else:
            stores_urls[ZakaStore] = zaka_price

        try:
            steam_pay_amount:float = self.SteamPay.price_amount
            steam_pay_currency:str = self.SteamPay.price_currency
            steam_pay_price:Price = Price(steam_pay_amount, steam_pay_currency)
        except AttributeError:
            pass
        else:
            stores_urls[SteamPayStore] = steam_pay_price

        return stores_urls

    def update_gog_field(self, new_field:Gog):
        self.Gog = new_field

    def update_zaka_field(self, new_field:Zaka):
        self.Zaka = new_field

    def update_steam_pay_field(self, new_field:SteamPay):
        self.SteamPay = new_field

    def update_game_name_field(self, new_field:str):
        self.game_name = new_field


    def __updt_price(self, model, amount, currency):
        model.price_amount = amount
        model.price_currency = currency
        model.save()

    def update_prices(self, stores_prices:Dict[Store, Price]):
        switch = {
            GogStore:self.Gog,
            ZakaStore:self.Zaka,
            SteamPayStore:self.SteamPay}

        for key in stores_prices.keys():
            price:Price = stores_prices[key]
            amount, currency = price.get_amount(), price.get_currency()
            model = switch[key]
            try:
                self.__updt_price(model, amount, currency)
            except AttributeError:
                pass

    def __updt_urls(self, model, url:str):
        model.game_url = url
        model.save()

    def update_urls(self, stores_urls:Dict[Store, str]):
        switch = {
            GogStore:self.Gog,
            ZakaStore:self.Zaka,
            SteamPayStore:self.SteamPay
        }

        for key in stores_urls.keys():
            url:str = stores_urls[key]
            model = switch[key]
            try:
                self.__updt_urls(model, url)
            except AttributeError:
                pass

    def get_game_dto(self) -> GameDTO:
        urls = self.get_stores_urls()
        prices = self.get_stores_prices()
        name = self.game_name
        return GameDTO(name, urls, prices)

