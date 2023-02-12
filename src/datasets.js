import { Dataset } from 'crawlee';
import procesos from './procesos.js' ;

/* this code handles making all the data set for each enabled  type of process*/

let datasets = {}
// fill the data sets
await Promise.all( procesos
    .filter(p=>p.isEnabled)
    .map( async p => 
        datasets[ p['datasetId'] ] =
        await Dataset.open(p.datasetId)
    )
)

export default datasets;

