import { queryComprasPage, queryProcessesCount, decode } from '../reverse_engineering/custom_ajax_calls.js'
import { comprasBaseUrl } from '../urls.js'
import DiskSet from '../utils/DiskSet.js'
import config from '../../crawlee.json' assert { type: "json" };

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
        queryProcessesCount, { ...config, startDate, endDate }
    );
    // for every 20 pagination of the page
    for(let p = 0; p < count; p+=20){
        // NOTE: this pagination is very weird.
        // It counts every 20 entries, so page 1 and 20
        // are the same page, and 21 is th next page.
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
    let new_compras = compras
        .map(c =>
            // decode the keys
            decode(c)
        ).map( c => ({ 
            // it is not provided by the back end request
            // create proper url
            url: comprasBaseUrl
            + `informacionProcesoContratacion${c.api_version}.cpe?`
            + `idSoliCompra=${c['idSoliCompra']}`,
            ...c,
        })).filter( c => {
            // check if we have not scrap that compras code before
            if(scraped.hasValue(c['Código'])){
                //log.warning(`${c['Código']} already scrapped`)
                return false
            } else{
                //log.debug(`${c['Código']} has not been scraped scrapped`)
                return true
            }
        })
    // add them to the global count
    TOTAL_COMPRAS_COUNT += parseInt(count);
    // count the one we have already scrapped
    TOTAL_COMPRAS_SCRAPED  += compras.length - new_compras.length;

    // log information
    log.info(`Between ${startDate} and ${endDate} found ${ new_compras.length } new compras. Tota; ${TOTAL_COMPRAS_COUNT}`);
    log.info(`tota compras to scrap ${TOTAL_COMPRAS_COUNT}`);
    log.debug(`Proxy: ${proxyInfo.url}, ${proxyInfo.sessionId}`);
    log.debug(`
    Between ${startDate} and ${endDate} we got:
    ${ compras.length } found compras
    new_compras: ${ new_compras.length },
    server send: ${ count },
    TOTAL_COMPRAS_COUNT: ${TOTAL_COMPRAS_COUNT}
    TOTAL_COMPRAS_SCRAPED:  ${TOTAL_COMPRAS_SCRAPED}
    `);

    // for every compra make add to the request queue to scrap
    await Promise.all(
        new_compras.map( async c =>
            await crawler
            .requestQueue
            .addRequest({
                method: 'GET',
                url: c.url,
                uniqueKey: c['Código'],
                label: 'compra',
                userData: c
            })
        )
    )
}

export default handleSeachPage
