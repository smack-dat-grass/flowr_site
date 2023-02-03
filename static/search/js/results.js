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
var sw = {
  // (A) INITIALIZE
  etime : null, // HTML time display
  erst : null, // HTML reset button
  ego : null, // HTML start/stop button
  init : function () {
    // (A1) GET HTML ELEMENTS
    sw.etime = document.getElementById("sw-time");
    //sw.erst = document.getElementById("sw-rst");
    //sw//.ego = document.getElementById("sw-go");

    // (A2) ENABLE BUTTON CONTROLS
    //sw.e//rst.addEventListener("click", sw.reset);
    //sw.erst.disabled = false;
    //sw.ego.addEventListener("click", sw.start);
    //sw.ego.disabled = false;
  },

  // (B) TIMER ACTION
  timer : null, // timer object
  now : 0, // current elapsed time
  tick : function () {
    // (B1) CALCULATE HOURS, MINS, SECONDS
    sw.now++;
    var remain = sw.now;
    var hours = Math.floor(remain / 3600);
    remain -= hours * 3600;
    var mins = Math.floor(remain / 60);
    remain -= mins * 60;
    var secs = remain;

    // (B2) UPDATE THE DISPLAY TIMER
    if (hours<10) { hours = "0" + hours; }
    if (mins<10) { mins = "0" + mins; }
    if (secs<10) { secs = "0" + secs; }
    sw.etime.innerHTML = hours + ":" + mins + ":" + secs;
  },

  // (C) START!
  start : function () {
    var search_time_text = document.getElementById("search_time_text");
    search_time_text.innerText = 'Elapsed Search Time';
    sw.timer = setInterval(sw.tick, 1000);
    //sw.ego.value = "Stop";
    //sw.ego.removeEventListener("click", sw.start);
    //sw.ego.addEventListener("click", sw.stop);
  },

  // (D) STOP
  stop  : function () {
  var search_time_text = document.getElementById("search_time_text");
  search_time_text.innerText = 'Time to Complete Search';
    clearInterval(sw.timer);
    sw.timer = null;
    //sw.ego.value = "Start";
    //sw.ego.removeEventListener("click", sw.stop);
    //sw.ego.addEventListener("click", sw.start);
  },

  // (E) RESET
  reset : function () {
    if (sw.timer != null) { sw.stop(); }
    sw.now = -1;
    sw.tick();
  }
};

//<!--window.addEventListener("load", sw.init);-->

try {
                sw.init()
                function loadJSON(path, success, error) {
                sw.start();
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

                // getJSONP('http://soundcloud.com/oembed?url=http%3A//soundcloud.com/forss/flickermood&format=js&callback=?', function (data) {
                //     console.log(data);
                // });
                //console.log(document.getElementById("report_id").value)
                url = '/search/' + document.getElementById("query").value +"/"+document.getElementById("type").value+ '/run_search';
                //console.log(url);
                loadJSON(url,
                    function (data) {
                        /* construct manually */

//                        console.log(data);
                        if(data['status'] !='success'){
                            Swal.fire('Error', data['message'],'error');
                            sw.stop();
                            return;
                        }
                        for(var i = 0; i < data['warnings'].length; i++){
                            Swal.fire("Warning", data['warnings'][i],'warning');
                        }
                        var tabledata = data["message"];
                        var count = 0;
                        for( key in tabledata){
//                            console.log(tabledata[key])
                            var node = document.createElement("div");
                            node.id="chillen"+String(count);
                            var title=document.createElement("h3");
                            var button=document.createElement("button");
                            button.id="chillenbutton"+String(count);
                            button.innerText ="download .csv";
                            button.value +="download .csv";
                            button.classList.add('w3-blue');
                            button.classList.add('w3-round');
                            button.classList.add('w3-hover-black');
//                            button.classList.add('w3-padding');
                            button.classList.add('w3-center');

                            title.innerText=key;
                            title.classList.add('w3-center');
                            document.getElementById("parent").appendChild(title);
                            document.getElementById("parent").appendChild(node);
                            document.getElementById("parent").appendChild(button);
//                            --appendChild(title);
//--<!--                            document.getElementById("parent").appendChild(node);-->
//<!--                            document.getElementById("parent").appendChild('<button id="\'+"chillenbutton"+String(count)+\'">download .csv</button>');-->
                            _columns = []
                            $.each(tabledata[key][0], function( k, v ) {
//                                console.log( "Key: " + k + ", Value: " + v );
                                var key=k
                               _columns.push({title:key,formatter:"html",field:key,headerFilter:"input",sorter:"string",headerFilterPlaceholder:"enter multiple search queries separated by commas, i.e Avi,Corp,Baker",headerFilterFunc:matchAnyFilter})

                            });
                            if (document.getElementById("chillen"+String(count)+"_rowcount") == null){
                                $("#chillenbutton"+String(count)).before('<p id="chillen'+String(count)+'_rowcount">'+tabledata[key].length+' record(s)</p>')
                            }
                            var table = new Tabulator("#chillen"+String(count), {
                            layout: "fitDataStretch",
                            columns : _columns,
                            data: tabledata[key],
//                            autoColumns: true,
                            movableRows: true,
                            pagination: "local",
                            movableColumns: true,
                            paginationSize: 10,
                            paginationSizeSelector: [10, 20, 50, 100],

                        });
                        document.getElementById("chillenbutton"+String(count)).addEventListener("click", function () {
                            table.download("csv", "data.csv");
                        });
                        count = count+1;
                        }
//                        document.getElementById('count').innerHTML = tabledata.length.toString().concat(' entries')

                        document.getElementById('progress_div').style.display = "none";
                        sw.stop();
                    },
                    function (xhr) {
                        console.error(xhr);
                    }
                );

//                console.log(url)
}catch(err){
Swal.fire('Error', err, 'error');
}
