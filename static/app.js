
$(document).ready(function() {
    const $resourceSearchResults = $('#resourceSearchResults');
    const $searchTerm = $('#searchTerm');
    const $searchForm = $('#searchForm');
    let $userId = parseInt(location.pathname.split('/')[2]);
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
    $searchForm.on("submit", async function(ev) {
        ev.preventDefault();
        let searchInput = $searchTerm.val();
        searchLibrary(searchInput);
    });

    //adds html of the results from the searchLibrary function above to the page
    function addItems(results) {

        for(let item of results) {
            let itemDisplay = `<li><form method="POST" action="http://127.0.0.1:5000/users/${$userId}/resources/search"><a data-id="${item.id}" class="resourceLink" href="${item.url}">${item.title}, ${item.description}, ${item.date}</a><button class="btn btn-secondary btn-sm m-1y addResource" data-id="${item.id}" data-title="${item.title}" data-description="${item.description}" data-url="${item.url}">Add Resource</button></form></li>`;
     
            $resourceSearchResults.append(itemDisplay);
        }
    }

    //this function adds a resource to the user's resource list on click of 'Add Resource' button
    //makes a post request to the Python API to add resource to database
    $('body').on('click', 'button.addResource', function() {
        
        let json = JSON.stringify({
            id: $(this).attr("data-id"),
            title: $(this).attr("data-title"),
            description: $(this).attr("data-description"),
            url: $(this).attr("data-url")
        })

        console.log(json);

        axios.post(`http://127.0.0.1:5000/users/${$userId}/resources/search`, json)
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.log(error);
            });
        });
});

//when lesson is submitted, add date to localstorage so we can use it in calendar.js to change calendar html

const $newLessonForm = $(".new-lesson-form");

$newLessonForm.on('submit', function() {
    let $lessonDate = $("#add_lesson_date").val();
    let events = [];
    events.push({
        date: $lessonDate
    });
    localStorage.setItem('events', JSON.stringify(events));
});





















