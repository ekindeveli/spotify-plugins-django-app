// Get token from URL
window.addEventListener("load", function(){
    let url = window.location.href;
    const searchBegin = url.indexOf("=");
    const searchEnd = url.indexOf("&");
    let token = url.slice(searchBegin+1, searchEnd);
    localStorage.setItem('token', token);
    var selection = sessionStorage.getItem('appSelect');
    var json = JSON.stringify(selection)
    $.ajax({
        type: "POST",
        url: "/get-token/",
        data: {"data": json},
        dataType: "json",
        success: function (response) {
                    // on successfull creating object
                    console.log("success, redirecting...")
                    myUrl = "https://spotifyplugins.herokuapp.com/"
                    myUrl += response['url']
                    window.location = myUrl
                },
    });
    });

