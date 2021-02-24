import Datepickk from "./datepickk";

window.onload = function() {
    const resourceSearchResults = document.querySelector('#resourceSearchResults');
    const searchTerm = document.querySelector('#searchTerm');
    const searchForm = document.querySelector('#searchForm');
    let userSearchResults = [];



    async function searchLibrary(query) {
        let result = await axios.get(`https://www.loc.gov/search/?q=${query}&fo=json`);
        let resultArray = result.data.results;
        for(let i = 0; i < resultArray.length; i++) {
            let searchItemObj = resultArray[i];
            let searchItemShow = (({ title, description, url }) => ({ title, description, url }))(searchItemObj);
            userSearchResults.push(searchItemShow);
        }
        addItems(userSearchResults);
    }

    searchForm.addEventListener("submit", async function(ev) {
        ev.preventDefault();

        let searchInput = searchTerm.value;
        searchLibrary(searchInput);
    });

    function addItems(results) {

        for(let item of results) {
            itemDisplay = document.createElement('li');
            itemDisplay.innerHTML = `<a href="${item.url}">${item.title}, ${item.description}</a>`;
            resourceSearchResults.appendChild(itemDisplay);
        }
    }
}

let datepicker = new Datepickk();
datepicker.show();






