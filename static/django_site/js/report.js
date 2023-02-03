//custom filter function
function matchAnyFilter(headerValue,cellValue, rowData, filterParams){
    //headerValue - the value of the header filter element
    //cellValue- the value of the column in this row
    //rowData - the data for the row being filtered
    //filterParams - params object passed to the headerFilterFuncParams property

    var matched = false;
    var values = headerValue.split(","); //break header into list of options
//    console.log(values)
    values.forEach(function(val){
//    console.log(cellValue);
        if(cellValue.toString().toLowerCase().indexOf(val.toString().toLowerCase()) !== -1){
            matched = true;
//            console.log("match found")
        }
    });

    return matched;
}

function build_tabulator_table(url,tableId){
        if (document.getElementById(tableId+"_rowcount") == null){
            $("#download_csv_"+tableId).before('<p id="'+tableId+'_rowcount">0 record(s)</p>')
        }
//        console.log(document.getElementById("report_id").value)
//                url = '/reports/' + document.getElementById("report_id").value + '/getjsreport'
        loadJSONGet(url,
            function (data) {
                console.log(data);
                if(data['response']=='error'){
                    Swal.fire('Error', data['message'], 'error');
                    return
                }
                var tabledata = data['message'];
                console.log(tabledata);
//                keys = []
                _columns = []
                for (var key in tabledata[0]){
                    _columns.push({title:key,formatter:"html",field:key,headerFilter:"input",sorter:"string",headerFilterPlaceholder:"enter multiple search queries separated by commas, i.e Avi,Corp,Baker",headerFilterFunc:matchAnyFilter})
//                    keys.push(key);
//                    console.log(key)

                }

                var table = new Tabulator("#"+tableId, {
                    layout: "fitDataStretch",
                    data: tabledata,
                    columns: _columns,
                    movableRows: true,
                    pagination: "local",
                    movableColumns: true,
                    paginationSize: 10,
                    paginationSizeSelector: [10, 20, 50, 100],
                    dataFiltered: function(filters, rows) {

                          var el = document.getElementById(tableId+"_rowcount");
                          el.innerHTML = rows.length+ " record(s)";
                    },
                    dataLoaded: function(data) {

                          var el = document.getElementById(tableId+"_rowcount");
                          el.innerHTML = data.length+ " record(s)";
                },
                });
                document.getElementById("download_csv_"+tableId).addEventListener("click", function () {
                    table.download("csv", "data.csv");
                });



                $("#"+tableId+"_loading").hide();
//                console.log(typeof data['message'])
//                console.log("Total rows: "+data['message'].length)
//                    if(typeof data['message'] != object){
                if(data['message'].length <=1 ){

                    $("#download_csv_"+tableId).hide();
                }

            },
            function (xhr) {
                console.error(xhr);
            }
        );
        console.log(url)
}

function build_pie_chart(url,tableId){
//        //console.log(document.getElementById("report_id").value)
//                url = '/reports/' + document.getElementById("report_id").value + '/getjsreport'
        loadJSONGet(url,
            function (data) {
                //console.log(data);
                if(data['response']=='error'){
                    Swal.fire('Error', data['message'], 'error');
                }
        // var ctx = .getContext("2d");
        $('#'+tableId).remove();
        $('#'+tableId+"_div").append('<canvas style="width: 400px;height: 200px;" width="400" height="200" class="w3-center" id="'+tableId+'"></canvas>');
        var canvas = document.getElementById(tableId);
        var ctx = canvas.getContext('2d');

//        var canvas = document.getElementById(tableId);
//        var ctx = canvas.getContext('2d');
//        ctx.setTransform(1, 0, 0, 1, 0, 0);
//        ctx.clearRect(0, 0, canvas.width, canvas.height);
        new Chart(ctx, {
                    type: 'pie',
                    data: {
                      labels: data['message']['labels'],
                      datasets: data['message']['datasets']
                    },
                    options: {
                      responsive: true,
                      plugins:{
                         legend: {
                            position: 'bottom',
                          },
                      title: {
                        display: false,
                        text: ''
                      }}
                    }})
//                    document.getElementById("download_csv_"+tableId).addEventListener("click", function () {

//                });
                $("#"+tableId+"_loading").hide();
            },
            function (xhr) {
                Swal.fire("Error", xhr, 'error');
            }
        );
        //console.log(url)
}

function build_bar_chart(url,tableId){
//        //console.log(document.getElementById("report_id").value)
//                url = '/reports/' + document.getElementById("report_id").value + '/getjsreport'
        loadJSONGet(url,
            function (data) {
                //console.log(data);
                if(data['response']=='error'){
                    Swal.fire('Error', data['message'], 'error');
                }
        $('#'+tableId).remove();
        $('#'+tableId+"_div").append('<canvas style="width: 400px;height: 200px;" width="400" height="200" class="w3-center" id="'+tableId+'"></canvas>');
        var canvas = document.getElementById(tableId);
        var ctx = canvas.getContext('2d');

//        ctx.setTransform(1, 0, 0, 1, 0, 0);
//        ctx.clearRect(0, 0, canvas.width, canvas.height);
        new Chart(ctx, {
//                    responsive:true,
                    type: 'bar',
                    data: {
                      labels: data['message']['labels'],
                      datasets: data['message']['datasets']
                    },
                    options: {
                    scaleShowValues: true,
                    scales: {
                              xAxes: [{
                                  beginAtZero: true,
                                  ticks: {
                                     autoSkip: false
                                  }
                              }],
                              yAxes: [{
                                  beginAtZero: true,
                                  ticks: {
                                     autoSkip: false
                                  }
                              }]
                            },
                      title: {
                        display: false,
                        text: ''
                      }
                    }})
//                    document.getElementById("download_csv_"+tableId).addEventListener("click", function () {

//                });
                $("#"+tableId+"_loading").hide();
            },
            function (xhr) {
                Swal.fire("Error", xhr, 'error');
            }
        );
        //console.log(url)
}