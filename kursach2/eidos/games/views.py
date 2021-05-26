from django.shortcuts import render
from .models import Game
from django.views.generic import DetailView


def index(request):
    games = Game.objects.all()
    return render(request, 'games/games.html', {"games": games})


class GameDetailView(DetailView):
    model = Game
    template_name = 'games/game_view.html'
    context_object_name = 'game'
