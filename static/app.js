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
            
            itemDisplay.innerHTML = `<form method="POST" action="/api/resources"><a data-id="${item.id}" class="resourceLink" href="${item.url}">${item.title}, ${item.description}, ${item.date}</a><button class="btn btn-secondary btn-sm m-1y addResource" data-id="${item.id}" data-title="${item.title}" data-description="${item.description}" data-url="${item.url}">Add Resource</button></form>`
     
            resourceSearchResults.appendChild(itemDisplay);
        }
    }

    resourceSearchResults.addEventListener('click', function(ev) {
        if(ev.target.tagName === 'button') {
            const resourceId = ev.target.dataset.id;
            const resourceTitle = ev.target.dataset.title;
            const resourceDescription = ev.target.dataset.description;
            const resourceUrl = ev.target.dataset.url;

            let json = JSON.stringify({
                id: resourceId,
                title: resourceTitle,
                description: resourceDescription,
                url: resourceUrl
            })

        axios.post(`http://127.0.0.1:5000/api/resources`, {json})
            .then(response => {
                console.log(response);
        })
            .catch(error => {
                console.log(error);
            });
        }
    })
}

/*const newLessonButton = document.querySelector(".newLessonButton")

newLessonButton.addEventListener('click', function(ev) {
    ev.preventDefault();

    const lessonTitle = document.querySelector(".title").value;
    const lessonSummary = document.querySelector(".summary").value;
    const lessonDate = document.querySelector(".date").value;

    let json = JSON.stringify({
        title: lessonTitle,
        summary: lessonSummary,
        date: lessonDate,
    })

    axios.post(`http://127.0.0.1:5000/api/lessons/add`, {json})
            .then(response => {
                console.log(response);
        })
            .catch(error => {
                console.log(error);
            });
    
    

})*/

/*itemDisplay.innerHTML = `<form method="post"><a data-id="${item.id}" class="resourceLink" href="${item.url}">${item.title}, ${item.description}, ${item.date}</a><p><a href="/api/resources" data-id="${item.id}" data-title="${item.title}" data-description="${item.description}" data-url="${item.url}" class="btn btn-secondary btn-sm m-1 addResource">Add Resource</a></p></form>`;
            resourceSearchResults.appendChild(itemDisplay);*/


















