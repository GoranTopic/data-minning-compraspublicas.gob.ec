import datasets from '../datasets.js'
import DiskSet from '../utils/DiskSet.js'
import Checklist from '../utils/Checklist.js'
import { query_tab } from '../reverse_engineering/XMLHttpRequest.js'
import tabParser from '../parsers/tabParser.js'
import processes from '../procesos.js';
import config from '../../crawlee.json' assert { type: "json" };
import download_pdf from '../utils/download_pdf.js';
import { mkdir, fileExists } from '../utils/files.js'
import { comprasBaseUrl, tabBaseUrl } from '../urls.js'

// creat a set do that we don't forget which compras we have already scrapped
let scraped = new DiskSet('scraped_codes', null,
    config.storageDir + '/datasets/' + config.defaultDatasetId
)

const handleCompraPage = async ({ request, page, log, enqueueRequest, session, proxyInfo }) => {
    // get options 
    let { downloadFiles, storageDir, defaultDatasetId } = config;
    // get request defined data about the compra
    let { Código, idSoliCompra, typeofProcess } = request.userData
    log.info(`Scrapping Compra ${Código} at ${request.url}`)
    log.debug(`Proxy: ${proxyInfo.url}, session ${proxyInfo.sessionId}`);
    // wait for page to load
    await page.waitForLoadState('networkidle'); 
    // empty obj to store scraped data
    let compra = {}
    // start to scrap tabs...
    let tab_count = 7;
    let tab_order = [ '', 'Descripción', 'Fechas', 'Productos', 'Parámetros de Calificación', '', 'Archivos' ] 
    // for every tab we query the tab, 
    // parse it and save it in the compra obj
    // to wri tot he dataset
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
    // get the datasetid and the path of the datase
    let { datasetId, proceso } = processes[typeofProcess];
    // add url 
    compra['url'] = request.url;
    // add type of porcess
    compra['typo de proceso'] = proceso;
    // get the data set
    let dataset = datasets[datasetId];
    // download files in enabled 
    if(downloadFiles){
        let abosluteDir = storageDir + '/datasets/' + datasetId + '/files/'
        let relativeDir = './datasets/' + datasetId + '/files/'
        mkdir(abosluteDir);
        let compraCode = compra['Descripción']['Código']
        let fileChecklist = new Checklist(
            compraCode + '_file_checklist', 
            compra['Archivos'],
            abosluteDir
        ) 
        await Promise.all(
            compra['Archivos']
            .map( async (a,i) => {
                // if it is not checked off
                if(!fileChecklist.isCheckedOff(a)){
                    let aboslutePath = abosluteDir + compraCode + '/' + a.title;
                    let relativePath = relativeDir + compraCode + '/' + a.title;
                    mkdir(abosluteDir + compraCode);
                    if(fileExists(aboslutePath)){
                        log.warning(`File ${aboslutePath}.pdf already exists`)
                        return false
                    }
                    let result = await download_pdf(
                        a.url, // pdf src
                        page, // page
                        aboslutePath // where to save
                    )
                    if(result){
                        log.info(`Downloaded ${relativePath}.pdf`);
                        log.debug(`Proxy: ${proxyInfo.url}, Session ${proxyInfo.sessionId}`);
                        // save where we donwloaded the file
                        compra['Archivos'][i]['local_url'] = relativePath + '.pdf';
                        // add to stats downloaded pdf
                        TOTAL_FILES_DOWNLOADED++;
                        processes[typeofProcess].stats.pdfs_downloaded++;
                        // checoff
                        fileChecklist.check(a);
                    }
                    else log.error(`Could not downloaded ${aboslutePath}.pdf`)
                }
            })
        )
        // if all the files have been downloaded
        if(fileChecklist.isDone()) fileChecklist.delete()
    }

    // count the scrapped file
    TOTAL_COMPRAS_SCRAPED++;
    processes[typeofProcess].stats.compras_scraped++;
    log.info(`Compra ${compra['Descripción']['Código']} scraped. ${TOTAL_COMPRAS_SCRAPED}/${TOTAL_COMPRAS_TO_SCRAP}`);
    //save data
    await dataset.pushData(compra);
    // add to list of already scraped codes
    scraped.add(Código);
}

export default handleCompraPage
