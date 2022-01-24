from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import json
import os
from django.views.decorators.csrf import csrf_exempt
from .models import Lyric, Chord


def home(request):
    return render(request, 'LyricsChords/home.html')


def login_redirect(request):
    return render(request, 'LyricsChords/login-redirect.html')


def plugin_start(request):
    client_id = os.environ.get('DJANGO_LYRIC_CLIENT_ID')
    # client_secret = os.environ.get('DJANGO_LYRIC_CLIENT_SECRET')
    scope2 = "user-read-playback-state"
    url = f'https://accounts.spotify.com/authorize?response_type=token&client_id={client_id}' \
          f'&scope={scope2}&redirect_uri=https://pluginsforspotify.herokuapp.com/login-redirect/'
    return redirect(url)


@csrf_exempt
def get_token(request):
    # request method should be POST.
    if request.method == "POST":
        try:
            request_data = request.POST.get('data', None)
            selection = json.loads(request_data)
            if "chord" in selection:
                jdata = {"url": "chords-plugin"}
            elif "lyric" in selection:
                jdata = {"url": "lyrics-plugin"}
            else:
                jdata = {}
            return JsonResponse(data=jdata, status=200)
        except TypeError:
            messages.error(request, "Unexpected Error! Returning to Home Page and restarting the plugin.")
            return redirect('home')
    else:
        # some error occured
        messages.error(request, "Unexpected Error! Returning to Home Page and restarting the plugin.")
        return redirect('home')


def lyrics_plugin(request):
    return render(request, "LyricsChords/lyrics-plugin.html")


@csrf_exempt
def get_lyrics(request):
    # request method should be POST
    if request.method == "POST":
        request_data = request.POST.get('data', None)
        token = json.loads(request_data)
        if token is not None:
            Lyric.lyric_scraper(token)
            ly = Lyric.objects.get(pk=1)
            lyric_data = {
                'lyrics': ly.lyrics,
                'source': ly.source,
                'songName': ly.songName,
                'is_playing': ly.is_playing,
                'artist': ly.artist,
                'song_length_ms': ly.song_length_ms
            }
            return JsonResponse(data=lyric_data, status=200)
        else:
            lyric_data = {
                'lyrics': "",
                'source': "",
                'songName': "Please log in to Spotify to use this plugin.",
                'is_playing': True,
                'artist': "",
                'song_length_ms': 10000
            }
            return JsonResponse(data=lyric_data, status=200)
    else:
        # some error occured
        messages.error(request, "Unexpected Error! Returning to Home Page and restarting the plugin.")
        return redirect('home')


def chords_plugin(request):
    return render(request, "LyricsChords/chords-plugin.html")


@csrf_exempt
def get_chords(request):
    # request should be ajax and method should be POST
    if request.method == "POST":
        # get the data
        request_data = request.POST.get('data', None)
        token = json.loads(request_data)
        if token is not None:
            Chord.chord_scraper(token)
            ch = Chord.objects.get(pk=1)
            lyric_data = {
                'chords': ch.chords,
                'source': ch.source,
                'songName': ch.songName,
                'is_playing': ch.is_playing,
                'artist': ch.artist,
                'song_length_ms': ch.song_length_ms
            }
            return JsonResponse(data=lyric_data, status=200)
        else:
            lyric_data = {
                'chords': "",
                'source': "",
                'songName': "Please log in to Spotify to use this plugin.",
                'is_playing': True,
                'artist': "",
                'song_length_ms': 10000
            }
            return JsonResponse(data=lyric_data, status=200)
    else:
        # some error occured
        messages.error(request, "Unexpected Error! Returning to Home Page and restarting the plugin.")
        return redirect('home')
