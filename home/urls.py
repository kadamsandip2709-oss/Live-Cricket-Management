from django.urls import path
from . import views

urlpatterns = [
    # Home & main pages
    path('', views.home, name='home'),
    path('matches/', views.matches, name='matches'),
    path('teams/', views.teams, name='teams'),
    path('players/', views.players, name='players'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Team URLs
    path("add-player/<int:team_id>/", views.add_player, name="add_player"),
    path("edit-team/<int:team_id>/", views.edit_team, name="edit_team"),
    path("delete-team/<int:team_id>/", views.delete_team, name="delete_team"),

    # Player URLs
    path("edit-player/<int:player_id>/", views.edit_player, name="edit_player"),
    path("delete-player/<int:player_id>/", views.delete_player, name="delete_player"),

    # Match URLs
    path("update-score/<int:match_id>/", views.update_score, name="update_score"),
]
