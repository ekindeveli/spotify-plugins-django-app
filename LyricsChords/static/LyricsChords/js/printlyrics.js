window.addEventListener("load", function(){
    var token = localStorage.getItem('token');
    json = JSON.stringify(token);

    function recurse(){
      var waitDuration = print_lyrics(json)
      if(isNaN(parseInt(waitDuration))){
          waitDuration = 10000;
        } else if (waitDuration > 90000){
          waitDuration = 80000;
        };
      window.setTimeout(recurse, waitDuration);
      }
    window.setTimeout(recurse, 150);
});

function print_lyrics(json) {
    var waitLength = null;
    $.ajax({
    async: false,
    type: "POST",
    url: "/get-lyrics/",
    data: {"data": json},
    dataType: "json",
    success: function (response) {
            // on successfull creating object
            var song = document.getElementById("song").innerHTML;
            if (song != response['songName']) {
                document.getElementById("song").innerHTML = response['songName'];
                document.getElementById("artist").innerHTML = response['artist'];
                document.getElementById("lyricText").innerText = response['lyrics'];
                document.getElementById("source").innerHTML = response['source'];
            };
            waitLength = response['song_length_ms'];
        },
    error: function(jqXHR, exception) {
            if (jqXHR.status == 500) {
                console.log("failure with status 500, please restart application...")
//                myUrl = "https://spotifyplugins.herokuapp.com/"
//                window.location = myUrl
            };
        },
    });
    return waitLength + 2000
};

