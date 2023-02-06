import { Dataset, createPlaywrightRouter, sleep } from 'crawlee';
import { divideDatesIntoIntervals } from './utils.js';
import config from '../crawlee.json' assert { type: "json" };
import { queryComprasPage, queryProcessesCount, decode } from './reverse_engineering/custom_ajax_calls.js'

export const router = createPlaywrightRouter();

router.addDefaultHandler( async ({ page, enqueueLinks, log }) => {
    let { palabrasClaves, entidadContratante, tipoDeContratacion,
            tipoDeCompra, codigoDelProceso, scrapToday,
            startDate, endDate } = config;

    // wait until page loads
    await page.waitForLoadState('networkidle'); 
    if(config.scrapToday){
        log.info('scrap compras of today')
        // wait until it button loads
        //await page.waitForSelector("toolbarbotones")
        log.info('quering compras count')
        // send search request
        /*
        let comprasCount = await page.evaluate(
            queryProcessesCount, 
            config
        )
        */
        //console.log(comprasCount)
        let compras = await page.evaluate(
            queryComprasPage, 
            { count: 2, 
                pagination: 0,
                ...config
            }
        )
        compras = compras.map(c => decode(c));
        console.log(compras);
    }else{
        // divide into date bacthes
        // for each batch
        //      set paramter dates
        //      click search button
        //      wait until it loads
        //      await scrapCompras
    }


});

const setSearchParamters = async (page, params)  => {

}

const scrapComprasList = async (page, enqueueLinks, log) => {
    /* scrap the output of the company seach, with all the pagination*/

}

const scrapComprasPage = async (page, enqueueLinks, log) => {
    /* scrap the output of the company seach, with all the pagination*/
    await enqueueLinks({
        globs: ['https://crawlee.dev/**'],
        label: 'detail',
    });

}


router.addHandler('compra', async ({ request, page, log }) => {
    const title = await page.title();
    log.info(`${title}`, { url: request.loadedUrl });
    await Dataset.pushData({
        url: request.loadedUrl,
        title,
    });
});


router.addHandler('file', async ({ request, page, log }) => {
    const title = await page.title();
    log.info(`${title}`, { url: request.loadedUrl });
    await Dataset.pushData({
        url: request.loadedUrl,
        title,
    });
});



