$(function() {
  console.log('jquery is working!');
    $.getJSON('/data', function(data_got){
        var data = [];
        data_got.forEach(function(d) {
            //var dt = moment(d.DAY, 'YYYY-MM-DD').toDate();

            data.push([Date.parse(d.DAY), parseFloat(d.PRICE)])
        });
        console.log(data);
        $('#container123').highcharts({
            chart: {
                zoomType: 'x'
            },
            title: {
                text: 'Henry Hub gas prices over the year'
            },
            subtitle: {
                text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            },
            xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: {
                    day: '%d %b %Y'    //ex- 01 Jan 2016
                }
            },
            yAxis: {
                title: {
                    text: 'Gas Prices'
                }
            },
            legend: {
                enabled: false
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                },
                series:{
                    turboThreshold:0//larger threshold or set to 0 to disable
                }
            },

            series: [{
                type: 'area',
                name: 'USD to EUR',
                data: data
            }]
        });
    });
});