var lyricSelect = document.getElementById("lyric-selector");
var chordSelect = document.getElementById("chord-selector");
lyricSelect.onclick = function() {
             sessionStorage.setItem('appSelect', 'lyrics');
             window.location.href = 'https://pluginsforspotify.herokuapp.com/plugin-start/'
        }
chordSelect.onclick = function() {
             sessionStorage.setItem('appSelect', 'chords');
             window.location.href = 'https://pluginsforspotify.herokuapp.com/plugin-start/'
        }