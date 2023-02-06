// For more information, see https://crawlee.dev/
import { PlaywrightCrawler, ProxyConfiguration, sleep } from 'crawlee';
import { router } from './routes.js';
// read secret
import * as dotenv from 'dotenv' 
dotenv.config()

const startUrls = ['https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/PC/buscarProcesoRE.cpe?op=P#'];

const crawler = new PlaywrightCrawler({
    // proxyConfiguration: new ProxyConfiguration({ proxyUrls: ['...'] }),
    requestHandler: router,
});

await crawler.run(startUrls);
