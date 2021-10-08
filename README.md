# History Lesson

History Lesson is a web app built with PostgreSQL, Python and Flask that allows history teachers to plan and schedule lessons with primary resources from the Library of Congress API.

[Library of Congress API](https://www.loc.gov/apis/json-and-yaml/)

The Library of Congress API provides a means to retrieve data about Library of Congress collections in JSON format. The Library of Congress is the nation's oldest federal cultural institution and the de facto national library of the United States. Data is available for several collections including newspapers, books, archived websites, photos, and videos. The API is accessible to the public with no API key or authentication required. 

### Status
This project is still in process. Version 1 will be deployed in October, 2021. 

### Installation

1. Fork repository
2. Clone repository to local environment
3. Run pip install to install dependencies:

```bash
$ pip install
```
4. Run flask run to start the application:

```bash
$ flask run
```

### Technologies

[PostgreSQL](https://www.postgresql.org/docs/)

[Python](https://docs.python.org/3.9/)

[Flask](https://flask.palletsprojects.com/en/2.0.x/)

[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

[Axios](https://axios-http.com/docs/intro)

[Bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/)

### Features

#### Registration/Login

To access the app, users will register for the website on their first visit and login on each subsequent visit. 

#### User Homepage

The user homepage is dominated by a JavaScript calendar that will show the dates of the user's planned lessons, and link them to a form to add a lesson to their calendar. It will also include a navigation header where the user can access their profile, and links to other pages of the website.

#### User Profile

The user profile will show the user's information, which they can edit from here. The profile will also show the number of fellow users who follow that user, and the fellow users who they are following. These numbers will each link to a list of said users (a followers list and a following list). The followers/following feature will allow teachers to connect with like-minded educators and find inspiration in their saved lesson plans and resources. In a later version of the app, I will also implement a message feature so the users can directly communicate on the app (in the current state, they can choose to reach out to each other via the posted email information). 

#### Browse Users

This page will include a list of all of the app's users. Each list item will link to the profile of that user, and include a button for the logged in user to follow that user.

#### Add Lesson Plan

Each calendar date will include a link to this page, and there will also be a seperate button on the user's profile page that links to this page. This page includes a form where a user can add a lesson plan to their profile and calendar. It also allows the user to add a saved resource to the lesson plan.  

#### Search Resources

This page includes a search box where users can search for any topic they choose. The search term will be used to make an axios post request to the LOC API, and the data of the response will be displayed in a list. Each list item will be followed by a button that allows a user to add the resource to their profile. If clicked, this button will lead the user to a form to add the resource to their profile, and also connect it to a specific lesson plan if they choose. 

### Contributing
Pull requests are welcome. Please open an issue first to discuss what you would like to change.

### License
Kristen Krofchik
