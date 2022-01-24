window.addEventListener("load", function(){
    var token = localStorage.getItem('token');
    json = JSON.stringify(token);

    function recurse(){
      var waitDuration = print_chords(json)
      if(isNaN(parseInt(waitDuration))){
          waitDuration = 10000;
        } else if (waitDuration > 90000){
          waitDuration = 80000;
        };
      window.setTimeout(recurse, waitDuration);
      }
    window.setTimeout(recurse, 150);
});

function print_chords(json) {
    var waitLength = null;
    $.ajax({
    async: false,
    type: "POST",
    url: "/get-chords/",
    data: {"data": json},
    dataType: "json",
    success: function (response) {
            // on successfull creating object
            var song = document.getElementById("songC").innerHTML;
            if (song != response['songName']) {
                document.getElementById("songC").innerHTML = response['songName'];
                document.getElementById("artistC").innerHTML = response['artist'];
                document.getElementById("chordText").innerHTML = response['chords'];
                // make all text same color
                var els = document.getElementsByClassName("_3rlxz");
                for (var i=0; i < els.length; i++){
                    els.item(i).style.color = "black"
                }
                // get rid of unnecessary text
                var X = document.getElementsByClassName("VvVqJ");
                for (var i=0; i<X.length; i++){
                    X.item(i).innerHTML = ""
                }
                document.getElementById("sourceC").innerHTML = response['source'];
            };
            waitLength = response['song_length_ms'];
        },
    error: function(jqXHR, exception) {
            if (jqXHR.status == 500) {
                console.log("failure with status 500, please restart application...")
//                myUrl = "https://pluginsforspotify.herokuapp.com/"
//                window.location = myUrl
            };
        },
    });
    return waitLength + 2000
};