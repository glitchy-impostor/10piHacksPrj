var text = "";

var date = new Date();
var startHour = date.getHours();
var startMinute = date.getMinutes();
var startSecond = date.getSeconds();



class Time
{
    constructor(hours, minutes, seconds)
    {
        this.hours = hours;
        this.minutes = minutes;
        this.seconds = seconds;
    }
}

start = new Time(startHour, startMinute, startSecond)

var task = new Time(2, 30, 56);

var estimatedSeconds = start.seconds + task.seconds;
var estimatedMinutes = start.minutes + task.minutes;
var estimatedHours = start.hours + task.hours;

if(estimatedSeconds >= 60)
{
    estimatedMinutes += Math.floor(estimatedSeconds / 60);
    estimatedSeconds = estimatedSeconds % 60;
}

if(estimatedMinutes >= 60)
{
    estimatedHours += Math.floor(estimatedMinutes / 60);
    estimatedMinutes = estimatedMinutes % 60;
}

function getTime(t)
{
    return t.hours + ":" + t.minutes + ":" + t.seconds;
}


var estimatedTime = new Time(estimatedHours, estimatedMinutes, estimatedSeconds);

text += estimatedTime.getTime();

document.getElementById("time").innerHTML = text;
