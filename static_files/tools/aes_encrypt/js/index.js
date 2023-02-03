$('document').ready(function(){
//$("#decrypt_button").hide();
//$("#encrypt_button").hide();
});

//function selectApplication(){
//    $("#download_entitlements_button").show();
//    $("#download_role_master_button").show();
//}
//function downloadEntitlements(){
//    $("body").addClass("loading");
//    var toolId= document.getElementById("tool_id").value;
//    var applicationId = $("#selected_application").val();
//    window.location.replace('/tools/'+toolId+"/entitlement_extraction/download_entitlements/"+applicationId+"/");
//    $("body").removeClass("loading");
//}
//
//function downloadRoleMaster(){
//    $("body").addClass("loading");
//    var toolId= document.getElementById("tool_id").value;
//    var applicationId = $("#selected_application").val();
//    window.location.replace('/tools/'+toolId+"/entitlement_extraction/download_role_master/"+applicationId+"/");
//    $("body").removeClass("loading");
//}
//
function encrypt(){
    $("body").addClass("loading");
    var toolId= document.getElementById("tool_id").value;
    var key = $("#encryption_key").val();
    var value = $("#encryption_value").val().replace('/', '%2F');
    var url = '/tools/'+toolId+"/aes_encrypt/encrypt/"+key+"/"+value+"/";
    loadJSONGet(url, function(data){
        var response = data;
        console.log(response);
        if(response['response']=='success'){
            Swal.fire("Success", "Encrypted Value is\n\n"+response['message'], 'success');
        }else{
                Swal.fire("Error", response['message'], 'error');
                $("body").removeClass("loading");
        }

    }, function(xhr){
        console.log(xhr);
        Swal.fire("Error", xhr, 'error');
        $("body").removeClass("loading");
    });

    $("body").removeClass("loading");

}

function decrypt(){
    $("body").addClass("loading");
    var toolId= document.getElementById("tool_id").value;
    var key = $("#encryption_key").val();
    var value = $("#encryption_value").val().replace('/', '%2F');
    var url = '/tools/'+toolId+"/aes_encrypt/decrypt/"+key+"/"+value+"/";
    loadJSONGet(url, function(data){
        var response = data;
        console.log(response);
        if(response['response']=='success'){
            Swal.fire("Success", "De-crypted Value is\n\n"+response['message'], 'success');
        }else{
                Swal.fire("Error", response['message'], 'error');
                $("body").removeClass("loading");
        }

    }, function(xhr){
        console.log(xhr);
        Swal.fire("Error", xhr, 'error');
        $("body").removeClass("loading");
    });

    $("body").removeClass("loading");

    $("body").removeClass("loading");

}