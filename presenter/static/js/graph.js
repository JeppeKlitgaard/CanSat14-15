var maxPoints = 250;
var series = []

var baseSettings = {
    rangeSelector: {
        enabled: false
    },

    exporting: {
        enabled: false
    },

    credits: {
        enabled: false
    },

    xAxis: {
        ordinal: false
    }
};

Highcharts.setOptions({
    global: {
        useUTC: false,
    }
});

function createGraph(domIdent, dataIdent, title, xText, yText, seriesInitData, extra_series) {
    extra_series = extra_series || [];
    // extra_series = [
    //     {name: "asd", data: [[1,2], [3,4]]}
    // ]
    ser = [
        {
            name: dataIdent,
            data: seriesInitData
        }
    ];

    for (i = 0; i < extra_series.length; i++) {
        ser.push(extra_series[i])
    };

    $(domIdent).highcharts('StockChart', $.extend(true, {}, baseSettings, {
        chart: {
            events: {
                load: function() {
                series.push(this.series[0]);
                }
            }
        },

        title: {
            text: title
        },

        xAxis: {
            title: {
                text: xText
            },
            labels: {
                enabled: true,
                formatter: function(){return this.value;}
            }
        },

        navigator: {
            xAxis: {
                labels: {
                    enabled: true,
                    formatter: function(){return this.value;}
                }
            },
        },

        yAxis: {
            title: {
                text: yText
            }
        },

        series: ser
    }));
}
