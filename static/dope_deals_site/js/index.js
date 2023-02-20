$(window).on('load', function () {

//    $("body").addClass("loading");
var url = '/get_flowr_site_health/'
//    var toolId= document.getElementById("tool_id").value;
//    $("#flowr_site_health_message").hide()
    build_tabulator_table(url,"flowr_site_health_table")

     //insert all your ajax callback code here.
//     //Which will run only after page is fully loaded in background.
//     if ($("#flowr_site_health_table tr").length === 0){
//        console.log("no health violators")
////        $("#flowr_site_health_message").text("No health violators")
////        $("#flowr_site_health_table").hide()
////        $("#download_csv_flowr_site_health_table").hide()
////        $("#flowr_site_health_message").show()
//
//    }else{
////    $("#flowr_site_health_message").show()
//    }




});