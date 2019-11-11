function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

document.getElementById('btn-email').disabled = true;
document.getElementById('btn-refresh').disabled = true;
document.getElementById('btn-export').disabled = true;
document.getElementById('btn-export-xls').disabled = true;
document.getElementById('btn-email').setAttribute("disabled", "");
document.getElementById('btn-refresh').setAttribute("disabled", "");
document.getElementById('btn-export').setAttribute("disabled", "");
document.getElementById('btn-export-xls').setAttribute("disabled", "");

var canvases = [document.getElementById('pm1'),
    document.getElementById('pm25'),
    document.getElementById('pm10'),
    document.getElementById('temperature'),
    document.getElementById('pressure'),
    document.getElementById('humidity'),
    document.getElementById('wind_speed'),
    document.getElementById('clouds')];

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
        $('#loader').show();
    }
});

$.ajax({
    type: 'post',
    url: url,
    data: JSON.stringify(JSON.parse(jsonData)),
    dataType: 'json',
    contentType: 'application/json',
    complete: function () {
        $('#loader').hide();
    },
    success: function (response) {
        response = JSON.parse(response);
        drawData(response.data);
        fillInfo(response.info);
        fillStats(response.data, response.stats);
        fillDataTable(response.data);
        enableButtons();
    },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
        alert("There was an error while collecting data. Please try again later");
    }
});

