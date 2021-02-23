const resourceSearchResults = document.getElementById('resourceSearchResults');
const searchBar = document.getElementById('searchBar');
let userSearchResults = [];


searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();
    searchLibrary(searchString);
    displayResults(searchString);
});


async function searchLibrary(query) {
    let result = await axios.get(`https://www.loc.gov/search/?q=${query}&fo=json`);
    console.log(result);
    let resultArray = result.data.results;
    console.log(resultArray);
    for(let i = 0; i < resultArray.length; i++) {
        searchItemObj = resultArray[i];
        searchItemShow = (({ title, description, url }) => ({ title, description, url }))(searchItemObj);
        userSearchResults.push(searchItemShow);
    }
}

const displayResults = (userSearchresults) => {
	const htmlString = userSearchresults
    	.map((result) => {
        	return `
            <li class='result'>
    			<h2>${result.title}</h2>
    			<p>House: ${result.description}</p>
    			<a href="${result.url}">Link</a>
            </li>
        `;
        })
        .join('');
    resourceSearchResults.innerHTML = htmlString;
};

