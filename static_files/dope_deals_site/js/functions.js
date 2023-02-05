function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function loadJSONGet(path, success, error) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                if (success)
                    success(JSON.parse(xhr.responseText));
            } else {
                if (error)
                    error(xhr);
            }
        }
    };
    xhr.open("GET", path, true);
    xhr.send();

}

function loadJSONPost(path, success, error) {
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.ajax({
            type: 'POST',
            url: path,
            data:{
            },headers: {
           'X-CSRFToken': csrfToken
         },
         success: function (d) {
            console.log(d);
            s(JSON.parse(d));
         },
         error: function (e){
            err(e)
         }

                        });
}


//function loadJSONPostData(path, data, success, error) {
//    var xhr = new XMLHttpRequest();
//    xhr.onreadystatechange = function () {
//        if (xhr.readyState === XMLHttpRequest.DONE) {
//            if (xhr.status === 200) {
//                if (success)
//                    success(JSON.parse(xhr.responseText));
//            } else {
//                if (error)
//                    error(xhr);
//            }
//        }
//    };
//
//    xhr.open("POST", path, true);
//    xhr.setRequestHeader("Content-Type", "application/json");
//    xhr.send(JSON.stringify({"selectedFnssos": data}));
//}

function loadJSONPostData(path, data, s, err) {
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    $.ajax({
            type: 'POST',
            url: path,
            data:{
                "content":data
            },headers: {
           'X-CSRFToken': csrfToken
         },
         success: function (d) {
         console.log(d);
            s(JSON.parse(d));
         },
         error: function (e){
            err(e)
         }

                        });
//    var xhr = new XMLHttpRequest();
//    xhr.onreadystatechange = function () {
//        if (xhr.readyState === XMLHttpRequest.DONE) {
//            if (xhr.status === 200) {
//                if (success)
//                    success(JSON.parse(xhr.responseText));
//            } else {
//                if (error)
//                    error(xhr);
//            }
//        }
//    };
//
//    xhr.open("GET", path, true);
//    xhr.setRequestHeader("Content-Type", "application/json");
//    xhr.send(JSON.stringify({"data": data}));
}