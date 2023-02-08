import { read_json, write_json, mkdir } from '../utils/files.js'


/* this class is similar to the disklist, but it remove any repeated values */
class DiskSet{
	constructor(name, values = null, path){
		this.dir_path = path??  data_directory + '/resources/list';
		mkdir(this.dir_path);
		this.name = name + ".json";
		this.filename = this.dir_path + '/' + this.name
		// try to read already saved values
		if(!values) values = read_json( this.filename ) ?? [];
		// create set
		this.set = new Set(values);
		// after done checking save to memeory
		this._save();
	}

	// save value
	_save = () => write_json( [ ...this.set ], this.filename );

	// add value to set, if unique it add it to array
	_add = value => {
		if( this.set.has(JSON.stringify(value)) )
			return false;
		else{ // if it not in the set
			this.set.add(JSON.stringify(value));
			return true;
		}
	}

	// add and saves value
	add = value => (this._add(value))? this._save() : false ;

	// remove value
	remove = value => {
		if( this.set.has(JSON.stringify(value)) ){
			this.set.delete(JSON.stringify(value))
			this._save();
			return true
		}else return false
	}


	// values 
	getValues = () => [ ...this.set ]

	// check if a passed value in on the list
	checkValue = value => this.set.has(JSON.stringify(value))

	// values count
	valuesCount = () => this.values.size


}

export default DiskSet

