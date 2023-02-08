import { parse } from 'node-html-parser';

const parseFechasTable = html =>{
    let dates = {}
    const root = parse(html);
    const rows = root.getElementsByTagName('tr');
    for(let row of rows){
        let title = row.getElementsByTagName('th')[0];
        let [ date, descrition ] = row.getElementsByTagName('td');
        // add to object
        title && date && (
            dates[title.text.trim()] = { 
                fecha: date.text.trim(), 
                descrition: descrition.text.trim()
            }
        )
    }
    return dates
};

export default parseFechasTable
