import config from '../crawlee.json' assert { type: "json" };
process.env["CRAWLEE_STORAGE_DIR"] =  config.storageDir
// For more information, see https://crawlee.dev/
import { PlaywrightCrawler, Dataset } from 'crawlee';
import { router } from './router.js';
import proxyConfig from './proxies.js'
import { buscarProcesoRE } from './urls.js'
// read secret
import * as dotenv from 'dotenv' 
dotenv.config()
// set sotrage dir as an eviromental variable
// make configuration file fro crawler
let crawler_config = {}
// get proxies
if(config.proxyMode) crawler_config.proxyConfiguration = proxyConfig;
// add router
crawler_config.requestHandler = router;
crawler_config.useSessionPool =true;
// Overrides default Session pool configuration
crawler_config.sessionPoolOptions = {
    maxPoolSize: 1000,
    sessionOptions:{
        maxAgeSecs: 60,
        maxUsageCount: 10, // only 
    },
}
// Set to true if you want the crawler to save cookies per session,
crawler_config.persistCookiesPerSession= true;
// initiate crawler
const crawler = new PlaywrightCrawler(crawler_config);
// set starting url
const startUrls = [ buscarProcesoRE ]
// start on search processos page
await crawler.run(startUrls);
// create cvs database
// check if database has undefined entries
//if( 
//console.log(await Dataset.getData())
//.items.some(i => i === undefined) )
//console.error(new Error('some entries are undefined'))
//else // if not, make into csv
//await Dataset.exportToCSV('compras_publicas', { toKVS: 'my-data' });

