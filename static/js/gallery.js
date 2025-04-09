class Gallery {
    constructor(cardList, makeCard, cardPerPage, target, arrowLeft, arrowRight) {
        // gallery div
        this.gallery = document.createElement("div");
        this.gallery.setAttribute("class", "Gallery");
        // list to store all images
        this.list = cardList;
        // user customize make card function
        this.makeCard = makeCard;
        // card per page
        this.cardPerPage = cardPerPage;
        // number of page
        this.pageNum = Math.ceil(this.list.length / cardPerPage);
        // setup top and bot count
        this.topCount = 0;
        this.botCount = 0;
        // page switch area
        this.pageSwitchArea = document.createElement("div");
        this.pageSwitchArea.setAttribute("class", "page-switch")
        // switch Btn 
        this.switchBtnList = [];
        // parent div for gallery and page switch
        this.target = target;
        // switch page by arrow
        this.arrowLeft = arrowLeft;
        this.arrowRight = arrowRight;
        this.currentPage = 0;
    }

    initialization() {
        // create HTML element 
        this.topRow = document.createElement("div")
        this.botRow = document.createElement("div")
        this.topRow.setAttribute("class", "top-row");
        this.botRow.setAttribute("class", "bot-row");
        this.gallery.appendChild(this.topRow);
        this.gallery.appendChild(this.botRow);
        this.target.appendChild(this.gallery);
        this.target.parentNode.parentNode.appendChild(this.pageSwitchArea);
    }
    /*
        reset gallery 
    */
    reset() {
        this.topCount = 0;
        this.botCount = 0;
        this.topRow.innerHTML = "";
        this.botRow.innerHTML = "";
        this.pageSwitchArea.innerHTML = "";
    }

    /*
        add to list
    */
    addCardToList(imgObj) {
        this.list.push(imgObj);
        this.pageNum = Math.ceil(this.list.length / this.cardPerPage);
    }
    /*
        add card to gallery
    */
    addContentToGallery() {
        // iterate list to add card  
        for (let i = 0; i < this.list.length; i++) {
            if (this.topCount > this.botCount) {
                this.botRow.appendChild(this.makeCard(i));
                this.botCount++;
            } else {
                this.topRow.appendChild(this.makeCard(i));
                this.topCount++;
            }
        }
        // add empty card to the empty space 
        let topRemind = this.pageNum * this.cardPerPage / 2 - this.topCount;
        let botRemind = this.pageNum * this.cardPerPage / 2 - this.botCount;
        console.log(topRemind);
        for (let i = 0; i < topRemind; i++) {
            console.log("insert card to top");
            let div = document.createElement("div");
            div.setAttribute("class", "seg-card");
            this.topRow.appendChild(div);
        }
        for (let i = 0; i < botRemind; i++) {
            console.log("insert card to bot");
            let div = document.createElement("div");
            div.setAttribute("class", "seg-card");
            this.botRow.appendChild(div);
        }

        // resize top-row and bot-row width 
        this.topRow.style.width = `calc(42vw*${this.pageNum})`;
        this.botRow.style.width = `calc(42vw*${this.pageNum})`;
    }
    /*
        add page switch to gallery
    */

    pageSwitchControl() {
        for (let i = 0; i < this.pageNum; i++) {
            let div = document.createElement("div");
            div.setAttribute("class", "page");
            if (i == 0) {
                div.classList.add("active");
            }
            div.setAttribute("pageNum", i);
            this.switchBtnList.push(div);
            this.pageSwitchArea.appendChild(div);
        }
    }

    addEvent() {
        this.pageSwitchArea.addEventListener('click', e => {
            console.log(this)
            if (e.target.classList.contains("page")) {
                this.currentPage = parseInt(e.target.getAttribute("pageNum"));
                Array.from(this.pageSwitchArea.children).forEach(item =>
                    item.classList.remove("active")
                );
                for (let i = 0; i < this.pageNum; i++) {
                    if (this.pageSwitchArea.children[i] == e.target) {
                        this.topRow.style.transform = `translateX(-${i / this.pageNum * 100}%)`;
                        this.botRow.style.transform = `translateX(-${i / this.pageNum * 100}%)`;
                        e.target.classList.add("active")
                    }
                }
            }
        })
        /*
            page switch by arrow
        */
        this.arrowLeft.addEventListener('click', e => {
            // check if next page is in the range
            if (this.currentPage > 0) {
                this.currentPage--;
                this.topRow.style.transform = `translateX(-${this.currentPage / this.pageNum * 100}%)`;
                this.botRow.style.transform = `translateX(-${this.currentPage / this.pageNum * 100}%)`;
                Array.from(this.pageSwitchArea.children).forEach(item =>
                    item.classList.remove("active")
                );
                Array.from(this.pageSwitchArea.children).forEach(item => {
                    if (parseInt(item.getAttribute('pageNum')) == this.currentPage) {
                        item.classList.add("active");
                    }
                });
            }
        });

        this.arrowRight.addEventListener('click', e => {
            // check if next page is in the range
            if (this.currentPage + 1 < this.pageNum) {
                this.currentPage++;
                this.topRow.style.transform = `translateX(-${this.currentPage / this.pageNum * 100}%)`;
                this.botRow.style.transform = `translateX(-${this.currentPage / this.pageNum * 100}%)`;
                Array.from(this.pageSwitchArea.children).forEach(item =>
                    item.classList.remove("active")
                );
                Array.from(this.pageSwitchArea.children).forEach(item => {
                    if (parseInt(item.getAttribute('pageNum')) == this.currentPage) {
                        item.classList.add("active");
                    }
                });
            }
        });

    }
}

