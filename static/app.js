window.onload = function() {
    const resourceSearchResults = document.querySelector('#resourceSearchResults');
    const searchTerm = document.querySelector('#searchTerm');
    const searchForm = document.querySelector('#searchForm');
    let userSearchResults = [];


    //uses the user's entered search query from the addEventListener function below to make an axios call to the LOC API.
    //return the results in a list on the page using the addItems function below
    async function searchLibrary(query) {
        let result = await axios.get(`https://www.loc.gov/search/?q=${query}&fo=json`);
        let resultArray = result.data.results;
        for(let i = 0; i < resultArray.length; i++) {
            let searchItemObj = resultArray[i];
            let searchItemShow = (({ id, title, description, date, url }) => ({ id, title, description, date, url }))(searchItemObj);
            userSearchResults.push(searchItemShow);
        }
        addItems(userSearchResults);
    }

    //grabs the user's search on submit of the search button. passes it to the searchLibrary function above.
    searchForm.addEventListener("submit", async function(ev) {
        ev.preventDefault();

        let searchInput = searchTerm.value;
        searchLibrary(searchInput);
    });

    //adds html of the results from the searchLibrary function above to the page
    function addItems(results) {

        for(let item of results) {
            itemDisplay = document.createElement('li');
            
            itemDisplay.innerHTML = `<form method="POST" action="/api/resources"><a data-id="${item.id}" class="resourceLink" href="${item.url}">${item.title}, ${item.description}, ${item.date}</a><button class="btn btn-secondary btn-sm m-1y addResource" data-id="${item.id}" data-title="${item.title}" data-description="${item.description}" data-url="${item.url}">Add Resource</button></form>`
     
            resourceSearchResults.appendChild(itemDisplay);
        }
    }

    //this function adds a resource to the user's resource list on click of 'Add Resource' button
    //makes a post request to the Python API to add resource to database
    document.body.addEventListener('click', function(event) {
        if(event.target.className === 'btn btn-secondary btn-sm m-1y addResource') {
            const resourceId = event.target.dataset['id'];
            const resourceTitle = event.target.dataset['title'];
            const resourceDescription = event.target.dataset['description'];
            const resourceUrl = event.target.dataset['url'];

            let resource = {};
            resource[id] = resourceId;
            resource[title] = resourceTitle;
            resource[description] = resourceDescription;
            resource[url] = resourceUrl;

        axios.post(`http://127.0.0.1:5000/api/resources`, JSON.stringify(resource), {headers: {"content-type": "application/json"},
        })
            .then(response => {
                console.log(response);
        })
            .catch(error => {
                console.log(error);
            });
        }
    })
}

//this code will add info to specific date on js calender when new lesson is added to that date

const newLessonButton = document.querySelector(".newLessonButton")

newLessonButton.addEventListener('click', function() {
    const lessonDate = document.getElementById("add_lesson_date").value;
    const dateArr = lessonDate.split('-');

})



















