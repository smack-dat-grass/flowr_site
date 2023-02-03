$('document').ready(function(){
//    $("body").addClass("loading");
    var reportId= document.getElementById("report_id").value;
var url = '/reports/'+reportId+'/getjsreport_history_list'
    build_tabulator_table(url,"report_table")
//    build_tabulator_table("/tools/"+toolId+"/idm_integration_dashboard/load_ge_application_overview_data","ge_app_table")
//    build_tabulator_table("/tools/"+toolId+"/idm_integration_dashboard/load_idm_digital_application_overview_data","idm_app_table")
////    build_tabulator_table("/tools/"+toolId+"/idm_integration_dashboard/load_ge_aggregating_apps_not_in_cmdb_data","idm_apps_aggregating_not_in_cmdb_table")
//    build_tabulator_table("/tools/"+toolId+"/idm_integration_dashboard/load_idm_apps_not_in_cmdb_data","idm_apps_not_in_cmdb_table")
//    build_tabulator_table("/tools/"+toolId+"/idm_integration_dashboard/load_ge_db_overview_data","ge_db_table")
////    build_tabulator_table("/tools/"+toolId+"/idm_integration_dashboard/load_infraidm_dbs_not_in_cmdb_data","infraidm_dbs_not_in_cmdb_table")

//    console.log("woo")


//$("#download_role_master_button").hide();
});