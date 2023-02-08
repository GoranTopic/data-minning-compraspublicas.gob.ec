import { parse } from 'node-html-parser';
let base_url = 'https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/ProcesoContratacion/';


const parseArchivosTable = html => {
    html = html.trim()
    let archivos = []
    const root = parse(html);
    let file_links = root.getElementsByTagName('a');
    file_links = file_links.map( e => base_url + e.getAttribute('href'))
    let divs = root.getElementsByTagName('div');
    let titles = divs.map(d => 
            d.text.trim().replace(/(\r\n|\n|\r|^[ ]+|[ ]+$)/gm, "")
        ).filter( (d,i) => !( i === 0 | i === 1) &&
            (d !== '') && ! d.startsWith('Archivo que contiene') 
        )
    for(let i =0; i < file_links.length; i++){
        archivos.push( { 
            title: titles[i],
            url: file_links[i]
        })
    }
    return archivos
}


export default parseArchivosTable
