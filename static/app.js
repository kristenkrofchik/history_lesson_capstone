window.onload = function() {
    const resourceSearchResults = document.querySelector('#resourceSearchResults');
    const searchTerm = document.querySelector('#searchTerm');
    const searchForm = document.querySelector('#searchForm');
    let userSearchResults = [];



    async function searchLibrary(query) {
        let result = await axios.get(`https://www.loc.gov/search/?q=${query}&fo=json`);
        let resultArray = result.data.results;
        console.log(resultArray);
        for(let i = 0; i < resultArray.length; i++) {
            let searchItemObj = resultArray[i];
            let searchItemShow = (({ id, title, description, date, url }) => ({ id, title, description, date, url }))(searchItemObj);
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
            itemDisplay.innerHTML = `<a data-id="${item.id}" class="resourceLink" href="${item.url}">${item.title}, ${item.description}, ${item.date}</a><p><a href="/resources/add" data-id="${item.id}" class="btn btn-primary addResource">Add Resource</a></p>`;
            resourceSearchResults.appendChild(itemDisplay);
        }
    }
}









