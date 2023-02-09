import { divideDatesIntoIntervals, todaysDate } from '../utils/dates.js';
import { buscarProcesoRE } from '../urls.js'
import config from '../../crawlee.json' assert { type: "json" };

/* this is the code that divides the given date into difrnt batches 
 * the reason for thie function is not only to divided the logic,
 * but so that we can enqueue an Request so that we can use
 * other proxies. */
const handleDateDivision = async ({ crawler, page, log, proxyInfo }) => {
    // get dates from config file
    let { scrapThisMonth, scrapToday, 
        startDate, endDate } = config;
    // dates to scrap
    if(scrapToday){
        log.info('Scrap compras publicas of today')
        // wait until it button loads
        startDate = todaysDate(); // today's date
        endDate  = todaysDate(); // today's date
    }
    // make batches for the date range
    let date_batches = 
        divideDatesIntoIntervals(
            startDate, endDate
        );
    log.info(`Made ${date_batches.length} date batches of 6 months each between the dates of ${startDate} to ${endDate}`);
    log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);
    // for every date range we call the 
    for( let dates of date_batches ){
        await crawler
            .requestQueue
            .addRequest({
                method: 'GET',
                url: buscarProcesoRE,
                uniqueKey: startDate + '-' + endDate,
                label: 'seach_page',
                userData: { startDate, endDate },
            })
    }
}

export default handleDateDivision
