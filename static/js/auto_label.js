
/*
    Porbability Threshold
    - Set reading value equal to prograss bar value
*/
function PThresholdInput(slideObj) {
    PThresholdVal.innerHTML = slideObj.value;
}

/*
    Auto label confirm BTN
    - Using training file to label current segmented image
*/
autoLabelConfirm.addEventListener('click', function Auto_Label() {
    let algo_id = document.querySelector('#model_selection').value;
    let training_file_id = document.querySelector('#label_file_selection').value;
    currentTrainingFile = training_file_id;
    PThresholdVal.innerHTML = PThreshold.value;
    let prob_threshold1 = PThreshold.value
    console.log(algo_id);
    console.log(segID);
    console.log(prob_threshold1);
    console.log("training_file_id:", training_file_id);

    $.ajax({
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        data: {
            segment_image_id: segID,
            prob_threshold: prob_threshold1,
            algorithm_id: algo_id,
            training_file_id: training_file_id
        },
        url: autoLabelImageURL,
        success: function (response) {
            loadSegmentImage(image_click);
            if (response.status != 200) {
                console.log("error: ", response.error)
            } else {
                notification("Auto labeled segment image.", "#5cb85c", "#000", "20px");
            }
        }
    })
});

/*
        Show bar chart in Label Page
    */
function showChart(label_class_count, winWidth) {
    let dps = [];

    dps.push({ y: 0, label: 'Uncategory', color: "#72bf77" })
    for (let i = 0; i < labelmap.length; i++) {
        dps.push({ y: 0, label: labelmap[i].name, color: labelmap[i].color })
    };

    let chartWidth = 400;
    let chartHeight = 330;
    if (winWidth < 1600) {
        chartWidth = 300;
        chartHeight = 230;
    }

    let chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2", // "light1", "light2", "dark1", "dark2",
        title: {
            text: "Number of segments labeled by class",
            fontSize: 16,
        },
        width: chartWidth,
        height: chartHeight,
        axisX: {
            interval: 1,
            labelAngle: -70,
            labelFontSize: 10,
            titleFontSize: 10,
        },
        axisY: {
            title: "Segments count",
            labelFontSize: 10,
            titleFontSize: 10,
        },
        data: [{
            type: "column",
            dataPoints: dps,
            colorSet: "customColorSet"
        }]

    });
    function parseDataPoints() {
        $.each(label_class_count, function (i, label) {
            dps[label[0]].y = label[1];
        })
    };
    parseDataPoints();
    chart.render();
}

/*
    Show pie chart in Label Page
*/
function showPieChart(segment_area, winWidth) {
    let dps = [];
    colorMap = {};
    colorMap[0] = { "name": "Uncategory", "color": "#72bf77" };
    for (var i = 0; i < labelmap.length; i++) {
        colorMap[labelmap[i].id] = { "name": labelmap[i].name, "color": labelmap[i].color };
    };


    let chartWidth = 400;
    let chartHeight = 330;
    if (winWidth < 1600) {
        chartWidth = 300;
        chartHeight = 230;
    }

    let chart = new CanvasJS.Chart("pieChartContainer",
        {
            theme: "light2",
            title: {
                text: "Segment Area in % of Pixels",
                fontSize: 16,
            },
            width: chartWidth,
            height: chartHeight,
            data: [{
                type: "pie",
                indexLabelFontSize: 10,
                radius: 120,
                toolTipContent: "#percent %",
                yValueFormatString: "#,##,###",
                indexLabel: "{label} #percent%",
                dataPoints: dps,
                indexLabelLineColor: "darkgrey",
                colorSet: "customColorSet"
            }]
        }
    );

    chart.render();
    function parseDataPoints() {
        $.each(segment_area, function (i, item) {
            dps.push({ y: item, label: colorMap[i]["name"], color: colorMap[i]["color"] });
        })
    };
    parseDataPoints();
    chart.render();
}