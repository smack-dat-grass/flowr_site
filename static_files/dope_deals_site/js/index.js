$(window).on('load', function () {

//    $("body").addClass("loading");
var url = '/get_dope_deals_site_health/'
//    var toolId= document.getElementById("tool_id").value;
//    $("#dope_deals_site_health_message").hide()
    build_tabulator_table(url,"dope_deals_site_health_table")

     //insert all your ajax callback code here.
//     //Which will run only after page is fully loaded in background.
//     if ($("#dope_deals_site_health_table tr").length === 0){
//        console.log("no health violators")
////        $("#dope_deals_site_health_message").text("No health violators")
////        $("#dope_deals_site_health_table").hide()
////        $("#download_csv_dope_deals_site_health_table").hide()
////        $("#dope_deals_site_health_message").show()
//
//    }else{
////    $("#dope_deals_site_health_message").show()
//    }




});