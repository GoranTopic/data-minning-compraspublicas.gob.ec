import { createPlaywrightRouter } from 'crawlee';
import handleSeachPage from './routes/handleSeach.js'
import handleCompraPage from './routes/handleCompra.js'

// make a router
export const router = createPlaywrightRouter();

// seach page for compras
router.addDefaultHandler(handleSeachPage);

// scrap the actual compra page
router.addHandler('compra',  handleCompraPage)
