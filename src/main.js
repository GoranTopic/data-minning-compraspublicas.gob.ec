import config from '../crawlee.json' assert { type: "json" };
process.env["CRAWLEE_STORAGE_DIR"] =  config.storageDir
// For more information, see https://crawlee.dev/
import { PlaywrightCrawler, Dataset } from 'crawlee';
import { router } from './router.js';
import proxyConfig from './proxies.js'
import { homePage } from './urls.js'

// total number of compras per date range
global.TOTAL_COMPRAS_TO_SCRAP = 0; 
global.TOTAL_COMPRAS_SCRAPED  = 0;
// make configuration file for crawler
let crawler_config = {}
// get proxies
if(config.proxyMode) 
    crawler_config.proxyConfiguration = proxyConfig;
// add router
crawler_config.requestHandler = router;
crawler_config.useSessionPool = true;
// Overrides default Session pool configuration
crawler_config.sessionPoolOptions = {
    maxPoolSize: config.maxPoolSize,
    sessionOptions: config.sessionOptions,
}
// Set to true if you want the crawler to save cookies per session,
crawler_config.persistCookiesPerSession= true;
// se the maximum allowed conrurent requests
crawler_config.maxConcurrency = config.maxConcurrency
// limit the ammount of reques tper minute
crawler_config.maxRequestsPerMinute = config.maxRequestsPerMinute
// initiate crawler
const crawler = new PlaywrightCrawler(crawler_config);
// set start at the home page
const startUrls = [ homePage ];
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

