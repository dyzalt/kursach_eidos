from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:pk>', views.NewsDetailWiew.as_view(), name='news-detail'),
    path('create/', views.create, name='create')
]
