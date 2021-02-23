//const resourceSearchResults = document.getElementById('resourceSearchResults');
//const searchButton = document.getElementById('searchButton');
let userSearchResults = [];

const $searchTerm = $("#searchTerm");
const $searchForm = $("#searchForm");
const $resourceSearchResults = $("#resourceSearchResults");


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


function addItems(results) {
    for(let item of results) {
        item = `<li>${item.title}</li>`;
        $resourceSearchResults.append(item);
    }
}

$searchForm.on("submit", async function(ev) {
    ev.preventDefault();

    let searchInput = $searchTerm.val();

    searchLibrary(searchInput);
});





