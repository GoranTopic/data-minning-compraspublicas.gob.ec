import config from '../crawlee.json' assert { type: "json" };
import procesos from './procesos.js'
process.env["CRAWLEE_STORAGE_DIR"] =  config.storageDir
// For more information, see https://crawlee.dev/
import { PlaywrightCrawler, Dataset } from 'crawlee';
import { router } from './router.js';
import proxyConfig from './proxies.js'
import { homePage } from './urls.js'

// total number of compras per date range
global.TOTAL_COMPRAS_TO_SCRAP = 0; 
global.TOTAL_COMPRAS_SCRAPED  = 0;
global.TOTAL_FILES_DOWNLOADED = 0;
global.TOTAL_ERRORS  = 0; // find a way to get the errors
// make configuration file for crawler
let crawler_config = {}
// get proxies
if(config.proxyMode) 
    crawler_config.proxyConfiguration = proxyConfig;
// add router
crawler_config.requestHandler = router;
// add th eoption to add session pool
crawler_config.useSessionPool = config.useSessionPool;
// Overrides default Session pool configuration
crawler_config.sessionPoolOptions = {
    maxPoolSize: config.maxPoolSize,
    sessionOptions: config.sessionOptions,
}
// Set to true if you want the crawler to save cookies per session,
crawler_config.persistCookiesPerSession= config.persistCookiesPerSession;
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

// print stas summery
// print stats for every type of proceso

Object.entries(procesos)
    .filter(p=>p[1].isEnabled) 
    .forEach( ([t,p]) => {
        console.log(`For ${t}: `)
        console.log(p)
    })
console.log({ 
    TOTAL_COMPRAS_TO_SCRAP,
    TOTAL_COMPRAS_SCRAPED,
    TOTAL_FILES_DOWNLOADED,
})
console.log('crawlee stats: ', crawler.stats.state)
// create cvs database
// check if database has undefined entries
//if( 
//console.log(await Dataset.getData())
//.items.some(i => i === undefined) )
//console.error(new Error('some entries are undefined'))
//else // if not, make into csv
//await Dataset.exportToCSV('compras_publicas', { toKVS: 'my-data' });

