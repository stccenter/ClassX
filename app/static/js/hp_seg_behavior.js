
/******************************************************
                    Hidden and show
******************************************************/
// Color Cluster hidden and show
$('input[name="ColorClustCheck"]').click(function () {
    if ($(this).prop("checked") == "1") {
        $("#ColorClustCheckOn").show();
    }
    else if ($(this).prop("checked") == "0") {
        $("#ColorClustCheckOn").hide();
    }
});

// Region Merging hidden and show
$('input[name="RAGCheck"]').click(function () {
    console.log("Region Merging");
    if ($(this).prop("checked") == "1") {
        if ($("#menuRAG").val() == 2) {
            console.log("Region Merging is 2");
            // $("#RAGThresh").prop("disabled", true);
            $("#RAGOn2").hide();
        } else {
            // $("#RAGThresh").prop("disabled", false);
        }
        $("#RAGOn").show();
    }
    else if ($(this).prop("checked") == "0") {
        $("#RAGOn").hide();
    }
});
$("#menuRAG").on('change', function () {
    if ($("#menuRAG").val() == 2) {
        console.log("Region Merging is 2");
        // $("#RAGThresh").prop("disabled", true);
        $("#RAGOn2").hide()
    } else {
        // $("#RAGThresh").prop("disabled", false);
        $("#RAGOn2").show()
    }
})

// Small Feature hidden and show
$('input[name="small_rem"]').click(function () {
    if ($(this).prop("checked") == "1") {
        $("#SFROn").show();
    }
    else if ($(this).prop("checked") == "0") {
        $("#SFROn").hide();
    }
});
/******************************************************
            Input connect to progress bar
******************************************************/
// pro-processing Color Cluster
let ColorClustVal = document.getElementById("ColorClustVal");
let ColorCluster = document.getElementById("ColorCluster");
ColorCluster.value = 5;
ColorClustVal.value = ColorCluster.value;
function ColorClustInput(slideObj) {
    ColorClustVal.value = slideObj.value;
}
ColorClustVal.addEventListener("input", function () {
    ColorCluster.value = ColorClustVal.value;
});

// Watershed Segementation Gauss Sigma
let gaussSigma = document.getElementById("gaussSigma");
let gaussSigmaVal = document.getElementById("gaussSigmaVal");
gaussSigma.value = 7; // default value
gaussSigmaVal.value = gaussSigma.value;
function gaussSigmaInput(slideObj) {
    gaussSigmaVal.value = slideObj.value;
}
gaussSigmaVal.addEventListener("input", function () {
    gaussSigma.value = gaussSigmaVal.value;
});

// Watershed Segementation featureSep
let featureSep = document.getElementById("featureSep");
let featureSepVal = document.getElementById("featureSepVal");
featureSep.value = 10;
featureSepVal.value = featureSep.value;
function featureSepInput(slideObj) {
    featureSepVal.value = slideObj.value;
}
featureSepVal.addEventListener("input", function () {
    featureSep.value = featureSepVal.value;
});


// SLIC segmentation level
let seglvl = document.getElementById("seglvl");
let SegLvlVal = document.getElementById("SegLvlVal");
seglvl.value = 12;
SegLvlVal.value = seglvl.value;
function SegLvlInput(slideObj) {
    SegLvlVal.value = slideObj.value;
}
SegLvlVal.addEventListener("input", function () {
    seglvl.value = SegLvlVal.value;
});

// SLIC compacting
let Compact = document.getElementById("Compact");
let CompactVal = document.getElementById("CompactVal");
Compact.value = 5;
CompactVal.value = Compact.value;
function CompactInput(slideObj) {
    CompactVal.value = slideObj.value;
}
CompactVal.addEventListener("input", function () {
    Compact.value = CompactVal.value;
});


// SLIC Gauss Sigma
let EdgeSmooth = document.getElementById("EdgeSmooth");
let EdgeSmoothVal = document.getElementById("EdgeSmoothVal");
EdgeSmooth.value = 0.5;
EdgeSmoothVal.value = EdgeSmooth.value;
function EdgeSmoothInput(slideObj) {
    EdgeSmoothVal.value = slideObj.value;
}
EdgeSmoothVal.addEventListener("input", function () {
    EdgeSmooth.value = EdgeSmoothVal.value;
});

