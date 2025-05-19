/*=============================================================
                Fetch elements from HTML
=============================================================*/
const openWindowBtn = document.querySelector(".upload-button");  // click to show Image Upload Window
const blurredBG = document.querySelector(".blurred-background"); // blurred backgound when openWindowBtn clicked
const uploadWindow = document.querySelector(".upload_window");   // image upload window
const closeWindowBtn = document.querySelector(".downside_upload"); //click to close Image Upload Window
const progressArea = document.querySelector(".progress-area");
const uploadedArea = document.querySelector(".uploaded-area");
const notification = document.querySelector(".notification"); // upload note when success or failed
// symbol for upload state
const checkSymbol = "fa-check";
const closeSymbol = "fa-close";
const loadingSymbol = "fa-spinner fa-pulse";


/*=============================================================
                Event Listener
=============================================================*/
//Image Upload Window open and close 
openWindowBtn.addEventListener("click", function () {
    blurredBG.style.display = "block";
    uploadWindow.style.display = "block";
});

closeWindowBtn.addEventListener("click", function () {
    blurredBG.style.display = "none";
    uploadWindow.style.display = "none";
    uploadedArea.innerHTML = "";
    notification.style.display = "none";
});


/*=============================================================
                Main function
=============================================================*/

// file upload 
function uploadFiles(file, domain_name, upload_url) {
    console.log("uploads: ");
    console.log(file);
    // check upload file's type
    let allowedExtensions = /(\.tif|\.fits)$/i; // /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if (!allowedExtensions.exec(file.name)) {
        // switch_notification_state("error", "Invalid Type");
        return;
    }

    // create a new package for data
    let form_data = new FormData();

    // check data is empty or not
    if (file.size == 0) {
        let message = "Please select a file to upload.";
        showError(message);
        return;
    }

    // put data into package
    form_data.append("files[]", file);


    //form_data.append("name", username); //There is no username (need update when coding on user share part)
    form_data.append("name", "username");
    form_data.append("domain_name", domain_name);

    // send data to backend
    $.ajax({
        type: "POST",
        processData: false,
        contentType: false,
        cache: false,
        url: upload_url,
        enctype: 'multipart/form-data',
        data: form_data,
        xhr: function () {  // function of progress and uploaded states
            let xhr = $.ajaxSettings.xhr();
            console.log("upload funciton ============================")
            xhr.upload.addEventListener("progress", ({ loaded, total }) => {
                // progress bar
                let fileLoaded = Math.floor((loaded / total) * 100); // getting percentage of loaded file size
                let fileTotal = Math.floor(total / 1000); // getting total file size in KB form bytes
                let fileSize;
                (fileTotal < 1024) ? fileSize = fileTotal + " KB" : fileSize = (loaded / (1024 * 1024)).toFixed(2) + " MB";
                console.log("fileLoaded: " + fileLoaded)
                console.log("fileSize: " + fileSize)
                // show notification to user
                // switch_notification_state("processing");

                let progressHTML = `
                    <li class="row">
                        <i class="image_icon"></i>
                        <div class="image-content">
                            <div class="details">
                                <span class="name">${file.name} • Uploading</span>
                                <span class="percent">${fileLoaded}%</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress" style="width: ${fileLoaded}%"></div>
                            </div>
                        </div>
                    </li>
                `;
                progressArea.innerHTML = progressHTML;
                if (loaded == total) {
                    // show upload info
                    progressArea.innerHTML = "";
                    console.log(file.name, getHash(file.name));
                    let uploadedHTML = `
                        <li class="row" id="id${getHash(file.name)}">
                            <div class="image-content upload">
                            <i class="fas fa-file-alt"></i>
                                <div class="details">
                                    <span class="name">${file.name} • <span class="state">Loading</span> </span> 
                                    <span class="size">${fileSize}</span>
                                </div>
                            </div>
                            <i class="fas ${loadingSymbol} symbol"></i>
                        </li>
                    `;
                    uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
                }
            });
            return xhr
        },
        dataType: 'json',
        success: function (response) {
            if (response.status == 200) {
                // show info to user
                // switch_notification_state("success");
                upload_card_result_handler(response);
                // add to image table
                var len = response.original_images.length;
                if (len > 0) {
                }

            } else {
                // show info to user
                // switch_notification_state("error", response.message)
                console.log("invalid: ", response.duplicatefiles)
                upload_card_result_handler(response);
                // upload_card_update("Error", getHash(response.original_images[0].name));
            }
        }
    });
}


// notification states switch
function switch_notification_state(state, errorInfo = "upload error") {
    notification.style.display = "block";
    if (notification.classList.contains("processing"))
        notification.classList.remove("processing");
    if (notification.classList.contains("error"))
        notification.classList.remove("error");
    if (notification.classList.contains("success"))
        notification.classList.remove("success");
    notification.classList.add(state);
    if (state == "success")
        notification.innerHTML = "Successfully stored.";
    else if (state == "processing")
        notification.innerHTML = "Uploaded, image analyzing ...";
    else
        notification.innerHTML = "Error: " + errorInfo;
}

// update card result handler
function upload_card_result_handler(response) {
    // handle with uploaded images
    console.log("RESPONSE",response)
    if (response.valid.length > 0) {
        let curState = document.querySelector(`#id${getHash(response.valid[0])} .state`);
        let curSymbol = document.querySelector(`#id${getHash(response.valid[0])} .symbol`);
        console.log("uploaded");
        console.log("curState:", curState);
        console.log("curSymbol:", curSymbol);
        curState.innerHTML = "Your image has been uploaded it will appear on your dashboard once its done proccessing.";
        curSymbol.classList.remove("fa-spinner");
        curSymbol.classList.remove("fa-pulse");
        curSymbol.classList.add("fa-check");
    }

    // handle with duplicate images
    if (response.duplicate.length > 0) {
        let curState = document.querySelector(`#id${getHash(response.duplicate[0])} .state`);
        let curSymbol = document.querySelector(`#id${getHash(response.duplicate[0])} .symbol`);
        console.log("duplicate");
        console.log("curState:", curState);
        console.log("curSymbol:", curSymbol);
        curState.innerHTML = "Duplicate file";
        curSymbol.classList.remove("fa-spinner");
        curSymbol.classList.remove("fa-pulse");
        curSymbol.classList.add("fa-close");
    }

    // handle with invalid images
    if (response.invalid.length > 0) {
        let curState = document.querySelector(`#id${getHash(response.invalid[0])} .state`);
        let curSymbol = document.querySelector(`#id${getHash(response.invalid[0])} .symbol`);
        console.log("invalid");
        console.log("curState:", curState);
        console.log("curSymbol:", curSymbol);
        curState.innerHTML = "Invalid file";
        curSymbol.classList.remove("fa-spinner");
        curSymbol.classList.remove("fa-pulse");
        curSymbol.classList.add("fa-close");
    }


}

/*=============================================================
                Helper Function
=============================================================*/
function getHash(input) {
    var hash = 0, len = input.length;
    const regex = /[0-9/A-Z/a-z/ /]/g;
    const letters = input.match(regex);
    input = letters.join("");
    for (var i = 0; i < len; i++) {
        hash = ((hash << 5) - hash) + input.charCodeAt(i);
        hash |= 0; // to 32bit integer
    }
    hash = Math.abs(hash);
    return hash;
}