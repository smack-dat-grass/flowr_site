function closeConnection(connectionId){

    var url = "/config/connections/"+connectionId+"/close_connection";
loadJSONGet(url,
            function (data) {
                console.log(data);
                if(data['status'] == 'success'){
//                    location.reload();
                    Swal.fire("Info", data['message'], 'success').then(() => {
                    location.reload();
                    });


                }else{
                    Swal.fire("Error", data['message'], 'error');

                }
            },
            function (xhr) {
                console.error(xhr);


            }
        );
}
function testConnection(connectionId){
var url = "/config/connections/"+connectionId+"/test_connection";

      loadJSONGet(url,
            function (data) {
                console.log(data);
                if(data['status'] == 'success'){
                    Swal.fire("Info", data['message'], 'success').then(() => {
                    location.reload();
                    });

//                    location.reload();

                }else{
                    Swal.fire("Error", data['message'], 'error');

                }
            },
            function (xhr) {
                console.error(xhr);


            }
        );

        }
function openConnection(connectionId){
var url = "/config/connections/"+connectionId+"/open_connection";

      loadJSONGet(url,
            function (data) {
                console.log(data);
                if(data['status'] == 'success'){
//                    location.reload();
                    Swal.fire("Info", data['message'], 'success').then(() => {
                    location.reload();
                    });

//                    Swal.fire({
//                      title: 'Success',
//                      html: `<p>${data['message']}</p>`,
//                      confirmButtonText: 'OK',
//                      focusConfirm: false,
//                      preConfirm: () => {
//
//                    }).then(() => {
//
//                        location.reload()
//                    });

                }else{
                    Swal.fire("Error", data['message'], 'error');

                }
            },
            function (xhr) {
                console.error(xhr);


            }
        );
        }