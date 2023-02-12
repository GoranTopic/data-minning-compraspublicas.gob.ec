import config from '../../crawlee.json' assert { type: "json" };
import * as dotenv from 'dotenv' 
// read secret
let {parsed:{ RUC, USER, PASS }} =
    dotenv.config({path: process.cwd()+'/.secret'})

/*  */
const handlerLogin = async ({ crawler, page, log, proxyInfo }) => {
    log.info(`Attempting to login with user ${USER}`);
    // wait until page loads
    await page.waitForLoadState('networkidle'); 
    // fied in the fields
    debugger;

}

export default handlerLogin;
