from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='games'),
    path('<int:pk>', views.GameDetailView.as_view(), name='game'),
]


