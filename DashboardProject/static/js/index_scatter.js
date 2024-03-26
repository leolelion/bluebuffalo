var ctx2 = document.getElementById('scatter_AQI_pop')
var aqi = [35, 60, 55, 50, 40, 40, 60]
var pop = [7000, 55000, 2500, 53000, 6000, 30000, 120000]
var city = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
var myChart = new Chart(ctx2, {
    type: 'scatter',
    data: {
        labels: pop,
        datasets: [
            {
                label: 'Locations',
                data: aqi,
                backgroundColor: 'blue',
                pointBorderColor: 'black',
                radius: 5
            }
        ]
    },
    options: {
        scales: {
            xAxes: {
                title: {
                    display: true,
                    text: 'Population at Location'
                }
            },
            yAxes: {
                title: {
                    display: true,
                    text: 'Air Quality Index'
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function (chart) {
                        // var i = chart[0].dataIndex;
                        var i = 3;
                        return city[i];
                    }
                }
            }
        }
    }
}
)