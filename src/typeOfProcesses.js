// this are the configurations
import config from '../crawlee.json' assert { type: "json" };
// this are th eoptions in the crawlee, which say if they enable 
// to be scraped
let { procesoDeContratación, procesoRégimenEspecial, 
    procedimientosEspeciales } = config ;
//  this are the url of the seach page
import { buscarProcesoDeContratación, buscarProcesoRégimenEspecial, 
    buscarProcesoProcedimientosEspeciales } from './urls.js';


/* this script keep track of the porcess that we need to scrp. 
 * They have difrent urls, databses, and directories
 * */
let typeOfProcesses = [{
    proceso: 'procesosDeContratacion',
    // this where the dataset is goin to store the values
    datasetId: 'procesosDeContratacion',
    // this it he url fro the search pag of the type of proocess
    seachPageUrl: buscarProcesoDeContratación,
    // this is whether of not it is enabled the process
    isEnabled: procesoDeContratación,
    // this is the code used by the backend server
    // apperently procesos de contratacion 
    // does not have a code
    // txtTiposContratacion:,
    // stadistic to keep track of
    stats: {
        compras_to_scrap: 0,
        compras_scraped: 0,
        pdfs_downloaded: 0,
    }
}, {
    proceso: 'procesosDeRegimenEspeciales',
    datasetId: 'procesosDeRegimenEspeciales',
    seachPageUrl: buscarProcesoRégimenEspecial,
    isEnabled: procesoRégimenEspecial,
    txtTiposContratacion: 186,
    stats: {
        compras_to_scrap: 0,
        compras_scraped: 0,
        pdfs_downloaded: 0,
    }
}, {
    proceso: 'procedimientosEspeciales', 
    datasetId: 'procedimientosEspeciales',
    seachPageUrl: buscarProcesoProcedimientosEspeciales,
    isEnabled: procedimientosEspeciales,
    txtTiposContratacion: 219,
    stats: {
        compras_to_scrap: 0,
        compras_scraped: 0,
        pdfs_downloaded: 0,
    }
}]

export default typeOfProcesses;
