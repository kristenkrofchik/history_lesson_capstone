
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

    document.querySelector('.date h1').innerHTML = months[date.getMonth()];

    document.querySelector('.date p').innerHTML = new Date().toDateString();

    let days = '';

    for(let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date"><h5>${prevLastDay - x + 1}</h5><a class="calendarLink" href="/lessons/new">Add Lesson</></div>`;
    }

    for(let i = 1; i <= lastDay; i++) {
        if(i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            days += `<div class="today"><h5>${i}<h5><a class="calendarLink" href="/lessons/new">Add Lesson</></div>`;
        } else {
            days += `<div"><h5>${i}<h5><a class="calendarLink" href="/lessons/new">Add Lesson</></div>`;
        }
    }

    for(let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date"><h5>${j}<h5><a class="calendarLink" href="/lessons/new">Add Lesson</></div>`;
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

//add onclick event for addLesson button. add the class "seeLessons" to that day.
//if a date has seeLessons just maybe change color and link to lesson plan

//make axios request ti iur database to get the startdate