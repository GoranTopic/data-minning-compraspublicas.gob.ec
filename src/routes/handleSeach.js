import { divideDatesIntoIntervals, todaysDate } from '../utils/dates.js';
import { queryComprasPage, queryProcessesCount, decode } from '../reverse_engineering/custom_ajax_calls.js'
import { comprasBaseUrl } from '../urls.js'
import DiskSet from '../utils/DiskSet.js'
import config from '../../crawlee.json' assert { type: "json" };


// creat a set do that we don't forget which compras we have already scrapped
let scraped = new DiskSet('scraped_codes', null, 
    process.cwd() + '/' + config.storageDir 
    + '/datasets/' + config.defaultDatasetId
)

const handleSeachPage = async ({ page, crawler, enqueueLinks, log, proxyInfo }) => {
    /* this is the code that is used to handle the compra seach page */
    let { scrapThisMonth, scrapToday, 
        startDate, endDate } = config;
    // dates to scrap
    if(scrapToday){
        log.info('scrap compras of today')
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

    // wait until page loads
    await page.waitForLoadState('networkidle'); 

    // for every date range
    for( let dates of date_batches ){
        // date to start and end
        let [ startDate, endDate ] = dates
        // send search request of the date interval
        let { count } = await page.evaluate(
            queryProcessesCount, 
            { ...config, startDate, endDate }
        );
        log.info(`Between ${startDate} and ${endDate} found ${ count } compras`)
        // for every 20 pagination of the page
        for(let p = 0; p < count/20; p++){
            // for every 
            let compras = await page.evaluate(
                queryComprasPage, 
                { ...config,
                    count, 
                    pagination: p,
                    startDate, 
                    endDate }
            )

            // forevery compra publica that we found
            compras = compras
                .map(c => 
                    // decode the keys
                    decode(c)
                ).map( c => ({ 
                    // create proper url
                    link: comprasBaseUrl
                    + `informacionProcesoContratacion${c.api_version}.cpe?`
                    + `idSoliCompra=${c['idSoliCompra']}`,
                    ...c,
                })).filter( c => {
                    // check if we have not scrap that compras code before
                    if(scraped.checkValue(c['Código'])){
                        log.warning(`${c['Código']} already scrapped`)
                        return false
                    } else 
                        return true
                })
                    
            // for every compra make add to the request queue to scrap
            await Promise.all( 
                compras.map( async c => 
                    await crawler
                    .requestQueue
                    .addRequest({
                        method: 'GET',
                        url: c.link,
                        uniqueKey: c['Código'],
                        label: 'compra',
                        userData: c
                    })
                )
            )
        }
    }
};

export default handleSeachPage
