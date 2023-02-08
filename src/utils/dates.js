const formatDate = date => {
    let year = date.getFullYear();
    let month = (date.getMonth() + 1).toString().padStart(2, '0');
    let day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
}

const todaysDate = () => formatDate(new Date());

function divideDatesIntoIntervals(startDate, endDate) {
    let currentDate = new Date(startDate);
    let nextDate = null;
    let monthInterval = 5;
    const end = new Date(endDate);
    const intervals = [];

    if(currentDate.getTime() === end.getTime())
        return [ [ formatDate(currentDate), formatDate(end) ] ]

    while(currentDate.getTime() < end.getTime()) {
        nextDate = new Date(currentDate);
        nextDate.setMonth(currentDate.getMonth() + monthInterval);
        //console.log(currentDate.toISOString() + " - " + nextDate.toISOString());
        //console.log(currentDate.getTime() + " - " + nextDate.getTime());
        //console.log(currentDate.getTime() < nextDate.getTime());
        if(nextDate.getTime() >= end.getTime()) 
            nextDate = new Date(endDate);
        intervals.push([ 
            formatDate(currentDate),
            formatDate(nextDate)
        ]);
        currentDate = new Date(nextDate);
    }
    return intervals;
}


/*
let startDate = '2023-02-05' // today's date
let endDate  = '2023-02-05' // today's date
console.log(divideDatesIntoIntervals(startDate,endDate))
*/

export { divideDatesIntoIntervals, todaysDate }
