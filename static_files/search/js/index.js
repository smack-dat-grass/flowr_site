$('document').ready(function(){
$("#submit").hide();
});
function showDescription(type){
//    var optionInput = document.getElementsByName(type)[0];
//    var description = optionInput.getAttribute('data-description').replace("\"","");

    var url = "/search/"+type+"/get_description";
    loadJSONGet(url, function(data){
        var response = data;
        if(response['status']=='success'){
            var description = response['message'];
            console.log(description);
            $('#description').html(description);
            $("#submit").show();
            $("body").removeClass("loading");
            if(getCookie('theme') != null){
                changeTheme(getCookie('theme'));
            }
        }else{
                Swal.fire("Error", response['message'], 'error');
                $("body").removeClass("loading");
        }


    }, function(xhr){
        console.log(xhr);
        Swal.fire("Error", xhr, 'error');
        $("body").removeClass("loading");
    });


}