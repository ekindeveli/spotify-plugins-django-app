from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login-redirect/', views.login_redirect, name="login-redirect"),
    path('plugin-start/', views.plugin_start, name="plugin-start"),
    path('get-token/', views.get_token, name="get-token"),
    path('lyrics-plugin/', views.lyrics_plugin, name="lyrics-plugin"),
    path('get-lyrics/', views.get_lyrics, name="get-lyrics"),
    path('chords-plugin/', views.chords_plugin, name="chords-plugin"),
    path('get-chords/', views.get_chords, name="get-chords"),
]