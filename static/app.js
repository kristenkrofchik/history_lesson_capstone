/*const resourceSearchResults = document.getElementById('resourceSearchResults');
const searchBar = document.getElementById('searchBar');
let searchOptions = [];*/


/*searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();
    const filteredResults = resourceSearchResults.filter(result => {
        return result.name.toLowerCase().includes(searchString) || result.house.toLowerCase().includes(searchString);
    });
    displayResults(filteredResults);
});*/


async function searchLibrary(query) {
    let result = await axios.get(`https://www.loc.gov/search/?q=${query}&fo=json`);
    console.log(result.data.results)
}

/*const displayResults = (results) => {
	const htmlString = results
    	.map((result) => {
        	return `
            <li class='result'>
    			<h2>${result.name}</h2>
    			<p>House: ${result.house}</p>
    			<img src="${result.image}"></img>
            </li>
        `;
        })
        .join('');
    resourceSearchResults.innerHTML = htmlString;
};

loadCharacters();*/