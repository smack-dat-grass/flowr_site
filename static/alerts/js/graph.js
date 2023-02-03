function loadJSON(path, success, error) {
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
$('document').ready(function(){
        // getJSONP('http://soundcloud.com/oembed?url=http%3A//soundcloud.com/forss/flickermood&format=js&callback=?', function (data) {
        //     console.log(data);
        // });
        console.log(document.getElementById("health_check_id").value)
        url = '/alerts/health_checks/' + document.getElementById("health_check_id").value + '/get_historical_graph/'+document.getElementById("days").value+'/'
        loadJSON(url,
            function (d) {
                var response =d ;
                console.log(response);
                if(response['status']!='success'){
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
        // var ctx = .getContext("2d");
        var myGraph = Chart.Line(document.getElementById("myChart"), {data:data, options: {
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
          labelString:  document.getElementById("xaxislabel").value
        }
      }],
      yAxes: [{
        display: true,
        scaleLabel: {
          display: true,
          labelString: document.getElementById("yaxislabel").value
        }
      }]
    }
  }})
        // window.myLine = new Chart(ctx, config);
        // console.log('done');
            },
            function (xhr) {
                console.error(xhr);
            }
        );
        console.log(url)
});