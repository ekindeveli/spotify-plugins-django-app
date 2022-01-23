window.addEventListener("load", function(){
    var token = localStorage.getItem('token');
    if (token != null){
        document.getElementById("ly-plgn").innerHTML = "Lyrics Plugin";
        document.getElementById("ch-plgn").innerHTML = "Chords Plugin";
    }
});

