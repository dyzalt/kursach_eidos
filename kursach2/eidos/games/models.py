from django.db import models

class Games(models.Model):
    pass



class ZakaGames(models.Model):
    game_name = models.CharField(primary_key=True, max_length=50)
    game_url = models.URLField()
    price_amount = models.FloatField()
    price_currency = models.CharField(max_length=10)

class GogGames(models.Model):
    game_name = models.CharField(primary_key=True, max_length=50)
    game_url = models.URLField()
    price_amount = models.FloatField()
    price_currency = models.CharField(max_length=10)

class SteamPayGames(models.Model):
    game_name = models.CharField(primary_key=True, max_length=50)
    game_url = models.URLField()
    price_amount = models.FloatField()
    price_currency = models.CharField(max_length=10)

class Articles(models.Model):
    title = models.CharField('Title', max_length=50)
    text = models.TextField('Text')
    date = models.DateTimeField('Date')