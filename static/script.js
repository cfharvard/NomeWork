//Global variables
const timer_el = document.querySelector('.watch .time');
const start_btn = document.getElementById('start');
const stop_btn = document.getElementById('stop');
const reset_btn = document.getElementById('reset');
const submit_btn = document.getElementById('submit');

let seconds = 0;
let interval = null;

//Event listeners
start_btn.addEventListener('click', start);
stop_btn.addEventListener('click', stop);
reset_btn.addEventListener('click', reset);
submit_btn.addEventListener('click', submit);



// Update the timer
function timer() {
    seconds++;

    // Format our time
    let hrs = Math.floor(seconds / 3600);
    let mins = Math.floor(seconds - (hrs * 3600) / 60);
    let secs = seconds % 60;
    
    if (secs < 10) secs = '0' + secs;
    if (mins < 10) secs = '0' + mins;
    if (hrs < 10) secs = '0' + hrs;

    timer_el.innerHTML = `${hrs}:${mins}:${secs}`;
}

function start() {
    if (interval) {
        return
    }

    interval = setInterval(timer, 1000);
}

function stop() {
    clearInterval(interval);
    interval = null;
}

function reset() {
    stop();
    seconds = 0;
    timer_el.innerHTML = '00:00:00'
}

function submit() {
    return
}
