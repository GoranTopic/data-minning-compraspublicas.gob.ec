import { parse } from 'node-html-parser';

const parseProductosTable = html => {
    let products = []
    const root = parse(html);
    var headers = root.querySelectorAll('table > thead > th')
        .map(h => h.text.trim() );
    // select second table
    const table = root.querySelectorAll('table')[1];
    // get the rows of the second table
    const rows = table.querySelectorAll('tbody tr');
    // the last row is the total row
    const total = rows.pop().childNodes[1].text;
    // fro every row   
    for(let row of rows){
        let cells = row.getElementsByTagName('td')
            .map(t => t.text.trim());
        let obj = {} 
        cells.forEach((c,i) => obj[headers[i]]=c)
        products.push(obj);
    }
    return ({ 'productos': products, 'total': total })
}

export default parseProductosTable