// Felzenswalb Gauss Sigma
let gaussSigmaF = document.getElementById("gaussSigmaF");
let gaussSigmaFVal = document.getElementById("gaussSigmaFVal");
gaussSigmaF.value = 0.8; // default value
gaussSigmaFVal.value = gaussSigmaF.value;
function gaussSigmaFInput(slideObj) {
    gaussSigmaFVal.value = slideObj.value;
}
gaussSigmaFVal.addEventListener("input", function () {
    gaussSigmaF.value = gaussSigmaFVal.value;
});

// Felzenswalb Scale
let scalefel = document.getElementById("scalefel");
let scalefelVal = document.getElementById("scalefelVal");
scalefel.value = 1; //default value
scalefelVal.value = scalefel.value;
function scalefelInput(slideObj) {
    scalefelVal.value = slideObj.value;
}
scalefelVal.addEventListener("input", function () {
    scalefel.value = scalefelVal.value;
});

// Felzenswalb Minimum Size
let minSize = document.getElementById("minSize");
let minSizeVal = document.getElementById("minSizeVal");
minSize.value = 20; //default value
minSizeVal.value = minSize.value;
function minSizeInput(slideObj) {
    minSizeVal.value = slideObj.value;
}
minSizeVal.addEventListener("input", function () {
    minSize.value = minSizeVal.value;
});

// Quickshift Gauss Sigma
let gaussSigmaQ = document.getElementById("gaussSigmaQ");
let gaussSigmaQVal = document.getElementById("gaussSigmaQVal");
gaussSigmaQ.value = 1.2; // default value
gaussSigmaQVal.value = gaussSigmaQ.value;
function gaussSigmaQInput(slideObj) {
    gaussSigmaQVal.value = slideObj.value;
}
gaussSigmaQVal.addEventListener("input", function () {
    gaussSigmaQ.value = gaussSigmaQVal.value;
});


// Quickshift Kernal Size
let kernalsize = document.getElementById("kernalsize");
let kernalsizeVal = document.getElementById("kernalsizeVal");
kernalsize.value = 3; // default value
kernalsizeVal.value = kernalsize.value;
function kernalsizeInput(slideObj) {
    kernalsizeVal.value = slideObj.value;
}
kernalsizeVal.addEventListener("input", function () {
    kernalsize.value = kernalsizeVal.value;
});

// Quickshift Maximum Distance
let maxDis = document.getElementById("maxDis");
let maxDisVal = document.getElementById("maxDisVal");
maxDis.value = 10;
maxDisVal.value = maxDis.value
function maxDisInput(slideObj) {
    maxDisVal.value = slideObj.value;
}
maxDisVal.addEventListener("input", function () {
    maxDis.value = maxDisVal.value;
});

// post processing Removal Threshhold
let rem_thresholdVal = document.getElementById("rem_thresholdVal");
let rem_threshold = document.getElementById("rem_threshold");
rem_threshold.value = 25;
rem_thresholdVal.value = rem_threshold.value;
function rem_thresholdInput(slideObj) {
    rem_thresholdVal.value = slideObj.value;
}
rem_thresholdVal.addEventListener("input", function () {
    rem_threshold.value = rem_thresholdVal.value;
});

// post processing Merging Threshold
let RAGThreshVal = document.getElementById("RAGThreshVal");
let RAGThresh = document.getElementById("RAGThresh");
RAGThresh.value = 10;
RAGThreshVal.value = RAGThresh.value;
function RAGThreshInput(slideObj) {
    RAGThreshVal.value = slideObj.value;
}
RAGThreshVal.addEventListener("input", function () {
    RAGThresh.value = RAGThreshVal.value;
});


/*
    Close Label Page 
*/
closeLabel.addEventListener("click", function () {
    labelSection.style.display = "none";
    let lens = document.querySelector(".img-zoom-lens");
    lens.style.width = `40px`;
    lens.style.height = `40px`;
})