/*=============================================================
                Fetch elements from HTML
=============================================================*/
const userSet = new Set();
const IMAGE_FILTER_TAG_ID_DICT = new Map();
const FILTERS = document.getElementById("filters");
const displayFilterBtn = document.querySelector("#filter_display_btn");
const filterContainer = document.querySelector(".filter_container");
const dropLeft = document.querySelector(".drop_left");
const dropDown = document.querySelector(".drop_down");
const filterBtns = document.querySelector(".filter_btns");

/*=============================================================
                Event Listener
=============================================================*/
displayFilterBtn.addEventListener('click', function () {
    filterContainer.classList.toggle("hide_filter");
    filterContainer.classList.toggle("show_filter");
    dropLeft.classList.toggle("show");
    dropDown.classList.toggle("show");
    filterBtns.classList.toggle("hide_height");
});

/*=============================================================
                Main function
=============================================================*/
function collEventListener() {
    let coll = document.getElementsByClassName("collapsible");
    let i;
    for (i = 0; i < coll.length; i++) {
        console.log("coll at" + i)
        coll[i].addEventListener("click", function () {
            this.classList.toggle("active");
            let content = this.nextElementSibling;
            let plus = this.getElementsByClassName("plus")[0];
            let minus = this.getElementsByClassName("minus")[0];
            if (content.style.display === "block") {
                minus.style.display = "none"
                plus.style.display = "block"
                content.style.display = "none";
            } else {
                plus.style.display = "none"
                minus.style.display = "block"
                content.style.display = "block";
            }
        });
    }
}

/*
  filterCteater
  input: 
    - json file
  output
    - reset IMAGE_FILTER_TAG_ID_DICT
    -  create parent div
    - create corresponding tag for each image filter
  using function
    - imageFilterCheckBoxArchitect
    - imageFilterDateArchitect
    - imageFilterUserArchitect
    - imageFilterMinMaxArchitect
  used by 
    - document.ready

*/
function filterCreater(dict, target) {
    // reset IMAGE_FILTER_TAG_ID_DICT
    if (IMAGE_FILTER_TAG_ID_DICT.size > 0) {
        for (const [key, value] of IMAGE_FILTER_TAG_ID_DICT)
            IMAGE_FILTER_TAG_ID_DICT.delete(key);
    }

    const userList = USERS; // backend is empty for user_list
    const userList_test = [];
    imageFilterUserArchitect(userList_test, FILTERS);

    // preprocess dict
    // filterList : [name, {type:checkbox/numeric..., data:[...]}]
    console.log("Object.entries(dict)", Object.entries(dict));
    // TODO: based on order from backend
    for (const filterList of Object.entries(dict)) {
        if (filterList[1].type == 'checkbox') {
            console.log("Create checkbox structure")
            console.log(filterList)
            imageFilterCheckBoxArchitect(filterList, FILTERS);
        }
        if (filterList[1].type == 'date') {
            console.log("Create date structure")
            imageFilterDateArchitect(filterList, FILTERS);
        }
        if (filterList[1].type == 'minmax') {
            console.log("Create minmax structure")
            imageFilterMinMaxArchitect(filterList, FILTERS);
        }
    }
    // check all checkbox
    var filter_checkboxs = document.querySelectorAll("#filter-form input[type='checkbox']");
    for (let i = 0; i < filter_checkboxs.length; i++) {
        filter_checkboxs[i].checked = true;
    }
    console.log("add EventListener")
    collEventListener();
}

/*
   imageFilterCheckBoxArchitect, imageFilterDateArchitect, 
   imageFilterUserArchitect, imageFilterMinMaxArchitect
   input: 
     - string name 
     - filterList
         filterList[0]: name of that filter
         filterList[1].type: type of that filter 
         filterList[1].data: data of that filter will use
     - parent html tag
   output
     - store readable html id or class for later data exchange
     - build html tag by dict data
     - add html structure to parent html tag
     - add corresponding name tag to IMAGE_FILTER_TAG_ID_DICT
   using function
     - 
   used by 
     - filterCreater
 */
