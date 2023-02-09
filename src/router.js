import { createPlaywrightRouter } from 'crawlee';
import handleSeachPage from './routes/handleSeach.js'
import handleCompraPage from './routes/handleCompra.js'
import handleDatesDivision from './routes/handleDatesDivision.js'

// make a router
export const router = createPlaywrightRouter();

// let divide into dates batches
router.addDefaultHandler(handleDatesDivision);

// make a query in the search page 
// and handle the results
router.addHandler(handleSeachPage);

// scrap the actual compras
// and every tab with every document
router.addHandler('compra',  handleCompraPage)
