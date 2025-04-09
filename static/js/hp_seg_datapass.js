/*
    marked boundary function
*/
function savePre(confirmNum, val) {
    if (val == 0) {
        confirm("Please select algorithm to make boundary.");
        return;
    }
    // display preview section
    prevewSection.style.display = "block";

    // get ID of cropped image (TODO: update id, username)
    let id = cropID;
    let username = "123";

    let param1 = 0;
    let param2 = 0;
    let param3 = 0;

    // convert form to array
    let form = $("#segmentForm");
    let form_data = form.serializeArray();
    console.log("after serializeArray: ", form_data);
    // Region Merging checked
    let menuRAG = $("#menuRAG").val();

    // For Color Clustering
    let menuColor = $("#menuColor").val();

    let value = val;
    if (value == "1") {
        param1 = gaussSigma.value;
        param2 = 0;
        param3 = featureSep.value;
    } else if (value == "2") {
        param1 = seglvl.value;
        param2 = Compact.value;
        param3 = EdgeSmooth.value;
    } else if (value == "3") {
        param1 = kernalsize.value;
        param2 = maxDis.value;
        param3 = gaussSigmaQ.value;
    } else {
        param1 = gaussSigmaF.value;
        param2 = scalefel.value;
        param3 = minSize.value;
    }
    form_data.push(
        {
            name: 'menu',
            value: val
        },
        {
            name: 'name',
            value: username
        },
        {
            name: 'id',
            value: id
        },
        {
            name: 'menuRAG',
            value: menuRAG
        },
        {
            name: 'menuColor',
            value: menuColor
        },
        {
            name: 'confirm',
            value: confirmNum
        },
        {
            name: 'param1',
            value: param1
        },
        {
            name: 'param2',
            value: param2
        },
        {
            name: 'param3',
            value: param3
        });

    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(form_data),
        url: segmentPreviewURL,
        beforeSend: function () {
            if (confirmNum == 1) {
                $('#wait').show();
            }
        },
        success: function (response) {
            console.log("response:", response)
            //console.log("response[0].hist_name:", response[0].hist_name)
            $('#wait').hide();
            if (response.status == 199) {
                if (confirm(response.error)) {
                    savePre(1, value);
                } else {
                    prevewSection.style.display = "none";
                }
            } else if (response.status == 100) {
                savePre(1, value)
            } else {
                if (response.status == 400) {
                    alert(response.error);
                }
                else {
                    if (response.length == 1) {
                        currentSEGIMG = response[0].hist_method;
                        previewImage.appendChild(imagePreviewMakeCard(response[0], false));
                    } else {
                        let topRow = document.querySelector(".preview-top-row");
                        let botRow = document.querySelector(".preview-bot-row");
                        for (let i = 0; i < response.length; i++) {
                            if (i % 2 == 0) {
                                topRow.appendChild(imagePreviewMakeCard(response[i], true));
                            } else {
                                botRow.appendChild(imagePreviewMakeCard(response[i], true));
                            }
                        }
                    }
                }
            }
        }
    })
}


/*
    Save image
*/
function savePreview(imgObj, val) {

    // crop image id
    let id = cropID;
    let username = "123";

    // segmentation setting detail
    let form = $("#segmentForm");
    let form_data = form.serializeArray();

    let menuRAG = $("#menuRAG").val();
    let menuColor = $("#menuColor").val();
    let chk = document.getElementById("checkboxid");
    let param1 = 0;
    let param2 = 0;
    let param3 = 0;

    // segmentation algorithm id
    let value = val;
    if (value == "1") {
        param1 = gaussSigma.value;
        param2 = 0;
        param3 = featureSep.value;
    }
    else if (value == "2") {
        param1 = seglvl.value;
        param2 = Compact.value;
        param3 = EdgeSmooth.value;
    }
    else if (value == "3") {
        param1 = kernalsize.value;
        param2 = maxDis.value;
        param3 = gaussSigmaQ.value;
    }
    else {
        param1 = gaussSigmaF.value;
        param2 = scalefel.value;
        param3 = minSize.value;
    }
    form_data.push(
        {
            name: 'menu',
            value: val
        },
        {
            name: 'name',
            value: username
        },
        {
            name: 'id',
            value: id
        },
        {
            name: 'menuRAG',
            value: menuRAG
        },
        {
            name: 'menuColor',
            value: menuColor
        },
        {
            name: 'hist_method',
            value: imgObj
        },
        {
            name: 'param1',
            value: param1
        },
        {
            name: 'param2',
            value: param2
        },
        {
            name: 'param3',
            value: param3
        });
    console.log("form data: ", form_data)
    $.ajax({
        type: 'POST',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(form_data),
        url: segmentSaveURL,
        success: function (response) {
            console.log("response1.image:", response.image)
            if (response.status == 404) {
                alert(response.error);
            }
            else {
                if (response.status == 200) {
                    console.log("response.image:", response.image)
                    segGallery.addCardToList(response.image);
                    segGallery.reset();
                    segGallery.addContentToGallery();
                    segGallery.pageSwitchControl()
                    segGallery.addEvent()
                    noSegmentYet.style.display = "none";
                }
                notification("Segmented Image Saved.", "#5cb85c", "#000", "20px")
            }
        }
    })
}

function loadSegImgByCropImgID(id) {
    let username = "123"
    console.log("loadSegImgByCropImgID:", id)
    $.ajax({
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        data: {
            crop_image_id: id,
        },
        url: loadAllSegementImg,
        success: function (response) {
            console.log("response: ", response)
            if (response.length == 0) {
                console.log("No segment images.");
            } else {
                console.log("response:", response)
                for (var i = 0; i < response.length; i++) {
                    segGallery.addCardToList(response[i]);
                }
                segGallery.addContentToGallery();
                segGallery.pageSwitchControl()
                segGallery.addEvent()
                if (segGallery.list.length > 0) {
                    noSegmentYet.style.display = "none";
                } else {
                    noSegmentYet.style.display = "block";
                }
                /*
                    Compare Window - initialization
                */
                compareLoadImage();
            }
        }
    })
}