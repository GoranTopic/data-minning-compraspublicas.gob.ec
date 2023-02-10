import { divideDatesIntoIntervals, todaysDate } from '../utils/dates.js';
import config from '../../crawlee.json' assert { type: "json" };
import { buscarProcesoRE } from '../urls.js'
import Checklist from '../utils/Checklist.js'


/* this is the code that divides the given date into difrnt batches 
 * the reason for thie function is not only to divided the logic,
 * but so that we can enqueue an Request so that we can use
 * other proxies. */
const handleDateDivision = async ({ crawler, page, log, proxyInfo }) => {
    // total number of compras per date range
    global.TOTAL_COMPRAS_COUNT = 0;
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
    // print to console
    log.info(`Made ${date_batches.length} date batches of 7 months each between the dates of ${startDate} to ${endDate}`);
    log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);

    // make a check list for the dates
    let dateChecklist = new Checklist(
        'dates_checklist', date_batches,
        process.cwd() + '/' + config.storageDir
        + '/datasets/' + config.defaultDatasetId
    )

        // for every date range we call the 
    for( let dates of date_batches ){
        // if it is not checked off already
        if( ! dateChecklist.isCheckedOff(dates) ){
            log.debug(`dates ${dates} are not checked out`)
            let [ startDate, endDate ] = dates;
            await crawler
                .requestQueue
                .addRequest({
                    method: 'GET',
                    url: buscarProcesoRE,
                    uniqueKey: startDate + '-' + endDate,
                    label: 'seach_page',
                    userData: { startDate, endDate },
                })
        }else
            log.debug(`dates ${dates} are checked out`)
    }

}

export default handleDateDivision
