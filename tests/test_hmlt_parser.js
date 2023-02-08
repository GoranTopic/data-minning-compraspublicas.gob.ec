import parseDescritionTable from '../src/parsers/description.js'
import parseFechasTable from '../src/parsers/fechas.js'
import parseProductosTable from '../src/parsers/productos.js'
import parseParametrosTable from '../src/parsers/parámetrosDeCalificación.js'
import parseArchivosTable from '../src/parsers/archivos.js'
import fs from 'fs'

const description_html = fs.readFileSync(`./tests/descriptionTab.html`, "utf8");
const fechas_html = fs.readFileSync(`./tests/fechasTab.html`, "utf8");
const productos_html = fs.readFileSync(`./tests/productosTab.html`, "utf8");
const parámetros_html = fs.readFileSync(`./tests/parámetrosDeCalificaciónTab.html`, "utf8");
const archivos_html = fs.readFileSync(`./tests/archivosTab.html`, "utf8");


let tab_order = [ '', 'Descripción', 'Fechas', 'Productos', 'Parámetros de Calificación', '', 'Archivos' ] 

const parseTable = (type, html) =>{
    switch(type) {
        case 'Descripción':
            return parseDescritionTable(html);
        case 'Fechas':
            return parseFechasTable(html);
        case 'Productos':
            return parseProductosTable(html);
        case 'Parámetros de Calificación':
            return parseParametrosTable(html);
        case 'Archivos':
            return parseArchivosTable(html);
        default:
            // code block
            break;
    } 

}


//console.log(parseTable('Descripción', description_html))
//console.log(parseTable('Fechas', fechas_html))
//console.log(parseTable('Productos', productos_html))
//console.log(parseTable('Parámetros de Calificación', parámetros_html))
console.log(parseTable('Archivos', archivos_html))



