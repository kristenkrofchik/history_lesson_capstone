//this code creates a vanilla js calendar and adds it to the user's home page.
console.log(localStorage);
const date = new Date();

const renderCalendar = () => {
    date.setDate(1);

    const monthDays = document.querySelector('.days');

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();

    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();

    const firstDayIndex = date.getDay();

    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();

    const nextDays = 7 - lastDayIndex - 1;

    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const monthsNumber = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    document.querySelector('.date h1').innerHTML = months[date.getMonth()];

    //grab current month to add to class
    let currentMonth = monthsNumber[date.getMonth()];

    document.querySelector('.date p').innerHTML = new Date().toDateString();

    //grab current year to add to class
    let currentYear = document.querySelector('.date p').innerHTML.slice(-4);

    let days = '';

    let userId = parseInt(location.pathname.split('/')[2]);

    for(let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date calDate ${x}"><h5>${prevLastDay - x + 1}</h5><a class="calendarLink" href="/users/${userId}/lessons/new">Add Lesson</></div>`;
    }

    for(let i = 1; i <= lastDay; i++) {
        if(i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            if(i < 10) {
                i = '0' + i;
            }
            days += `<div class="today calDate ${currentYear}-${currentMonth}-${i}"><h5>${i}<h5><a class="calendarLink" href="/users/${userId}/lessons/new">Add Lesson</></div>`;
        } else {
            if(i < 10) {
                i = '0' + i;
            }
            days += `<div class="calDate ${currentYear}-${currentMonth}-${i}"><h5>${i}<h5><a class="calendarLink" href="/users/${userId}/lessons/new">Add Lesson</></div>`;
        }
    }

    for(let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date calDate"><h5>${j}<h5><a class="calendarLink" href="/users/${userId}/lessons/new">Add Lesson</></div>`;
        monthDays.innerHTML = days;
    }
}


document.querySelector('.prev').addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
})

document.querySelector('.next').addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
})


renderCalendar();

//get dates with events from local storage.
//loop through events and add 'Lesson planned' to any day with event
//further functionality-- add link to lesson. need to store lesson id in localstorage

let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

function showHasEvents() {
    for(let i = 0; i < events.length; i++) {
        let day = document.getElementsByClassName(`${events[i].date}`)[0];
        let htmlString = '<p class="addLessonText">Lesson planned!</p>';
        day.insertAdjacentHTML('beforeend', htmlString);
    }
}

showHasEvents();



