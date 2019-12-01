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
        beforeSend: function(xhr, settings) {
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
        complete: function() {
            $('#loader').hide();
        },
        success: function(response) {
            response = JSON.parse(response);
            drawData(response.data, response['prediction_offset'], response['enable_heavy_computing']);
            fillInfo(response.info);
            if (hasHistoricalData(response.data)) {
                fillStats(response.data.historical, response.stats.historical, 'historical_stats');
            } else {
                hideHistoricalStats();
            }
            if (response['enable_heavy_computing']) {
                fillStats(response.data.fbprophet, response.stats.fbprophet, 'fbprophet_stats');
            } else {
                hideHeavyComputingStats();
            }
            fillStats(response.data.linreg, response.stats.linreg, 'linreg_stats');
            fillStats(response.data.arima, response.stats.arima, 'arima_stats');
            fillDataTable(response.data, response['enable_heavy_computing']);
            enableButtons();
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            alert("There was an error while collecting data. Please try again later");
        }
    });

    function hasFactorData(data, factor) {
        if (Object.keys(data).includes(factor)) {
            var dates = Object.keys(data[factor]);
            for (var i = 0; i < dates.length; i++) {
                if (data[factor][dates[i]] != null) {
                    return true;
                }
            }
        }

        return false;
    }

    function hasHistoricalData(data) {
        var historicalData = data.historical;
        var factors = Object.keys(historicalData);
        for (var i = 0; i < factors.length; i++) {
            if (hasFactorData(historicalData, factors[i])) {
                return true;
            }
        }

        return false;
    }

    function hideHistoricalStats() {
        document.getElementById("historical_stats_header").style.display = "none";
        document.getElementById("historical_stats").style.display= "none";
    }

    function hideHeavyComputingStats() {
        document.getElementById("fbprophet_stats_header").style.display = "none";
        document.getElementById("fbprophet_stats").style.display= "none";
    }

    function mergeLabels(data, factor) {
        first = [];
        second = [];
        if (Object.keys(data).includes("historical") && Object.keys(data.historical).includes(factor)) {
            first = Object.keys(data.historical[factor]);
        }
        if (Object.keys(data.linreg).includes(factor)) {
            second = Object.keys(data.linreg[factor]);
        }

        return first.concat(second);
    }

    function hasData(data, factor, enableHeavyComputing) {
        if (enableHeavyComputing) {
            return Object.keys(data.historical).includes(factor) && hasFactorData(data.historical, factor) ||
                    Object.keys(data.fbprophet).includes(factor) && hasFactorData(data.fbprophet, factor) ||
                    Object.keys(data.linreg).includes(factor) && hasFactorData(data.linreg, factor) ||
                    Object.keys(data.arima).includes(factor) && hasFactorData(data.arima, factor);
        } else {
            return Object.keys(data.historical).includes(factor) && hasFactorData(data.historical, factor) ||
                    Object.keys(data.linreg).includes(factor) && hasFactorData(data.linreg, factor) ||
                    Object.keys(data.arima).includes(factor) && hasFactorData(data.arima, factor);
        }
    }

    function applyPredictionOffset(data, offset) {
        return Array(offset).fill(null).concat(data);
    }

    function getDatasets(data, factor, predictionOffset, enableHeavyComputing) {
        datasets = [];
        if (Object.keys(data.historical).includes(factor)) {
            datasets.push({
                        label: 'Historical data',
                        data: Object.values(data.historical[factor]),
                        fill: false,
                        backgroundColor: 'rgb(255, 128, 0)',
                        borderColor: 'rgb(255, 128, 0)'
                    });
        }
        if (Object.keys(data.linreg).includes(factor)) {
            datasets.push({
                        label: 'Trend analysis prediction',
                        data: applyPredictionOffset(Object.values(data.linreg[factor]), predictionOffset),
                        fill: false,
                        backgroundColor: 'rgb(153, 153, 0)',
                        borderColor: 'rgb(153, 153, 0)'
                    });
        }
        if (enableHeavyComputing && Object.keys(data.fbprophet).includes(factor)) {
            datasets.push({
                        label: 'FBProphet prediction',
                        data: applyPredictionOffset(Object.values(data.fbprophet[factor]), predictionOffset),
                        fill: false,
                        backgroundColor: 'rgb(51, 51, 255)',
                        borderColor: 'rgb(51, 51, 255)'
                    });
        }
        if (Object.keys(data.arima).includes(factor)) {
            datasets.push({
                        label: 'ARIMA prediction',
                        data: applyPredictionOffset(Object.values(data.arima[factor]), predictionOffset),
                        fill: false,
                        backgroundColor: 'rgb(186, 85, 211)',
                        borderColor: 'rgb(186, 85, 211)'
                    });
        }

        return datasets;
    }

    function drawData(data, predictionOffset, enableHeavyComputing) {
        /* Hide unused canvas */
        canvases.map(c => c.style.display = hasData(data, c.id, enableHeavyComputing) ? "block" : "none")

        /* PM1 */
        var pm1 = new Chart(document.getElementById('pm1'), {
            type: 'line',
            data: {
                labels: mergeLabels(data, 'pm1'),
                datasets: getDatasets(data, 'pm1', predictionOffset, enableHeavyComputing)
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
                labels: mergeLabels(data, 'pm25'),
                datasets: getDatasets(data, 'pm25', predictionOffset, enableHeavyComputing)
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
                labels: mergeLabels(data, 'pm10'),
                datasets: getDatasets(data, 'pm10', predictionOffset, enableHeavyComputing)
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
                labels: mergeLabels(data, 'temperature'),
                datasets: getDatasets(data, 'temperature', predictionOffset, enableHeavyComputing)
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
                labels: mergeLabels(data, 'pressure'),
                datasets: getDatasets(data, 'pressure', predictionOffset, enableHeavyComputing)
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
                labels: mergeLabels(data, 'humidity'),
                datasets: getDatasets(data, 'humidity', predictionOffset, enableHeavyComputing)
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
                labels: mergeLabels(data, 'wind_speed'),
                datasets: getDatasets(data, 'wind_speed', predictionOffset, enableHeavyComputing)
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
            data: {

            },
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
                labels: mergeLabels(data, 'clouds'),
                datasets: getDatasets(data, 'clouds', predictionOffset, enableHeavyComputing)
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

    function fillStats(data, stats, name) {
        var table = document.getElementById(name);
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

    function fillDataTable(data, enableHeavyComputing) {
        var table = document.getElementById('datatable');
        var factors = ['pm1', 'pm25', 'pm10', 'temperature', 'pressure', 'humidity', 'wind_speed', 'wind_degree', 'clouds'];
        var sources = [];
        if (hasHistoricalData(data)) {
            sources.push('historical');
        }
        sources.push('linreg');
        sources.push('arima');
        if (enableHeavyComputing) {
            sources.push('fbprophet');
        }
        var sourcesFactorsData = {};
        for (var i = 0; i < sources.length; i++) {
            var factorsData = {};
            for (var j = 0; j < factors.length; j++) {
                if (hasFactorData(data[sources[i]], factors[j])) {
                    factorsData[factors[j]] = data[sources[i]][factors[j]];
                }
            }
            sourcesFactorsData[sources[i]] = factorsData;
        }
        if (hasAnyFactor(sourcesFactorsData)) {
            var sourceRow = table.insertRow();
            sourceRow.insertCell().appendChild(document.createTextNode(""));
            presentFactors = Object.keys(sourcesFactorsData['linreg']);
            for (var i = 0; i < sources.length; i++) {
                sourceRow.insertCell().appendChild(document.createTextNode(sources[i]));
                for (var j = 0; j < presentFactors.length - 1; j++) {
                    sourceRow.insertCell().appendChild(document.createTextNode(""));
                }
            }

            var headerRow = table.insertRow();
            headerRow.insertCell().appendChild(document.createTextNode("datetime"));
            for (var i = 0; i < sources.length; i++) {
                for (var j = 0; j < presentFactors.length; j++) {
                    headerRow.insertCell().appendChild(document.createTextNode(presentFactors[j]));
                }
            }

            var dates = mergeLabels(sourcesFactorsData, presentFactors[0]);
            for (var i = 0; i < dates.length; i++) {
                var row = table.insertRow();
                row.insertCell().appendChild(document.createTextNode(dates[i]));
                for (var j = 0; j < sources.length; j++) {
                    for (var k = 0; k < presentFactors.length; k++) {
                        var isUndefined = typeof sourcesFactorsData[sources[j]][presentFactors[k]][dates[i]] === 'undefined';
                        var cellData = isUndefined ? null : sourcesFactorsData[sources[j]][presentFactors[k]][dates[i]];
                        row.insertCell().appendChild(document.createTextNode(cellData));
                    }
                }
            }
        }
    }

    function hasAnyFactor(sourcesFactorsData) {
        return Object.keys(sourcesFactorsData['linreg']).length > 0;
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