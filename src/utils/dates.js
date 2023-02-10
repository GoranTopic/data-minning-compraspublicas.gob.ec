const formatDate = date => 
    date.toISOString().split('T')[0];

const todaysDate = () => formatDate(new Date());

function divideDatesIntoIntervals({ startDate, endDate, intevalInMonths}) {
    intevalInMonths = intevalInMonths ?? 3
    let currentDate = new Date(startDate);
    let end = new Date(endDate);
    let nextDate = null;
    let monthInterval = intevalInMonths;
    let intervalInMs = monthInterval * 30 * 24 * 60 * 60 * 1000;
    let intervals = [];

    // if start date is grater than end date
    if(currentDate.getTime() > end.getTime())
        throw new Error('is the start date greater the end date?')

    // if the dates are the same
    if(currentDate.getTime() === end.getTime())
        return [ [ formatDate(currentDate), formatDate(end) ] ]
    // if the dates a smaller than teh range
    if( (end.getTime() - currentDate.getTime()) <= intervalInMs)
        return [ [ formatDate(currentDate), formatDate(end) ] ]
    
    //else calculate teh intervals
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
/*
let testdate1 = '2022-2-1'
console.log(testdate1, formatDate(new Date(testdate1)) )
*/
 
export { divideDatesIntoIntervals, todaysDate }
