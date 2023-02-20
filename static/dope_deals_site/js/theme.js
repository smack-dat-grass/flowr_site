$('document').ready(function(){
   changeTheme(getTheme());
//   $('tr').addClass('w3-white w3-text-black ');
//    $('td').addClass('w3-white w3-text-black ');
//    $('th').addClass('w3-black w3-text-white ');
    $('#django_site_logo').attr('src','https://www.clipartmax.com/png/middle/362-3625575_marijuana-leaf-icon-clipart-cannabis-clip-art-marijuana-leaf-vector.png')
});

function changeTheme(theme){
//    var  logo = $('#django_site_logo').attr('src');
    $("#table_theme_div").empty();
    console.log('changing to theme to: '+theme)
    if(theme=='darkstar'){
        $('body').removeClass();
        $('nav').removeClass();
                $('button').removeClass('w3-red');
        $('select').removeClass('w3-red');
        $('button').addClass('w3-green');
        $('select').addClass('w3-green');
        $('th').removeClass('w3-black');
        $('td').removeClass('w3-text-black');
        $('tr').removeClass('w3-text-black');
        $('th').removeClass('w3-red');
        $('th').removeClass('w3-green');
        $('body').addClass('w3-black w3-text-white w3-center');
        $('nav').addClass('w3-sidebar w3-bar-block w3-small w3-hide-small w3-center');
        $('nav').addClass('w3-nav w3-text-white ');
        $('tr').addClass('w3-dark-grey w3-text-white ');
        $('td').addClass('w3-dark-grey w3-text-white ');
        $('th').addClass('w3-black w3-text-white ');
        $('#theme').removeClass('w3-light-grey w3-red w3-green');
        $('#theme').addClass('w3-green');
        $(':input[type=button]').removeClass('w3-red w3-green')
        $(':input[type=button]').addClass('w3-green')
        $('#alerts').children('div').removeClass('w3-black w3-white')
        $('#alerts').children('div').addClass('w3-black')
        $('#notifications').children('div').removeClass('w3-black w3-white')
        $('#notifications').children('div').addClass('w3-black')
        $('#health_check_alerts').children('div').removeClass('w3-black w3-white')
        $('#health_check_alerts').children('div').addClass('w3-black')
        $('#table_theme_div').append('<link href="/static/flowr_site/css/tabulator_midnight.min.css" rel="stylesheet">');
    }else if (theme=='idm'){
        $('body').removeClass();
        $('body').addClass('w3-light-gray w3-text-black w3-center');
        $('button').removeClass('w3-red');
        $('select').removeClass('w3-red');
        $('button').addClass('w3-green');
        $('select').addClass('w3-green');
        $('nav').removeClass();
        $('th').removeClass('w3-black');
        $('th').removeClass('w3-red');
        $('td').removeClass('w3-dark-grey');
        $('tr').removeClass('w3-dark-grey');
        $('th').removeClass('w3-green');
        $('nav').addClass('w3-sidebar w3-bar-block w3-small w3-hide-small w3-center');
        $('nav').addClass('w3-white w3-text-black');
        $('tr').addClass('w3-white w3-text-black ');
        $('td').addClass('w3-white w3-text-black ');
        $('th').addClass('w3-black w3-text-white ');
        $('#theme').removeClass('w3-light-grey w3-red w3-green');
        $('#theme').addClass('w3-green');
        $(':input[type=button]').removeClass('w3-red w3-green')
        $(':input[type=button]').addClass('w3-green')
        $('#alerts').children('div').removeClass('w3-black w3-white')
        $('#alerts').children('div').addClass('w3-white')
        $('#notifications').children('div').removeClass('w3-black w3-white')
        $('#notifications').children('div').addClass('w3-white')

        $('#health_check_alerts').children('div').removeClass('w3-black w3-white')
        $('#health_check_alerts').children('div').addClass('w3-white')
        $('#table_theme_div').append('<link href="/static/flowr_site/css/tabulator_simple.min.css" rel="stylesheet">');

}else if (theme=='green'){
        $('body').removeClass();
        $('body').addClass('w3-light-grey w3-text-black w3-center');
        $('button').removeClass('w3-red');
        $('select').removeClass('w3-red');
        $('button').addClass('w3-green');
        $('select').addClass('w3-green');
        $('th').removeClass('w3-black');
        $('th').removeClass('w3-red');
        $('th').removeClass('w3-green');
        $('nav').removeClass();
        $('td').removeClass('w3-dark-grey');
        $('tr').removeClass('w3-dark-grey');
        $('nav').addClass('w3-sidebar w3-bar-block w3-small w3-hide-small w3-center');
        $('nav').addClass('w3-green w3-text-white');
        $('tr').addClass('w3-white w3-text-black ');
        $('td').addClass('w3-white w3-text-black ');
        $('th').addClass('w3-green w3-text-white ');
        $('#theme').removeClass('w3-light-grey w3-red w3-green');
        $('#theme').addClass('w3-light-grey');
        $(':input[type=button]').removeClass('w3-red w3-green')
        $(':input[type=button]').addClass('w3-green')
        $('#alerts').children('div').removeClass('w3-black w3-white')
        $('#alerts').children('div').addClass('w3-white')
        $('#notifications').children('div').removeClass('w3-black w3-white')
        $('#notifications').children('div').addClass('w3-white')
        $('#health_check_alerts').children('div').removeClass('w3-black w3-white')
        $('#health_check_alerts').children('div').addClass('w3-white')
        $('#table_theme_div').append('<link href="/static/flowr_site/css/tabulator_modern.min.css" rel="stylesheet">');
}else if (theme=='red'){
        $('body').removeClass();
        $('body').addClass('w3-light-grey w3-text-black w3-center');

        $('nav').removeClass();
        $('nav').addClass('w3-sidebar w3-bar-block w3-small w3-hide-small w3-center');
        $('nav').addClass('w3-red w3-text-white');
        $('button').removeClass('w3-green');
        $('select').removeClass('w3-green');
        $('th').removeClass('w3-black');
        $('th').removeClass('w3-red');
        $('th').removeClass('w3-green');
        $('button').addClass('w3-red');
        $('select').addClass('w3-red');
        $('td').removeClass('w3-dark-grey');
        $('tr').removeClass('w3-dark-grey');
        $('tr').addClass('w3-white w3-text-black ');
        $('td').addClass('w3-white w3-text-black ');
        $('th').addClass('w3-red w3-text-white ');

        $('#theme').removeClass('w3-light-grey w3-red w3-green');
        $('#theme').addClass('w3-light-grey');
        $(':input[type=button]').removeClass('w3-red w3-green')
        $(':input[type=button]').addClass('w3-red')
        $('#alerts').children('div').removeClass('w3-black w3-white')
        $('#alerts').children('div').addClass('w3-white')
        $('#notifications').children('div').removeClass('w3-black w3-white')
        $('#notifications').children('div').addClass('w3-white')
        $('#health_check_alerts').children('div').removeClass('w3-black w3-white')
        $('#health_check_alerts').children('div').addClass('w3-white')
        $('#table_theme_div').append('<link href="/static/flowr_site/css/tabulator_simple.min.css" rel="stylesheet">');


}    setCookie('theme', theme, 365);
    $('#theme').val(theme);


}

function getTheme(){
if (getCookie('theme') != null){
    return getCookie('theme');
}else{
    return 'darkstar'
}
}