/*!
    * Start Bootstrap - SB Admin v6.0.3 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2021 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    (function($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });
})(jQuery);

//
//$('.carousel').carousel({
//    interval: 50000
//  })

//$('.carousel-item').css({"transition":"15s", "transition-timing-function":"linear"})
//$('.carousel-item').css("padding", "0 5px")

$('.carousel').carousel({
    interval: 10000
  })
$('.carousel-item').css({"transition":"5s", "transition-timing-function":"linear"})




$("#filter_form").submit(function(e){
    //alert("Submitted");
    var serializedData = $(this).serialize();


    $.ajax({
        type: 'GET',
        url: "filter_chart",
        data: serializedData,
        success: function (response) {

            
            mylineChart.data.labels = response.response.graph_labels
            mylineChart.data.datasets[0].data = response.response.graph_data
            

            mybarChart.data.labels = response.response.bar_labels;
            mybarChart.data.datasets[0].data = response.response.bar_data;

            $('#line_chart_name').text(response.response.name)
            $('#bar_chart_name').text(response.response.name)

            mylineChart.update();
            mybarChart.update();

            
        },
        error: function (response) {
            // alert the error if any error occured
            alert('error');
        }
    })

    e.preventDefault();
});






$(".stock_cards").click(function(e){
    //alert('ping');
    var dataid = $(this).attr("data-id");
    //alert(names_list[0])
    $('#line_chart_name').text(names_list[dataid])
    $('#bar_chart_name').text(names_list[dataid])
  


    mylineChart.data.labels =  dataset_linechart_labels[dataid]
    mylineChart.data.datasets[0].data =  dataset_linechart_data[dataid]
    //
    //

    mybarChart.data.labels = dataset_barchart_labels[dataid]
    mybarChart.data.datasets[0].data = dataset_barchart_data[dataid]

    mylineChart.update();
    mybarChart.update();
    
    
    e.preventDefault();
});




