# spotify-plugins-django-app
  A Plugin for Spotify that retrieves the lyrics/chords of currently playing song. A web application built with django.

  The app requests 'user-read-playback-state' instead of 'user-read-currently-playing' because 
  the program uses the 'progress_ms' and 'duration_ms' fields to calculate how much time left in a song 
  instead of pinging the server every 10 seconds. These fields require the 'user-read-playback-state' permission.