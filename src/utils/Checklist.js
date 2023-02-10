import { read_json, write_json, delete_json, mkdir } from '../utils/files.js'

// get data directory
let data_directory =  process.cwd();

/* this class makes a checklist for value that need to be check,
 * it takes a check function whihc goes throught the values. */
class Checklist{
    /* this function takes list of name name to check and */
    constructor(name, values, path, options={ recalc_on_check: true }){
        // only for script
        this.dir_path = path ?? data_directory + '/resources/checklists';
        mkdir(this.dir_path);
        // if you want to mantain the original missing list of value after checks
        this.recalc_on_check = options.recalc_on_check;
        this.name = name + ".json";
        this.filename = this.dir_path + '/' + this.name
        this.checklist = read_json(this.filename);
        this.values = values ?? [];
        this.missing_values = [];
        // make checklist
        if(!this.checklist){
            this.checklist = {};
            for(let value of this.values){
                if(this._isObject(value))
                    value = JSON.stringify(value)
                this.checklist[value] = false
            }
        }else // if we found checklist in memory
            this.values = Object.keys(this.checklist);
        // calculate the missing values
        this._calcMissing();
        // save new checklist
        write_json(this.checklist, this.filename);
    }

    _isObject = (objValue) =>
        ( objValue &&
            typeof objValue === 'object' &&
            objValue.constructor === Object );

    _calcMissing = () => {
        this.missing_values = [];
        this.values = Object.keys(this.checklist);
        this.values.forEach( value  => {
            if(this._isObject(value))
                value = JSON.stringify(value)
            if(! this.checklist[value] )
                this.missing_values.push(value)
        })
    }

    valuesDone = () => 
        this.values.length - this.missing_values.length;

    getMissingValues = () =>{
        debugger;
        return this.missing_values;
    }

    missingLeft = () =>
        this.missing_values.length

    nextMissing = () =>
        this.missing_values.shift();

    check = (value, mark = true) => {
        /* checks a value on the list as done */
        if(this._isObject(value))
            value = JSON.stringify(value)
        this.checklist[value] = mark;
        if(this.recalc_on_check) 
            this._calcMissing();
        return write_json(this.checklist, this.filename);
    }

    uncheck = value => {
        /* unchecks a value on on the list which might have been done */
        if(this._isObject(value))
            value = JSON.stringify(value)
        this.checklist[value] = false;
        if(this.recalc_on_check) 
            this._calcMissing();
        return write_json(this.checklist, this.filename);
    }

    add = (value, overwrite = true) => {
        /* add a value as not done to the list
         * if overwrite is true, it writes over any truely value */
        if(this._isObject(value)) value = JSON.stringify(value)
        // if it is not in the list, or overwrite is true
        if(!this.checklist[value] || overwrite){
            this.checklist[value] = false;
        }
        this._calcMissing();
        return write_json(this.checklist, this.filename);
    }

    addList = (values, overwrite=true) => {
        /* adds a list of values as not done to the list */
        debugger
        for(let value of values)
            this.add(value, overwrite);
        return true;
    }

    isCheckedOff = value => {
        /* Checks if all value has been already been checked off */
        if(this._isObject(value))
            value = JSON.stringify(value)
        return this.checklist[value]
    }

    // returns all key values
    getAllValues = () => Object.keys(this.values)


    // returns length of all the values
    valuesCount = () => Object.keys(this.values).length

    isDone = () =>
        /* checks if all the value on the checklist are done */
        Object.values(this.checklist).every(v => v)

    remove = value => {
        // remvoes the value from the list
        if(this._isObject(value)) value = JSON.stringify(value)
        delete this.values[value];
        this._calcMissing();
    }

    delete = () =>  {
        /* delete the checklist from disk*/
        this.values = []
        this.checklist = []
        delete_json(this.filename)
    }
}

export default Checklist;
