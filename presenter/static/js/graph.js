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

function createGraph(domIdent, dataIdent, title, xText, yText, seriesInitData) {
    $(domIdent).highcharts('StockChart', $.extend({}, baseSettings, {
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

        series: [
            {
                name: dataIdent,
                data: seriesInitData
            }
        ]
    }));
}