function drawData(data) {
    /* Hide unused canvas */
    canvases.map(c => c.style.display = hasFactorData(data, c.id) ? "block" : "none")

    /* PM1 */
    var pm1 = new Chart(document.getElementById('pm1'), {
        type: 'line',
        data: {
            labels: Object.keys(data.pm1),
            datasets: [{
                data: Object.values(data.pm1),
                fill: false,
                borderColor: 'rgba(0,0,0,0.6)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'PM1'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'PM1 (\xB5g/m\xB3)'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    })

    /* PM25 */
    var pm25 = new Chart(document.getElementById('pm25'), {
        type: 'line',
        data: {
            labels: Object.keys(data.pm25),
            datasets: [{
                data: Object.values(data.pm25),
                fill: false,
                borderColor: 'rgba(0,0,0,0.6)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'PM2.5'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            annotation: {
                annotations: [{
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: data.pm25_norm,
                    borderColor: 'rgb(255, 0, 0)',
                    borderWidth: 2,
                    label: {
                        enabled: false,
                        content: 'Norm',
                        position: 'right'
                    }
                }]
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'PM2.5 (\xB5g/m\xB3)',
                        ticks: {
                            beginAtZero: true
                        }
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    })

    /* PM10 */
    var pm10 = new Chart(document.getElementById('pm10'), {
        type: 'line',
        data: {
            labels: Object.keys(data.pm10),
            datasets: [{
                data: Object.values(data.pm10),
                fill: false,
                borderColor: 'rgba(0,0,0,0.6)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'PM10'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            annotation: {
                annotations: [{
                    type: 'line',
                    mode: 'horizontal',
                    scaleID: 'y-axis-0',
                    value: data.pm10_norm,
                    borderColor: 'rgb(255, 0, 0)',
                    borderWidth: 2,
                    label: {
                        enabled: false,
                        content: 'Norm',
                        position: 'right'
                    }
                }]
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'PM10 (\xB5g/m\xB3)'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    })

    /* TEMPERATURE */
    var temperature = new Chart(document.getElementById('temperature'), {
        type: 'line',
        data: {
            labels: Object.keys(data.temperature),
            datasets: [{
                data: Object.values(data.temperature),
                fill: false,
                borderColor: 'rgba(0,0,0,0.6)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'Temperature'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Temperature (\xB0C)'
                    }
                }]
            }
        }
    })

    /* PRESSURE */
    var pressure = new Chart(document.getElementById('pressure'), {
        type: 'line',
        data: {
            labels: Object.keys(data.pressure),
            datasets: [{
                data: Object.values(data.pressure),
                fill: false,
                borderColor: 'rgba(0,0,0,0.6)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'Pressure'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Pressure (hPa)'
                    }
                }]
            }
        }
    })

    /* HUMIDITY */
    var humidity = new Chart(document.getElementById('humidity'), {
        type: 'bar',
        data: {
            labels: Object.keys(data.humidity),
            datasets: [{
                data: Object.values(data.humidity),
                fill: false,
                backgroundColor: 'rgb(128,128,128)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'Humidity'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    },
                    categoryPercentage: 1.0,
                    barPercentage: 1.0
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: '% of humidity'
                    },
                    ticks: {
                        beginAtZero: true,
                        max: 100
                    }
                }]
            }
        }
    })

    /* WIND SPEED */
    var wind_speed = new Chart(document.getElementById('wind_speed'), {
        type: 'line',
        data: {
            labels: Object.keys(data.wind_speed),
            datasets: [{
                data: Object.values(data.wind_speed),
                fill: false,
                borderColor: 'rgba(0,0,0,0.6)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'Wind speed'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Speed (m/s)'
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    })

    /* WIND DIRECTION */
    var wind_degree = new Chart(document.getElementById('wind_degree'), {
        type: 'line',
        data: {},
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Wind direction'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: false
                }],
                yAxes: [{
                    display: false
                }]
            }
        }
    })

    /* CLOUDS */
    var clouds = new Chart(document.getElementById('clouds'), {
        type: 'bar',
        data: {
            labels: Object.keys(data.clouds),
            datasets: [{
                data: Object.values(data.clouds),
                fill: false,
                backgroundColor: 'rgb(128,128,128)'
            }]
        },
        options: {
            legend: {
                display: false
            },
            responsive: true,
            title: {
                display: true,
                text: 'Clouds'
            },
            tooltips: {
                mode: 'index',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    time: {
                        unit: 'day'
                    },
                    categoryPercentage: 1.0,
                    barPercentage: 1.0
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: '% of cloudiness'
                    },
                    ticks: {
                        beginAtZero: true,
                        max: 100
                    }
                }]
            }
        }
    })
}

function fillInfo(info) {
    document.getElementById('info').innerText = info.join('\n');
}

function fillStats(data, stats) {
    var table = document.getElementById('stats');
    for (var factor in stats) {
        if (hasFactorData(data, factor.toLowerCase().split(" ").join("_").split(".").join(""))) {
            var row = table.insertRow();
            row.insertCell().appendChild(document.createTextNode(factor));
            row.insertCell().appendChild(document.createTextNode(stats[factor].mean));
            row.insertCell().appendChild(document.createTextNode(stats[factor].median));
            row.insertCell().appendChild(document.createTextNode(stats[factor].stdev));
        }
    }
}

function hasFactorData(data, factor) {
    var dates = Object.keys(data[factor]);
    for (var i = 0; i < dates.length; i++) {
        if (data[factor][dates[i]] != null) {
            return true;
        }
    }

    return false;
}

function fillDataTable(data) {
    var table = document.getElementById('datatable');
    var factors = ['pm1', 'pm25', 'pm10', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_degree', 'clouds'];
    var factorsData = {};
    for (var i = 0; i < factors.length; i++) {
        if (hasFactorData(data, factors[i])) {
            factorsData[factors[i]] = data[factors[i]];
        }
    }
    if (Object.keys(factorsData).length > 0) {
        var headerRow = table.insertRow();
        headerRow.insertCell().appendChild(document.createTextNode("datetime"));
        presentFactors = Object.keys(factorsData);
        for (var i = 0; i < presentFactors.length; i++) {
            headerRow.insertCell().appendChild(document.createTextNode(presentFactors[i]));
        }

        var dates = Object.keys(factorsData[presentFactors[0]]);
        for (var i = 0; i < dates.length; i++) {
            var row = table.insertRow();
            row.insertCell().appendChild(document.createTextNode(dates[i]));
            for (var j = 0; j < presentFactors.length; j++) {
                row.insertCell().appendChild(document.createTextNode(factorsData[presentFactors[j]][dates[i]]));
            }
        }
    }
}

function enableButtons() {
    document.getElementById('btn-email').disabled = false;
    document.getElementById('btn-refresh').disabled = false;
    document.getElementById('btn-export').disabled = false;
    document.getElementById('btn-export-xls').disabled = false;
    document.getElementById('btn-email').removeAttribute("disabled");
    document.getElementById('btn-refresh').removeAttribute("disabled");
    document.getElementById('btn-export').removeAttribute("disabled");
    document.getElementById('btn-export-xls').removeAttribute("disabled");
    addExportButtonHandler();
    addExportXlsButtonHandler();
}

/* Helper functions */
function getFullChartWidth() {
    return Math.max.apply(null, canvases.map(c => c.width));
}

function getFullChartHeight() {
    return canvases.filter(c => c.style.display != 'none').map(c => c.height).reduce((a, b) => a + b, 0);
}

function addExportButtonHandler() {
    var exportBtn = document.getElementById('btn-export');
    exportBtn.addEventListener('click', function (e) {
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        canvas.width = getFullChartWidth();
        canvas.height = getFullChartHeight();
        ctx.fillStyle = "white";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        var tempY = 0;
        for (var i = 0; i < canvases.length; i++) {
            if (canvases[i].style.display != 'none') {
                ctx.drawImage(canvases[i], 0, tempY);
                tempY = tempY + canvases[i].height;
            }
        }
        var dataUrl = canvas.toDataURL('image/png');
        exportBtn.href = dataUrl;
    });
}

function addExportXlsButtonHandler() {
    var exportXlsBtn = document.getElementById('btn-export-xls');
    exportXlsBtn.addEventListener('click', function (e) {
        $('#datatable').table2excel({
            name: filename,
            filename: filename + '.xls'
        });
    });
}