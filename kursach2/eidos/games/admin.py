from django.contrib import admin
from .models import  Game, Zaka, Gog, SteamPay, GameArticle
from .app.GameApp import ParseAndStoreApp as PAS
# Register your models here.
admin.site.register(GameArticle)
admin.site.register(Zaka)
admin.site.register(Gog)
admin.site.register(SteamPay)


class GameAdmin(admin.ModelAdmin):
    list_display = ["game_name", "Zaka", "Gog", "SteamPay", "Article"]
    ordering = ["game_name"]
    actions = ["update_prices"]

    def update_prices(self, request, queryset):
        games = list(queryset)
        if len(games)==1:
            game = games[0]
            PAS.update_one_game_prices_by_game_object(game)
        elif len(games) > 1:
            PAS.update_many_games_prices_by_games_objects(games)


admin.site.register(Game, GameAdmin)