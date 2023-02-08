import { Dataset, createPlaywrightRouter, sleep } from 'crawlee';
import { divideDatesIntoIntervals, todaysDate } from './utils/dates.js';
import { queryComprasPage, queryProcessesCount, decode } from './reverse_engineering/custom_ajax_calls.js'
import { query_tab } from './reverse_engineering/XMLHttpRequest.js'
import tabParser from './parsers/tabParser.js'
import config from '../crawlee.json' assert { type: "json" };
import download_pdf from './utils/download_pdf.js';
import { mkdir, fileExists } from './utils/files.js'
import { comprasBaseUrl, tabBaseUrl } from './urls.js'
import DiskSet from './utils/DiskSet.js'

// creat a set do that we don't forget which compras we have already scrapped
let scraped = new DiskSet('scraped_codes', null, 
    process.cwd() + '/' + config.storageDir 
    + '/datasets/' + config.defaultDatasetId
)

export const router = createPlaywrightRouter();

router.addDefaultHandler( async ({ page, crawler, enqueueLinks, log }) => {
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
            // decode the keys
                .map(c => decode(c))
            // create proper url
                .map( c => ({ 
                    link: comprasBaseUrl
                    + `informacionProcesoContratacion${c.api_version}.cpe?`
                    + `idSoliCompra=${c['idSoliCompra']}`,
                    ...c,
                }));

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
});


router.addHandler('compra', 
    async ({ request, page, log, enqueueRequest }) => {
        // get options 
        let { downloadFiles, storageDir, defaultDatasetId } = config;
        // get request defined data
        let { Código, idSoliCompra } = request.userData
        log.info(`Scrapping Compra ${Código} at ${request.url}`)
        // check if we have not scrap that url before
        if( scraped.checkValue(Código) )
            return log.warning(`${Código} already scrapped`)
        // wait for page to load
        await page.waitForLoadState('networkidle'); 
        // empty obj to store scraped data
        let compra = {}
        // start to scrap tabs...
        let tab_count = 7;
        let tab_order = [ '', 'Descripción', 'Fechas', 'Productos', 'Parámetros de Calificación', '', 'Archivos' ] 
        // for every tab
        for( let tab = 1; tab < tab_count; tab++)
            if(tab_order[tab]){
                let url = tabBaseUrl
                    + `tab=${tab}`
                    + `&id=${idSoliCompra}`;
                let res = await page.evaluate(query_tab, url);
                if(res) compra[tab_order[tab]] = tabParser(
                    tab_order[tab], 
                    res.srcElement.responseText
                )
            }
        // add url 
        compra['url'] = request.url;

        // download files in enabled 
        if(downloadFiles){
            let filesDir = process.cwd()+'/'+storageDir 
                + '/datasets/' + defaultDatasetId + '/files/'
            mkdir(filesDir);
            await Promise.all(
                compra['Archivos']
                .map( async a => {
                    let compraDir = filesDir + compra['Descripción']['Código']
                    let filePath = compraDir + a.title
                    mkdir(compraDir)
                    if(fileExists(filePath)){
                        log.warning(`File ${filePath} already exists`)
                        return false
                    }
                    let result = await download_pdf(
                        a.url, // pdf src
                        page, // page
                        filePath // where to save
                    )
                    if(result) log.info(`Downloaded ${filePath}`)
                    else log.error(`Could not downloaded ${filePath}`)
                })
            )
        }

        log.info(`saving compra public with code ${compra['Descripción']['Código']}`);
        //save data
        await Dataset.pushData(compra);
        // add to list of already scraped codes
        scraped.add(Código);
    }
);
