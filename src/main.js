import config from '../crawlee.json' assert { type: "json" };
process.env["CRAWLEE_STORAGE_DIR"] =  config.storageDir
// For more information, see https://crawlee.dev/
import { PlaywrightCrawler, sleep } from 'crawlee';
import { router } from './router.js';
import proxyConfi from './proxies.js'
import { buscarProcesoRE } from './urls.js'
// read secret
import * as dotenv from 'dotenv' 
dotenv.config()
// set sotrage dir as an eviromental variable
// make configuration file fro crawler
let crawler_config = {}
// get proxies
if(config.proxyMode) crawler_config.proxyConfiguration = proxyConfi;
// add router
crawler_config.requestHandler = router;
// initiate crawler
const crawler = new PlaywrightCrawler(crawler_config);
// set starting url
const startUrls = [ buscarProcesoRE ]
// start on search processos page
await crawler.run(startUrls);
