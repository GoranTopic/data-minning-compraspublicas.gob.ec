import { Dataset } from 'crawlee';
import DiskSet from '../utils/DiskSet.js'
import { query_tab } from '../reverse_engineering/XMLHttpRequest.js'
import tabParser from '../parsers/tabParser.js'
import config from '../../crawlee.json' assert { type: "json" };
import download_pdf from '../utils/download_pdf.js';
import { mkdir, fileExists } from '../utils/files.js'
import { comprasBaseUrl, tabBaseUrl } from '../urls.js'

// creat a set do that we don't forget which compras we have already scrapped
let scraped = new DiskSet('scraped_codes', null, 
    process.cwd() + '/' + config.storageDir 
    + '/datasets/' + config.defaultDatasetId
)

const handleCompraPage = async ({ request, page, log, enqueueRequest, session, proxyInfo }) => {
    // get options 
    let { downloadFiles, storageDir, defaultDatasetId } = config;
    // get request defined data
    let { Código, idSoliCompra } = request.userData
    log.info(`Scrapping Compra ${Código} at ${request.url}`)
    log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);
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
            .map( async (a,i) => {
                let compraDir = filesDir + compra['Descripción']['Código']
                let filePath = compraDir + '/' + a.title
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
                if(result){
                    log.info(`Downloaded ${filePath}`);
                    log.debug(`Proxy: ${proxyInfo.url}, Session ${proxyInfo.sessionId}`);
                    // save where we donwloaded the file
                    compra['Archivos'][i]['local_url'] = filePath;
                }
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

export default handleCompraPage
