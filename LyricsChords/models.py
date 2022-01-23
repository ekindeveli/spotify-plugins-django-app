from django.db import models
from .services import SpotiAuth, WebScraper, ChordScraper
# Create your models here.


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Lyric(SingletonModel):

    songName = models.CharField(max_length=100, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    lyrics = models.TextField(blank=True)
    source = models.CharField(max_length=100, blank=True)
    is_playing = models.BooleanField(default=False)
    song_length_ms = models.IntegerField(default=10000)

    @staticmethod
    def lyric_scraper(token):
        ly = Lyric.objects.get_or_create(pk=1)[0]
        if len(token) > 0:
            song, artist, is_playing, song_length_ms = SpotiAuth.currently_playing(token)
            if is_playing:
                ly.song_length_ms = song_length_ms
                if song != ly.songName:
                    ly.lyrics, ly.source, ly.songName = WebScraper.lyrics_method_iterator(song, artist)
                    ly.is_playing = is_playing
                    ly.artist = artist
                else:
                    pass
                ly.save()
                return
            else:
                ly.is_playing = is_playing
                ly.songName = "Spotify is not playing any songs."
                ly.artist = ""
                ly.lyrics = ""
                ly.source = ""
                ly.song_length_ms = song_length_ms
                ly.save()
        else:
            print("Token not accessed")


class Chord(SingletonModel):

    songName = models.CharField(max_length=100, blank=True)
    artist = models.CharField(max_length=100, blank=True)
    chords = models.TextField(blank=True)
    source = models.CharField(max_length=100, blank=True)
    is_playing = models.BooleanField(default=False)
    song_length_ms = models.IntegerField(default=10000)

    @staticmethod
    def chord_scraper(token):
        ch = Chord.objects.get_or_create(pk=1)[0]
        if len(token) > 0:
            song, artist, is_playing, song_length_ms = SpotiAuth.currently_playing(token)
            if is_playing:
                ch.song_length_ms = song_length_ms
                if song != ch.songName:
                    ch.chords, ch.songName, ch.source = ChordScraper.get_chords(song, artist)
                    ch.is_playing = is_playing
                    ch.artist = artist
                ch.save()
                return
            else:
                ch.is_playing = is_playing
                ch.song_length_ms = song_length_ms
                ch.songName = "Spotify is not playing any songs."
                ch.artist = ""
                ch.chords = ""
                ch.source = ""
                ch.save()
        else:
            print("Token not accessed")
