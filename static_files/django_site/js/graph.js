function buildLineGraph(url, canvas, xaxislabel, yaxislabel){
//console.log(document.getElementById("health_check_id").value)
//        url = '/alerts/health_checks/' + document.getElementById("health_check_id").value + '/get_historical_graph/'+document.getElementById("days").value+'/'
        loadJSONGet(url,
            function (d) {
                var response =d ;
                console.log(response);
                if(response['response']!='success'){
                    return;
                }
                var data = response['message'];
                console.log(data);


                var config = {
            type: 'line',
            data: {
                labels: data['labels'],
                datasets: data['datasets']
            }

            };

        console.log(config);
        $("#"+canvas+"_loading").hide();
//        console.log("Supposed to have hidden canvas again")
        // var ctx = .getContext("2d");
        var myGraph = Chart.Line(document.getElementById(canvas), {data:data, options: {
    responsive: true,
    title: {
      display: false,
      text: ''
    },
    tooltips: {
      mode: 'label',
    },
    hover: {
      mode: 'nearest',
      intersect: true
    },
    scales: {
      xAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString:  xaxislabel
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: yaxislabel
        }
      }]
    }
  }});
        // window.myLine = new Chart(ctx, config);
        // console.log('done');
            },
            function (xhr) {
                console.error(xhr);
            }
        );

        console.log(url)
//        console.log("Supposed to have hidden canvas")

}