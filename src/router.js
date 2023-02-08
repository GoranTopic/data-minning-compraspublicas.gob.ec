import { Dataset, createPlaywrightRouter, sleep } from 'crawlee';
import { divideDatesIntoIntervals, todaysDate } from './utils/dates.js';
import { queryComprasPage, queryProcessesCount, decode } from './reverse_engineering/custom_ajax_calls.js'
import { query_tab } from './reverse_engineering/XMLHttpRequest.js'
import tabParser from './parsers/tabParser.js'
import config from '../crawlee.json' assert { type: "json" };
import download_pdf from './utils/download_pdf.js';
import { mkdir } from './utils/files.js'
import { comprasBaseUrl, tabBaseUrl } from './urls.js'

export const router = createPlaywrightRouter();

router.addDefaultHandler( async ({ page, crawler, enqueueLinks, requestQueue, log }) => {
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
        let [ startDate, endDate ] = dates
        //console.log(startDate);
        //console.log(endDate);
        log.info('quering compras count')
        // send search request of the date interval
        let { count } = await page.evaluate(
            queryProcessesCount, 
            { ...config, startDate, endDate }
        );
        //console.log({ count })
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

            compras = 
                compras.map(c => decode(c));
            // for every compra make add to the request queue
            //console.log(compras);
            let links = compras.map( c => 
                comprasBaseUrl
                + `informacionProcesoContratacion${c.api_version}.cpe?`
                + `idSoliCompra=${c.url_id}`
            );
            await enqueueLinks({ 
                urls: links ,
                label: 'compra',
            })
        }
    }
});


router.addHandler('compra', 
    async ({ request, page, log, enqueueRequest }) => {
        let { downloadFiles, storageDir, defaultDatasetId } = config;
        await page.waitForLoadState('networkidle'); 
        log.info(`scrapping: ${request.url}`)
        const title = await page.title();
        let idSoliCompra = request.url.split('idSoliCompra=')[1];
        let compra = {};
        let tab_count = 7;
        let tab_order = [ '', 'Descripción', 'Fechas', 'Productos', 'Parámetros de Calificación', '', 'Archivos' ] 
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
    
        //save data
        log.info(`saving compra public with code ${compra['Descripción']['Código']}`);
        await Dataset .pushData(compra);

        // download files in enabled 
        if(downloadFiles){
            let filesDir = process.cwd()+'/'+storageDir+'/'  
                + 'datasets' + '/' + defaultDatasetId + '/' 
                + 'files/'
            mkdir(filesDir);
            await Promise.all(
                compra['Archivos']
                .map( async a => {
                    let compraFileDir = filesDir + compra['Descripción']['Código']
                    mkdir(compraFileDir)
                    let result = await download_pdf(
                        a.url, // pdf src
                        page, // page
                        compraFileDir + a.title // files
                    )
                    if(result) log.info(`Downloaded ${process.cwd() + '/' + a.title}`)
                    else log.error(`Could not downloaded ${process.cwd() + '/' + a.title}`)
                })
            )
        }
    }
);
