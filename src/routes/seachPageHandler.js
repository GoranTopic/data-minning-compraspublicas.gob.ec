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
    let { dates: [ startDate, endDate ], typeofProcess } = request.userData;
    // get the code of the type of process to query the backend
    let { txtTiposContratacion } = typeofProcess;
    // wait until page loads
    await page.waitForLoadState('networkidle'); 
    // query the webstie of the count of the proceses 
    // between the date intevals
    let { count } = await page.evaluate(
        queryProcessesCount, { 
            ...config, txtTiposContratacion,
            startDate, endDate, 
        }
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
                    startDate, endDate,
                    txtTiposContratacion,
                }
            );
        //  add results to the compras count
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
            typeofProcess,
            ...c,
        })).filter( c => 
            // check if we have not scrap that compras code before
            ! scraped.hasValue( c['Código'] )
        );
    // add them to the global count
    TOTAL_COMPRAS_TO_SCRAP += parseInt(count);
    // count the one we have already scrapped
    TOTAL_COMPRAS_SCRAPED  += compras.length - new_compras.length;
    // log information
    log.info(`Between ${startDate} and ${endDate} found ${ new_compras.length } new compras. Tota; ${TOTAL_COMPRAS_TO_SCRAP}`);
    log.info(`Tota compras to scrap ${TOTAL_COMPRAS_TO_SCRAP}`);
    log.debug(`Proxy: ${proxyInfo.url}, ${proxyInfo.sessionId}`);
    log.debug(`
    In ${typeofProcess.proceso} 
    Between ${startDate} and ${endDate} we got:
    ${ compras.length } found compras
    new_compras: ${ new_compras.length },
    server send: ${ count },
    TOTAL_COMPRAS_TO_SCRAP: ${TOTAL_COMPRAS_TO_SCRAP}
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
                userData: c,
            })
        )
    )
}

export default handleSeachPage
