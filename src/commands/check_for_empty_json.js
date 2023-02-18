import { read_json, mkdir, fileExists, write_json } from '../utils/files.js';
import config from '../../crawlee.json' assert { type: "json" };
import { readdirSync, renameSync, existsSync, unlink } from 'fs'
import procesos from '../procesos.js' ;
import prompt_sync from 'prompt-sync';
import prompt_history from 'prompt-sync-history';

// initiate prompt
const prompt = prompt_sync({ history: prompt_history() })


const getJsonFiles = source =>
  readdirSync(source, { withFileTypes: true })
    .filter(j => j.isFile())
    .map(j => j.name)

const isJsonEmpty = json =>
    (Object.keys(json).length === 0)? true: false


// get all of the json files form a given dir
let datasets = [];
// get the paths of the datasets
Object.entries(procesos)
    .map(p => p[1])
    .filter(p => p.isEnabled)
    .map( p => datasets.push(
        config.storageDir + '/datasets/' + p.datasetId
    ));


let emptyJsons = [];
for(let dataset of datasets){
    console.log(`chekcing dataset: ${dataset}`);
    for(let jsonFilename of getJsonFiles(dataset)){
        let jsonPath = dataset + '/' + jsonFilename;
        let json = read_json(jsonPath);
        if( json === null || isJsonEmpty(json) ){
            console.log(`found empty json: ${jsonPath}`);
            emptyJsons.push(jsonPath);
        }
    }
}

if(emptyJsons.length < 0){
    let input = prompt('Do you want to remove them? [y/n] ');
    if(input === 'y'){
        emptyJsons.forEach( e_j => {
            unlink(e_j, (err) => {
                if (err) {
                    console.error(err);
                    return;
                }
                console.log(`${e_j} removed successfully`);
            });
        });
    }
}else{
    console.log('no empty jsons found')
}
