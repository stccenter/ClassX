/*=============================================================
                Fetch elements from HTML
=============================================================*/
const TABLE = document.getElementById("imageTable");
const curPageTag = document.getElementById("currentPage");
const totalPageTag = document.getElementById("totalPages");
let currentPage = 1;
let rowsPerPage = 8;
let totalRows = 0;
let totalPages = 0;

const monthsShort = {
    Jan: '01',
    Feb: '02',
    Mar: '03',
    Apr: '04',
    May: '05',
    Jun: '06',
    Jul: '07',
    Aug: '08',
    Sep: '09',
    Oct: '10',
    Nov: '11',
    Dec: '12',
};
// image Table row

// Image table related variable

/*=============================================================
                Event Listener
=============================================================*/



/*=============================================================
                Main function
=============================================================*/
/*  
  addRow (dynamic)
  - addRow on clearInput
  - addRow on document.Ready 
      a. uploadFiles
      b. search bar
  - {"id" : i.id, "name": i.name, 
     "uploader_name" : uploader_name, 
     "upload_time": i.upload_time, 
     "size" : i.size, "width" : i.width, 
     "height": i.height, "light":i.light,
     "longitude":i.longitude, "latitude":i.latitude, 
     "altitude":i.altitude, "fstop":i.fstop, "gps_date":i.mode, 
     "pitch":i.pitch, "roll":i.pitch, "roll":i.roll, 
     "shutter_speed":i.shutter_speed, "alias": i.alias, 
     "thumbnail_path":i.thumbnail_path}
*/
function addRow(id, alias, name, time, creation_date, user, size, width, height, light, thumbnail_path, metadata) {
    // Insert a row at the end of the table
    let newRow = TABLE.insertRow(1);
    newRow.id = "tr_" + id;

    // Insert a cell in the row at index 0
    let preCell = newRow.insertCell(0);
    let nameCell = newRow.insertCell(1);
    let timeCell = newRow.insertCell(2);
    timeCell.className = "hideable";
    let creationCell = newRow.insertCell(3);
    creationCell.className = "hideable";
    let userCell = newRow.insertCell(4);
    userCell.className = "hideable";
    let sizeCell = newRow.insertCell(5);
    sizeCell.className = "hideable";
    let dimCell = newRow.insertCell(6);
    dimCell.className = "hideable";
    let actionCell = newRow.insertCell(7);


    //*************************Index Zero column******************************************/
    // preCell.style.backgroundColor = "red";
    preCell.style.backgroundImage = `url(/static/${thumbnail_path})`;

    let imgInfo = document.createElement("div");
    imgInfo.setAttribute("data-toggle", "modal");
    imgInfo.setAttribute("image_name", name);
    imgInfo.setAttribute("data-target", '#preview' + id);
    let metaStr = "";
    for (let key in metadata) {
        // let value = isNaN(metadata[key]) ? metadata[key] : Number(metadata[key]).toFixed(4);
        let value = metadata[key];
        if (key == "longitude" || key == "latitude")
            value = isNaN(metadata[key]) ? metadata[key] : Number(metadata[key]).toFixed(6);
        metaStr = metaStr + string_convertor(key) + ": " + value + "<br>"
    }

    imgInfo.innerHTML = metaStr;
    preCell.appendChild(imgInfo);

    //*************************Index One column******************************************/
    //first div
    //console.log('addRow First column')
    let divElement = document.createElement("div");
    divElement.className = "d-flex align-items-center"
    let divElement0 = document.createElement("div");
    divElement0.setAttribute('style', 'display: flex;')

    //second div
    let divElement1 = document.createElement("div");
    divElement1.className = "ms-3";
    let input1 = document.createElement('input');
    input1.setAttribute('type', 'text');
    input1.setAttribute('id', 'myInput_' + id);
    input1.setAttribute('style', 'display: none');
    input1.setAttribute('placeholder', 'Image Alias...');
    divElement1.appendChild(input1);



    let pElement1 = document.createElement("p");
    pElement1.className = "fw-normal mb-1";
    pElement1.setAttribute('id', 'myInput2_' + id);
    pElement1.setAttribute('style', 'display: inline-block');
    //Image name text
    let nameText = document.createTextNode(name);
    let aliasText = null; // Initialize the alias text node to null

    // Check if the alias is different from the name
    if (alias !== name) {
        aliasText = document.createTextNode(' (' + alias + ')'); // Create the alias text node
    }
    let spaceText = document.createTextNode(' ');
    let ficonElement1 = document.createElement('i');
    let tooltip = document.createElement("span");


    let spaceText1 = document.createTextNode(' ');
    let btnElement2 = document.createElement("button");
    btnElement2.className = " action-button  btn-secondary";
    btnElement2.setAttribute('id', 'showInputButton_' + id);
    btnElement2.setAttribute("onclick", `goHomepage(${id})`);
    btnElement2.setAttribute('type', 'button');
    btnElement2.setAttribute('value', id);
    btnElement2.setAttribute('style', 'display: inline-block; background-color: var(--primary);');



    let ficonElement2 = document.createElement('i');
    ficonElement2.className = "fas fa-external-link-alt";
    ficonElement2.setAttribute("aria-hidden", "true");
    btnElement2.appendChild(ficonElement2);
    btnElement2.appendChild(document.createTextNode(" View"));

    let btnElement3 = document.createElement("button");
    btnElement3.className = " btn  btn-secondary";
    btnElement3.setAttribute('id', 'aliasInputButton_' + id);
    btnElement3.setAttribute('onclick', 'ImageAliasInput(this)');
    btnElement3.setAttribute('type', 'button');
    btnElement3.setAttribute('style', 'display: none; background-color: var(--primary);');
    btnElement3.setAttribute('alias', id);
    btnElement3.setAttribute('OGname', name);

    let ficonElement3 = document.createElement('i');
    ficonElement3.className = "fa fa-save";
    ficonElement3.setAttribute("aria-hidden", "true");
    ficonElement3.setAttribute('style', 'display: inline-block; background-color: var(--primary);');

    btnElement3.appendChild(ficonElement3);
    pElement1.appendChild(btnElement3);

    pElement1.appendChild(nameText);
    if (aliasText !== null) {
        pElement1.appendChild(aliasText); // Append the alias text node
    }
    pElement1.appendChild(spaceText);
    pElement1.appendChild(tooltip);
    pElement1.appendChild(spaceText1);
    pElement1.appendChild(btnElement2);
    let tooltipList = new bootstrap.Tooltip(tooltip, {
        delay: { show: 200, hide: 100 } // Add a slight delay to hide the tooltip on mouse leave
    });

    tooltip.addEventListener("mouseenter", function () {

        tooltipList.show();
    });

    // Add mouseleave event to hide the tooltip when the mouse leaves the tag
    tooltip.addEventListener("mouseleave", function () {

        tooltipList.hide();
    });

    let pElement2 = document.createElement('p');
    pElement2.className = "text-muted mb-0";
    //Source text
    let sourceText = document.createTextNode("Source:");
    pElement2.appendChild(sourceText);
    divElement1.appendChild(pElement1);
    divElement1.appendChild(spaceText);
    divElement1.appendChild(btnElement2);
    divElement1.appendChild(btnElement3);

    divElement1.appendChild(spaceText1);
    divElement1.appendChild(tooltip);

    divElement1.appendChild(pElement2);

    //second div append to first div
    divElement.appendChild(divElement1)

    //first div append to td
    nameCell.appendChild(divElement);
    //*************************Second column upload time******************************************/
    let pElement3 = document.createElement('p');
    pElement3.className = "fw-normal mb-1";
    //time text

    var time_split = time.split(' ')
    month = monthsShort[time_split[2]];
    var time_fmt = time_split[3] + '-' + month + '-' + time_split[1] + ' ' + time_split[4]
    //console.log(time_fmt)
    let timeText = document.createTextNode(time_fmt);
    pElement3.appendChild(timeText)
    timeCell.appendChild(pElement3);
    //*************************Third column******************************************/
    let pElement7 = document.createElement('p');
    pElement7.className = "fw-normal mb-1";
    //time text

    var creation_date = creation_date.split(' ')
    month = monthsShort[creation_date[2]];
    var time_fmt = creation_date[3] + '-' + month + '-' + creation_date[1] + ' ' + creation_date[4]
    //console.log(time_fmt)
    timeText = document.createTextNode(time_fmt);
    pElement7.appendChild(timeText)
    creationCell.appendChild(pElement7);
    //*************************Fourth column******************************************/
    let pElement4 = document.createElement('p');
    pElement4.className = "fw-normal mb-1";
    let userText = '';
    if (user == 'default') {
        userText = document.createTextNode('Administrator');
    }
    else {
        userText = document.createTextNode(user);
    }
    pElement4.appendChild(userText)
    userCell.appendChild(pElement4);
    //*************************Fifth column******************************************/
    let pElement5 = document.createElement('p');
    pElement5.className = "fw-normal mb-1";
    //size text
    let sizeText = document.createTextNode(size);
    pElement5.appendChild(sizeText)
    sizeCell.appendChild(pElement5);
    //*************************Sixth column******************************************/
    let pElement6 = document.createElement('p');
    pElement6.className = "fw-normal mb-1";
    //dimension text
    let dimText = document.createTextNode(width + ', ' + height);
    pElement6.appendChild(dimText)
    dimCell.appendChild(pElement6);
    //*************************Seventh column******************************************/
    let cropAnchor = document.createElement("a");
    cropAnchor.href = "/crop"+'?original_image_id=' + id;
    let cropButton = document.createElement("button");
    cropButton.className = "action-button open-cropping-tool";
    cropButton.setAttribute("type", "button");
    let cropIcon = document.createElement("i");
    cropIcon.className = "fas fa-crop";
    cropButton.appendChild(cropIcon);
    cropButton.appendChild(document.createTextNode("Crop Image"));
    cropAnchor.appendChild(cropButton);

    let deleteButton = document.createElement("a");
    deleteButton.href = "#";
    deleteButton.className = "btn btn-secondary";
    deleteButton.setAttribute("style", "background-color: var(--primary);");
    let trashIcon = document.createElement("i");
    trashIcon.className = "fas fa-trash";
    // deleteButton.appendChild(trashIcon);
    divElement0.appendChild(cropAnchor);
    // divElement0.appendChild(deleteButton);
    actionCell.appendChild(divElement0);
    document.addEventListener("DOMContentLoaded", function () {
        let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    });

    //*************************Image Previews******************************************/
    $("#previews").append('<div class="modal fade" id="preview' + id + '" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true"> <div class="modal-dialog" role="document" style="max-width: 70%;"> <div class="modal-content"> <div class="modal-header"> <h5 class="modal-title" id="exampleModalLabel"> ' + name + ' </h5> <button type="button" class="close" data-dismiss="modal" aria-label="Close"> <span aria-hidden="true"> × </span> </button> </div> <div class="modal-body" style="margin: auto;"> <img src="/static/' + thumbnail_path + '" /> </div> </div> </div> </div>');

    //*************************Page System******************************************/

    totalRows = TABLE.rows.length - 1;
    totalPages = Math.ceil(totalRows / rowsPerPage);
    totalPageTag.innerHTML = totalPages;
}


/*
    prevPage
    - previous page of images
  */
function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        displayRows();
    }
}

/*
  nextPage
  - next page of images
*/
function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        displayRows();
    }
}

/*
  !!gotoPage
  - not used yet
*/
function gotoPage() {
    var page = parseInt(document.getElementById("goToPage").value);
    if (page >= 1 && page <= totalPages) {
        currentPage = page;
        displayRows();
    }
}

/*
 displayRows
 - the function used under prevPage, nextPage, and gotoPage
*/
function displayRows() {
    var startRow = (currentPage - 1) * rowsPerPage + 1;
    var endRow = Math.min(startRow + rowsPerPage - 1, totalRows);
    console.log("startRow: ", startRow);
    console.log("endRow: ", endRow);
    for (var i = 1; i <= totalRows; i++) {
        var row = TABLE.rows[i];
        if (i >= startRow && i <= endRow) {
            row.style.display = "table-row";
        } else {
            row.style.display = "none";
        }
    }
    document.getElementById("currentPage").innerHTML = currentPage;
    document.getElementById("totalPages").innerHTML = totalPages;
}

/*=============================================================
                Helper Function
=============================================================*/