import { parse } from 'node-html-parser';

const parseParametrosTable = html =>{
    let parametros = {}
    const root = parse(html);
    const table = root.getElementsByTagName('table')[1];
    const rows = table.getElementsByTagName('tr');
    for(let row of rows){
        let [ header, field ] = row.getElementsByTagName('td');
        // add to object
        header? field?
            parametros[header.text.trim()] = field.text.trim() :
            parametros[header.text.trim()] = '' : 
            ''
    }
    return parametros
}

export default parseParametrosTable
