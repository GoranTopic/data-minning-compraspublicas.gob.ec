import { parse } from 'node-html-parser';

const parseDescritionTable = html =>{
    let table = {}
    const root = parse(html);
    const rows = root.getElementsByTagName('tr');
    for(let row of rows){
        let header = row.getElementsByTagName('th')[0]
            ?.text
            ?.replace(':', "")
            ?.trim()
        let field = row.getElementsByTagName('td')[0]
            ?.text
            ?.trim();
        // add to object
        header? field? 
            table[header] = field :
            table[header] = '' : 
            ''
    }
    return table
}

export default parseDescritionTable;