function imageFilterCheckBoxArchitect(filterList, FILTERS) {

    // common variable
    const name = string_convertor(filterList[0]);
    const idList = [];
    // create doucment tag
    const outerDiv = document.createElement("div");
    const nameLabel = document.createElement("button")
    const img_plux = document.createElement("img")
    const img_minus = document.createElement("img")

    // set document attribute
    setAttributes(outerDiv, { "class": "collapsible_content" })
    nameLabel.textContent = name;

    // create checkboxs
    for (let tags of filterList[1].data) {
        // common variable 
        let id = filterList[0] + '_' + tags;

        // create tags
        let cBox = document.createElement("input")
        let br = document.createElement("br")
        let cBoxLabel = document.createElement("label")

        // set attribute
        cBox.setAttribute("type", "checkbox")
        cBox.setAttribute("id", id)
        cBox.setAttribute("name", id)
        cBoxLabel.textContent = tags
        cBoxLabel.setAttribute("for", id)

        // add to outerDiv
        outerDiv.appendChild(cBox)
        outerDiv.appendChild(cBoxLabel)
        outerDiv.appendChild(br)

        // Store id into idList
        idList.push(id)
    }

    // set attribute
    setAttributes(nameLabel, { "class": "collapsible", "type": "button" })
    setAttributes(img_plux, { "src": plusSymbol, "class": "collapsible_icon plus" })
    setAttributes(img_minus, { "src": minusSymbol, "class": "collapsible_icon minus" })
    //tags structure
    nameLabel.appendChild(img_plux)
    nameLabel.appendChild(img_minus)
    // tag structure
    outerDiv.setAttribute("id", "chechbox1")
    FILTERS.appendChild(nameLabel)
    FILTERS.appendChild(outerDiv)

    // add idList to IMAGE_FILTER_TAG_ID_DICT
    IMAGE_FILTER_TAG_ID_DICT.set(filterList[0], idList);
}

function imageFilterDateArchitect(filterList, FILTERS) {
    // common variable
    const name = string_convertor(filterList[0]);
    const idList = [];
    const startID = filterList[0] + '_start';
    const endID = filterList[0] + '_end';

    // store date relative id to 
    idList.push(startID, endID);
    IMAGE_FILTER_TAG_ID_DICT.set(filterList[0], idList);


    // create doucment tags
    const outerDiv = document.createElement("div");
    const nameLabel = document.createElement("button");
    const img_plux = document.createElement("img")
    const img_minus = document.createElement("img")

    // set document tags' attribute
    setAttributes(outerDiv, { "class": "collapsible_content" })
    nameLabel.textContent = name;
    setAttributes(nameLabel, { "class": "collapsible", "type": "button" })
    setAttributes(img_plux, { "src": plusSymbol, "class": "collapsible_icon plus" })
    setAttributes(img_minus, { "src": minusSymbol, "class": "collapsible_icon minus" })

    // create child tags
    let startDate = document.createElement("input");
    let endDate = document.createElement("input");
    let br1 = document.createElement("br");
    let br2 = document.createElement("br");
    let startDateLabel = document.createElement("label");
    let endDateLabel = document.createElement("label");
    let startDateDiv = document.createElement("div");
    let endDateDiv = document.createElement("div");

    // set child tags' attribute
    setAttributes(startDate, { "type": "date", "id": startID, "name": startID });
    setAttributes(endDate, { "type": "date", "id": endID, "name": endID });
    startDateLabel.textContent = "Start Date";
    startDateLabel.setAttribute("for", startID);
    endDateLabel.textContent = "End Date";
    endDateLabel.setAttribute("for", endID);

    // tag structure
    nameLabel.appendChild(img_plux)
    nameLabel.appendChild(img_minus)
    FILTERS.appendChild(nameLabel);
    startDateDiv.appendChild(startDateLabel);
    startDateDiv.appendChild(br1);
    startDateDiv.appendChild(startDate);
    endDateDiv.appendChild(endDateLabel);
    endDateDiv.appendChild(br2);
    endDateDiv.appendChild(endDate);
    outerDiv.appendChild(startDateDiv);
    outerDiv.appendChild(endDateDiv);
    FILTERS.appendChild(outerDiv);
}


