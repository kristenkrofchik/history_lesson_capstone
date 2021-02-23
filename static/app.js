const resourceSearchResults = document.getElementById('resourceSearchResults');
const searchButton = document.getElementById('searchButton');
let userSearchResults = [];


async function searchLibrary(query) {
    let result = await axios.get(`https://www.loc.gov/search/?q=${query}&fo=json`);
    let resultArray = result.data.results;
    for(let i = 0; i < resultArray.length; i++) {
        searchItemObj = resultArray[i];
        searchItemShow = (({ title, description, url }) => ({ title, description, url }))(searchItemObj);
        userSearchResults.push(searchItemShow);
    }
}

/*function searchBox(ev) {
    ev.preventDefault();
    const searchString = ev.target.value.toLowerCase();
    searchLibrary(searchString);
}*/

searchButton.addEventListener('click', (ev) => {
    const searchString = ev.target.value.toLowerCase();
    searchLibrary(searchString);

    for(let result in userSearchResults) {
        for(let [key, value] of Object.entries(result)) {
            
        }
    }


