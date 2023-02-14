import config from '../../crawlee.json' assert { type: "json" };
import typesofProcesses from '../procesos.js';
import { divideDatesIntoIntervals, todaysDate } from '../utils/dates.js';
import handleLogin from './loginHandler.js';

/* this that make all the necessary initiation to begin scrapping
 * it handles which process to scrap,
 * it logins in if necessary,
 * it handles which dates to scrap
 * it divides the date range into intervals of dates
 * */
const handleInititation = async ({ crawler, page, log, proxyInfo }) => {
    // get dates from config file
    let { scrapThisMonth, scrapToday,
        startDate, endDate, divideDatesInMonths } = config;
    // import procesos   
    let { procesosDeContratacion } = typesofProcesses;
    // if processos de contratacion are enabled the
    // proceed to login
    if(procesosDeContratacion.isEnabled) {
        let cookies = await handleLogin( { crawler, page, log, proxyInfo } );
        if( ! cookies ) log.error('Could not log in');
    }
    // handle the dat to scrap
    if(scrapToday){
        log.info('Scraping today\'s Compras Publicas')
        // wait until it button loads
        startDate = todaysDate(); // today's date
        endDate  = todaysDate(); // today's date
    }
    /* add scrap this manth */
    // make batches for the date range
    let date_batches = 
        divideDatesIntoIntervals({
            startDate, 
            endDate, 
            intevalInMonths: divideDatesInMonths
        });
    // print to console
    log.info(`Made ${date_batches.length} date batches of ${divideDatesInMonths} months each between the dates of ${startDate} to ${endDate}`);
    log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);

    let requests = [];
    let procesos = Object
        .entries(typesofProcesses)
        .filter(p => p[1].isEnabled) 
    // for every enabled process
    for(let [type, process] of procesos ){
        // for every date range we call the
        for( let [ startDate, endDate ] of date_batches ){
            // add to our request list
            requests.push({
                method: 'GET',
                url: process.seachPageUrl,
                label: 'seach_page',
                uniqueKey: startDate + endDate + type,
                userData: {
                    dates: [startDate, endDate],
                    typeofProcess: type,
                },
            })
        }
    }
    // add the requests
    await crawler.addRequests( requests )
}

export default handleInititation
