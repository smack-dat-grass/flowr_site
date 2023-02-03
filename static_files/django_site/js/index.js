$(window).on('load', function () {

//    $("body").addClass("loading");
var url = '/get_django_site_health/'
//    var toolId= document.getElementById("tool_id").value;
//    $("#django_site_health_message").hide()
    build_tabulator_table(url,"django_site_health_table")

     //insert all your ajax callback code here.
//     //Which will run only after page is fully loaded in background.
//     if ($("#django_site_health_table tr").length === 0){
//        console.log("no health violators")
////        $("#django_site_health_message").text("No health violators")
////        $("#django_site_health_table").hide()
////        $("#download_csv_django_site_health_table").hide()
////        $("#django_site_health_message").show()
//
//    }else{
////    $("#django_site_health_message").show()
//    }




});