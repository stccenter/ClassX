/*
    Croppped Image Library page management
    #page = #image / 8 + (#image % 8  > 0 ? 1 : 0);
*/
let imgNum = 0;
let pageNum = 0;
let switchBtnNum = 0;
let switchBtnList = [];
const pageSwitchArea = document.querySelector(".page-switch");
const topRow = document.querySelector(".top-row");
const botRow = document.querySelector(".bottom-row");
let cards = null;

let topCount = 0;// track number of cards on top row 
let botCount = 0;// track number of cards on bottom row


/*
page switch on click
*/

pageSwitchArea.addEventListener('click', e => {
    if (e.target.classList.contains("page")) {
        Array.from(pageSwitchArea.children).forEach(item =>
            item.classList.remove("active")
        );
        for (let i = 0; i < pageNum; i++) {
            if (pageSwitchArea.children[i] == e.target) {
                topRow.style.transform = `translateX(-${i / pageNum * 100}%)`;
                botRow.style.transform = `translateX(-${i / pageNum * 100}%)`;
                console.log(e)
                e.target.classList.add("active")
            }
        }
    }
})


/*
    reload library function
    argument: pageSwitchControl_flag, openModal_target
*/

function loadLib(flag, target) {
    // reset library structure
    imgLibReset()
    // set pageswitch match with number of images
    pageSwitchControl(flag);

    addContent();
    if (CROPPEDIMG.length > 0) {
        openModal(target);
    }

    cards = document.getElementsByClassName("card");
    Array.from(cards).forEach(function (card) {
        card.addEventListener("click", function () {
            // highlight click card
            Array.from(cards).forEach(item =>
                item.classList.remove("card-active")
            );
            card.classList.add("card-active");
            let activeCard = document.querySelector(".card-active .img");
            let sideBarPreviewImageTmp = document.querySelector("#preview");
            sideBarPreviewImageTmp.style.backgroundImage = activeCard.style.backgroundImage;
        });
    });
}

/*
    Image Library - reset
*/
function imgLibReset() {
    // reset basic counts
    imgNum = CROPPEDIMG.length;
    pageNum = Math.ceil(imgNum / 8);
    switchBtnNum = pageNum;
    // reset top and bot row counts
    topCount = 0;
    botCount = 0;
    // reset gallery
    topRow.innerHTML = "";
    botRow.innerHTML = "";
    // reset pageswitch
    pageSwitchArea.innerHTML = "";
}

/*
    Add page switch btn based on number of images
*/
function pageSwitchControl(isAdd) {
    for (let i = 0; i < switchBtnNum; i++) {
        let div = document.createElement("div");
        if (i == 0) {
            div.setAttribute("class", "page active");
        } else {
            div.setAttribute("class", "page");
        }
        switchBtnList.push(div);
        pageSwitchArea.appendChild(div);
    }

    // if it is first time load, default to first page
    if (!isAdd) {
        // switchBtnList[0].classList.add("active");
    } else {// if it is adding new cropped image, default to last page4
        switchBtnList[switchBtnList.length - 1].classList.add("active");
    }

}

/*
    adding 8 * #page cards, half on top-row, half on bottom-row
*/
function addCards() {
    let topRemind = pageNum * 4 - topCount;
    let botRemind = pageNum * 4 - botCount;
    for (let i = 0; i < topRemind; i++) {
        let div = document.createElement("div");
        div.setAttribute("class", "card");
        topRow.appendChild(div);
    }
    for (let i = 0; i < botRemind; i++) {
        let div = document.createElement("div");
        div.setAttribute("class", "card");
        botRow.appendChild(div);
    }
}



/*
   Image Library - add
   based on number of top-row image and bot-row images to deside new card location
*/
function imgLibAdd(id) {
    if (topCount > botCount) {
        botRow.appendChild(makeCard(id));
        botCount++;
    } else {
        topRow.appendChild(makeCard(id));
        topCount++;
    }
}

/*
    Add images to gallery
*/
function addContent() {
    // for each cropped, add it to gallery
    for (let i = 0; i < imgNum; i++) {
        imgLibAdd(i);
    }
    // add empty cards to empty gallery space
    addCards();
    // resize top-row and bot-row width 
    topRow.style.width = `calc(50vw*${pageNum})`;
    botRow.style.width = `calc(50vw*${pageNum})`;
}

