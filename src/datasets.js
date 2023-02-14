import { Dataset } from 'crawlee';
import procesos from './procesos.js' ;
import config from '../crawlee.json' assert { type: "json" };

/* this code handles making all the data set for each enabled  type of process*/

let datasets = {}
// fill the data sets
await Promise.all(
    Object.entries(procesos)
    .map(p => p[1])
    .filter(p=>p.isEnabled)
    .map( async p => 
        datasets[ p['datasetId'] ] =
        await Dataset.open(config.storageDir + '/datasets/' + p.datasetId)
    )
)

export default datasets;

