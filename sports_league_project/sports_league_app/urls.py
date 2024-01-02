from django.urls import path
from .views import upload_csv, game_list, add_game, edit_game, delete_game

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
    path('games/', game_list, name='game_list'),
    path('games/add/', add_game, name='add_game'),
    path('games/<str:team_name>/edit/', edit_game, name='edit_game'),
    path('games/<str:team_name>/delete/', delete_game, name='delete_game'),
]