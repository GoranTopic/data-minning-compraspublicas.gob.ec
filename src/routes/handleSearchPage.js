import { queryComprasPage, queryProcessesCount, decode } from '../reverse_engineering/custom_ajax_calls.js'
import { comprasBaseUrl } from '../urls.js'
import DiskSet from '../utils/DiskSet.js'
import config from '../../crawlee.json' assert { type: "json" };
import Checklist from '../utils/Checklist.js'

// make a check list for the dates
let dateChecklist = new Checklist(
    'dates_checklist', null,
    process.cwd() + '/' + config.storageDir
    + '/datasets/' + config.defaultDatasetId
)

// creat a set do that we don't forget which compras we have already scrapped
let scraped = new DiskSet('scraped_codes', null, 
    process.cwd() + '/' + config.storageDir 
    + '/datasets/' + config.defaultDatasetId
)

const handleSeachPage = async ({ request, page, crawler, log, proxyInfo, session }) => {
    /* this is the code that is used to handle the compra seach page */
    // where we are going to store all the compras of the page
    let compras = [];
    // date to start and end
    let { startDate, endDate } = request.userData
    // wait until page loads
    await page.waitForLoadState('networkidle'); 
    // send search request of the date interval
    let { count } = await page.evaluate(
        queryProcessesCount, 
        { ...config, startDate, endDate }
    );
    // add them to the global count
    TOTAL_COMPRAS_COUNT += parseInt(count);
    // log information
    log.info(`Between ${startDate} and ${endDate} found ${ count } compras`);
    log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);
    // for every 20 pagination of the page
    for(let p = 0; p < count/20; p++){
        // query the next page
        let result =
            await page.evaluate(
                queryComprasPage,
                { ...config,
                    count,
                    pagination: p,
                    startDate,
                    endDate }
            );
        compras = compras.concat(result)
    }

    // process every compra that we found
    let valid_compras = compras
        .map(c =>
            // decode the keys
            decode(c)
        ).map( c => ({
            // create proper url
            link: comprasBaseUrl
            + `informacionProcesoContratacion${c.api_version}.cpe?`
            + `idSoliCompra=${c['idSoliCompra']}`,
            ...c,
        }))

    let codes = new Set(valid_compras.map(c => c['Código']))
    console.log(codes)

    /*
 .filter( (c, i, a) =>
            // check for unique compras based on codigo
            a.map(c => ).indexOf(c['Código']) === i
        )
        */
    /*
     * .filter( c => {
         // check if we have not scrap that compras code before
            if(scraped.hasValue(c['Código'])){
                //log.warning(`${c['Código']} already scrapped`)
                return false
            } else{
                //log.debug(`${c['Código']} has not been scraped scrapped`)
                return true
            }
        })
        */

    log.debug(`
    Between ${startDate} and ${endDate} we got:
    ${ count } from server
    valid_compras: ${valid_compras.length},
    compras ${compras.length} 
    TOTAL_COMPRAS_COUNT: ${TOTAL_COMPRAS_COUNT}`);

    /*
    if(compras.length === 0){
        log.info(`Compras between ${startDate} and ${endDate} checkedoff`)
        log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);
        dateChecklist.check([startDate, endDate])
    }

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
    */
}

export default handleSeachPage