function imageFilterMinMaxArchitect(filterList, FILTERS) {
    // common variables
    const id = filterList[0];
    const name = string_convertor(filterList[0]);
    const idList = [];

    // adding IMAGE_FILTER_TAG_ID_DICT 
    idList.push(id + '_min', id + '_max');
    IMAGE_FILTER_TAG_ID_DICT.set(id, idList)

    // create document tags
    const outerDiv = document.createElement("div")
    const nameLabel = document.createElement("button")
    const minDiv = document.createElement("div")
    const maxDiv = document.createElement("div")
    const minLabel = document.createElement("label")
    const maxLabel = document.createElement("label")
    const minInput = document.createElement("input")
    const maxInput = document.createElement("input")
    const img_plux = document.createElement("img")
    const img_minus = document.createElement("img")

    // set document tags' attribute
    nameLabel.textContent = name;
    setAttributes(nameLabel, { "class": "collapsible", "type": "button" })
    setAttributes(outerDiv, { "class": "minmax collapsible_content" })
    minLabel.textContent = "min"
    maxLabel.textContent = "max"
    setAttributes(minInput, { "type": "number", "id": id + "_min", "name": id + "_min", "step": "any", "min": filterList[1].data['min'], "max": filterList[1].data['max'] })
    setAttributes(maxInput, { "type": "number", "id": id + "_max", "name": id + "_max", "step": "any", "min": filterList[1].data['min'], "max": filterList[1].data['max'] })
    setAttributes(minDiv, { "class": "minmaxElement" })
    setAttributes(maxDiv, { "class": "minmaxElement" })
    setAttributes(img_plux, { "src": plusSymbol, "class": "collapsible_icon plus" })
    setAttributes(img_minus, { "src": minusSymbol, "class": "collapsible_icon minus" })
    //tags structure
    nameLabel.appendChild(img_plux)
    nameLabel.appendChild(img_minus)
    outerDiv.appendChild(minDiv)
    outerDiv.appendChild(maxDiv)
    minDiv.appendChild(minLabel)
    maxDiv.appendChild(maxLabel)
    minDiv.appendChild(minInput)
    maxDiv.appendChild(maxInput)
    FILTERS.appendChild(nameLabel)
    FILTERS.appendChild(outerDiv)
}
/*
imageFilterUserArchitect
input: 
  - user list
  - parent html tag
output
  - store readable html id or class for later data exchange
  - build html tag by dict data
  - add html structure to parent html tag
  - add corresponding name tag to IMAGE_FILTER_TAG_ID_DICT
using function
  - 
used by 
  - filterCreater
*/
function imageFilterUserArchitect(filterList, FILTERS) {
    console.log("imageFilterUserArchitect");
    console.log(filterList);
    console.log("add user")

    let outerDiv = document.createElement("div")
    let nameLabel = document.createElement("button");
    let selection = document.createElement("select");
    const img_plux = document.createElement("img")
    const img_minus = document.createElement("img")


    for (let i of filterList) {
        let option = document.createElement("option")
        option.setAttribute("value", i);
        option.textContent = i;
        selection.appendChild(option);
        setAttributes(option, { "value": i })
    }

    let result = document.createElement("span");
    nameLabel.textContent = "Shared by"
    setAttributes(outerDiv, { "class": "collapsible_content" })
    setAttributes(nameLabel, { "class": "collapsible", "type": "button" })
    setAttributes(img_plux, { "src": plusSymbol, "class": "collapsible_icon plus" })
    setAttributes(img_minus, { "src": minusSymbol, "class": "collapsible_icon minus" })
    setAttributes(selection, { "name": "user", "id": "selectUser" });


    selection.addEventListener("change", (event) => {
        output = selection.options[selection.selectedIndex].value;
        if (!userSet.has(output)) {
            console.log("userSet dont have ", output)
            userSet.add(output)
            let item = document.createElement("span");
            let label = document.createElement("label");
            let closeX = document.createElement("span");
            setAttributes(closeX, { "id": output })
            closeX.textContent = " x";
            closeX.onclick = function () {
                console.log("delete ", this.id)
                userSet.delete(this.id);
                this.parentNode.remove();
                return false;
            }
            label.textContent = output;
            item.appendChild(label)
            item.appendChild(closeX);
            result.appendChild(item);
        }
    });
    nameLabel.appendChild(img_plux)
    nameLabel.appendChild(img_minus)
    FILTERS.appendChild(nameLabel);
    outerDiv.appendChild(selection);
    outerDiv.appendChild(result);
    FILTERS.appendChild(outerDiv);
}


/*
  clearInput (Dynamic)
  - clear input in filter table
*/
function clearInput() {
    // reset value for each input under filter table
    var filter_inputs = document.querySelectorAll("#filter-form input[type='number']");
    for (let i = 0; i < filter_inputs.length; i++) {
        filter_inputs[i].value = "";
    }
    var filter_checkboxs = document.querySelectorAll("#filter-form input[type='checkbox']");
    for (let i = 0; i < filter_checkboxs.length; i++) {
        filter_checkboxs[i].checked = true;
    }
    //Post filter result to backend
    searchBackend("")
}
/*=============================================================
                Helper Function
=============================================================*/
/*
set attribute for html tag
*/
function setAttributes(el, attrs) {
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}
function string_convertor(str) {
    return (str[0].toUpperCase() + str.substring(1)).replaceAll("_", " ");
}