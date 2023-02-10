import { createPlaywrightRouter } from 'crawlee';
import handleDatesDivision from './routes/datesDivisionHandler.js'
import handleSeachPage from './routes/seachPageHandler.js'
import handleCompraPage from './routes/compraHandler.js'

// make a router
export const router = createPlaywrightRouter();

// let divide into dates batches
router.addDefaultHandler(handleDatesDivision);

// make a query in the search page 
// and handle the results
router.addHandler('seach_page', handleSeachPage);

// scrap the actual compras
// and every tab with every document
router.addHandler('compra',  handleCompraPage)
